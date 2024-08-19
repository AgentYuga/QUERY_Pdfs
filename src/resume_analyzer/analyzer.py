import os
import re
import time
from openai import OpenAI
from anthropic import Anthropic
from handler.analysis_prompt import get_analysis_prompt
from handler.env_vars import load_env_vars
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
                model = "gpt-3.5-turbo" if model_choice == "OpenAI GPT-3.5" else "gpt-4"
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
                model = "claude-3-5-sonnet-20240620"
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


import json
import re

def parse_result(result, filename, evaluation_criteria):
    try:
        # Extract the JSON part from the result
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the response")
        
        json_str = result[json_start:json_end]
        
        # Attempt to parse the JSON output from the result
        parsed_json = json.loads(json_str)

        # Create the parsed result dictionary
        parsed_result = {
            "Filename": filename,
            "Name": parsed_json.get("name", "Not found in resume"),
            "Email": parsed_json.get("email", "Not found in resume"),
            "Overall Score": parsed_json.get("overall_score", 0),
            "Explanation": parsed_json.get("explanation", "Not provided")
        }

        # Add scores for each evaluation criterion
        scores = parsed_json.get("scores", {})
        for criterion in evaluation_criteria:
            # Create a regex pattern to match the criterion more flexibly
            pattern = re.compile(r''.join(criterion.lower().split()))
            matching_keys = [key for key in scores.keys() if pattern.search(key.lower().replace(' ', '').replace('_', ''))]
            
            if matching_keys:
                parsed_result[f"{criterion} Score"] = scores[matching_keys[0]]
            else:
                parsed_result[f"{criterion} Score"] = 0

    except (json.JSONDecodeError, ValueError) as e:
        # If JSON decoding fails or no JSON object is found, print the error and return default values
        print(f"Error processing result for {filename}: {str(e)}")
        print("Raw result:")
        print(result)
        parsed_result = {
            "Filename": filename,
            "Name": "Not found in resume",
            "Email": "Not found in resume",
            "Overall Score": 0,
            "Explanation": "Not provided"
        }
        for criterion in evaluation_criteria:
            parsed_result[f"{criterion} Score"] = 0

    # Debugging: Print parsed result before returning
    print(f"Parsed result for {filename}:")
    print(parsed_result)
    
    return parsed_result








