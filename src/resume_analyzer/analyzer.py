import os
import re
import time
from openai import OpenAI
from anthropic import Anthropic
from prompts.analysis_prompt import get_analysis_prompt
from config.env_vars import load_env_vars
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def analyze_resume(job_description, evaluation_criteria, filename, content, model_choice):
    load_env_vars()
    prompt = get_analysis_prompt(job_description, evaluation_criteria, filename, content)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if "OpenAI" in model_choice:
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                model = "gpt-3.5-turbo" if model_choice == "OpenAI GPT-3.5" else "gpt-4o" if model_choice == "OpenAI GPT-4o" else "gpt-4"
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are an HR assistant analyzing resumes."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                result = response.choices[0].message.content.strip()
            else:  # Anthropic
                client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                model = "claude-3-sonnet-20240320"
                response = client.messages.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.7
                )
                result = response.content
            
            print(f"Raw response for {filename}:")
            print(result)
            print("-" * 50)
            
            return parse_result(result, filename, evaluation_criteria)
        
        except Exception as e:
            print(f"Error analyzing {filename}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 2})")
                time.sleep(2)
            else:
                print(f"Failed to analyze {filename} after {max_retries} attempts")
                return {
                    "Filename": filename,
                    "Name": "Error during analysis",
                    "Email": "Error during analysis",
                    "Overall Score": 0,
                    "Explanation": f"Error: {str(e)}",
                    **{f"{criterion} Score": 0 for criterion in evaluation_criteria}
                }

def parse_result(result, filename, evaluation_criteria):
    name = re.search(r"Candidate Name: (.+)$", result, re.MULTILINE)
    email = re.search(r"Email: (.+)$", result, re.MULTILINE)
    overall_score = re.search(r"Overall Score: (\d+)", result)
    explanation = re.search(r"Brief explanation: (.+)$", result, re.MULTILINE)
    
    parsed_result = {
        "Filename": filename,
        "Name": name.group(1) if name else "Not found in resume",
        "Email": email.group(1) if email else "Not found in resume",
        "Overall Score": int(overall_score.group(1)) if overall_score else 0,
        "Explanation": explanation.group(1) if explanation else "Not provided"
    }
    
    for criterion in evaluation_criteria:
        score = re.search(rf"{criterion}: (\d+)", result)
        parsed_result[f"{criterion} Score"] = int(score.group(1)) if score else 0

    time.sleep(1) # adding a small delay bwteen API calls
    return parsed_result