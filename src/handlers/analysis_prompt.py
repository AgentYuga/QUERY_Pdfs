# def get_analysis_prompt(job_description, evaluation_criteria, filename, content):
#     return f"""
#     You are an expert in resume analysis. Please carefully review the following resume based on the provided job description and evaluation criteria. 

#     **Job Description:** {job_description}

#     **Evaluation Criteria:**
#     {' '.join([f'{i+1}. {criterion}' for i, criterion in enumerate(evaluation_criteria)])}

#     **Resume Filename:** {filename}
#     **Resume Content:** {content[:4000]}...

#     **Your Tasks:**
#     1. **Identify and Extract:**
#        - **Candidate Name:** Search for common name formats. [Extract the full name from the resume]
#        - **Email:** Search for common email patterns. [Extract the email address from the resume]
#     2. **Evaluate the Resume:**
#        - Assign a score out of 100 for each evaluation criterion based on relevant information from the resume. If information is unclear or missing, infer cautiously and explain the reason.
#        - Provide a detailed, logical explanation for the overall score in 5-6 sentences, referencing how well the resume aligns with the job description and each criterion.
#     3. **Calculate Overall Score:**
#        - The overall score should be a weighted average of the individual criteria scores. Explain how each criterion influenced the final score.
#     4. **Self-Check:**
#        - Before finalizing your response, double-check that all the requested information is correctly identified and that your analysis is logical. If corrections are needed, adjust the output accordingly.
    
#     Ensure that all fields are filled. If the information is not found in the resume, state 'Not found in resume'. Analyze the resume with attention to detail and ensure your explanations are concise and clear.
#     """

def get_analysis_prompt(job_description, evaluation_criteria, filename, content):
    return f"""
    You are an expert in resume analysis. Please carefully review the following resume based on the provided job description and evaluation criteria.

    **Job Description:** {job_description}

    **Evaluation Criteria:**
    {' '.join([f'{i+1}. {criterion}' for i, criterion in enumerate(evaluation_criteria)])}

    **Resume Filename:** {filename}
    **Resume Content:** {content[:4000]}...

    **Your Tasks:**
    1. Identify and Extract:
       - Candidate Name: [Extract the full name from the resume]
       - Email: [Extract the email address from the resume]
    2. Evaluate the Resume:
       - Assign a score out of 100 for each evaluation criterion based on relevant information from the resume.
    3. Calculate Overall Score:
       - Provide the overall score as a weighted average of the individual criteria scores.

    Return the analysis strictly in the following JSON format:

    ```json
    {{
      "name": "[Candidate Name]",
      "email": "[Candidate Email]",
      "overall_score": [Overall Score],
      "scores": {{
        {', '.join([f'"{criterion.lower().replace(" ", "_")}_score": [Score]' for criterion in evaluation_criteria])}
      }},
      "explanation": "[Provide a brief summary of the resume in about 5-6 lines and an explanation for the overall score]"
    }}
    ```

    Ensure the JSON is properly formatted with no additional text outside the JSON block.
    """
