import os
import re
import time
from handler.analysis_prompt import get_analysis_prompt
from tenacity import retry, stop_after_attempt, wait_fixed
from handler.models import openai_model, anthropic_model, groq_model


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def analyze_resume(job_description, evaluation_criteria, filename, content, model_choice):
    #load_env_vars()
    prompt = get_analysis_prompt(job_description, evaluation_criteria, filename, content)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if "OpenAI" in model_choice:
                result = openai_model(model_choice, prompt)
            elif "Anthropic" in model_choice:
                result = anthropic_model(prompt)
            elif "Llama 3.1" in model_choice:
                result = groq_model(prompt)
            else:
                raise ValueError(f"Model {model_choice} not recognized.")
            
            # For Debugging
            # print(f"Raw response for {filename}:")
            # print(result)
            # print("-" * 50)
            
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
        # Extracting the JSON part from result
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the response")
        
        json_str = result[json_start:json_end]
        
        # parse the JSON output
        parsed_json = json.loads(json_str)

        print(f"parsed_json: {parsed_json}")

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
        #print(f"scores_before: {scores}")


        for criterion in evaluation_criteria:
            normalized_criterion = criterion.replace('\xa0', ' ')
            
            # Create a regex pattern to match the criterion
            pattern = re.compile(r''.join(normalized_criterion.lower().split()))
            normalized_scores = {key.replace('\xa0', ' '): value for key, value in scores.items()}
            matching_keys = [key for key in normalized_scores.keys() if pattern.search(key.lower().replace(' ', '').replace('_', ''))]
            
            if matching_keys:
                parsed_result[f"{criterion} Score"] = normalized_scores[matching_keys[0]]
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
    # print(f"Parsed result for {filename}:")
    # print(parsed_result)
    
    return parsed_result







