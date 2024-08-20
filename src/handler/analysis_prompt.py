# def get_analysis_prompt(job_description, evaluation_criteria, filename, content):
#     return f"""
#     You are an expert in resume analysis. Please carefully review the following resume based on the provided job description and evaluation criteria.

#     **Job Description:** {job_description}

#     **Evaluation Criteria:**
#     {' '.join([f'{i+1}. {criterion}' for i, criterion in enumerate(evaluation_criteria)])}

#     **Resume Filename:** {filename}
#     **Resume Content:** {content[:4000]}...

#     **Your Tasks:**
#     1. Identify and Extract:
#        - Candidate Name: [Extract the full name from the resume]
#        - Email: [Extract the email address from the resume]
#     2. Evaluate the Resume:
#        - Assign a score out of 100 for each evaluation criterion based on relevant information from the resume.
#     3. Calculate Overall Score:
#        - Provide the overall score as a weighted average of the individual criteria scores.

#     Return the analysis strictly in the following JSON format:

#     ```json
#     {{
#       "name": "[Candidate Name]",
#       "email": "[Candidate Email]",
#       "overall_score": [Overall Score],
#       "scores": {{
#         {', '.join([f'"{criterion.lower().replace(" ", "_")}_score": [Score]' for criterion in evaluation_criteria])}
#       }},
#       "explanation": "[Provide a brief summary of the resume in about 5-6 lines and an explanation for the overall score]"
#     }}
#     ```

#     Ensure the JSON is properly formatted with no additional text outside the JSON block.
#     """
# ------------------------------------------------------------------------------------------------------------------------------------------

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

      -  For each evaluation criterion, assign a score out of 100 based on relevant information found in the resume.
            Duration of Employment or Experience:

            Employment Dates:
            Identify employment dates for each job experience or work experience or company, which may appear in various formats (e.g., "May 2019 - March 2023" or "2015-2018").
            If specific durations (e.g., "3 years") are stated, use those directly.
            Otherwise, calculate the duration based on the start and end dates.

            Average Tenure:
            Calculate the total duration of employment by summing the durations of all listed jobs or work experience or job experience.
            Divide the total duration by the number of companies or jobs to determine the average tenure.

            Total Experience or Minimum Experience:
            Use the explicitly mentioned total experience in the resume if available.
            If not mentioned, sum up the durations of all listed work experiences to estimate total experience.

            Scoring:

               For Average Tenure:
               Score 100 if the calculated average tenure meets or exceeds the requirement (e.g., "2 years average tenure").
               Score 90 if the average tenure is within 10% less than the requirement.
               Assign lower scores proportionally for values significantly below the requirement.

               For Minimum Experience:
               Score 100 if the total experience meets or exceeds the requirement (e.g., "3 years minimum experience").
               Score 90 if the experience is within 10% less than the requirement.
               Assign lower scores proportionally for values significantly below the requirement.

            Other Criteria:

            Use your expertise to assign appropriate scores for other criteria not related to employment duration or experience. Consider factors such as skills, certifications, education, and relevant achievements mentioned in the resume.

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
      "explanation": "[Provide a brief summary of the resume in about 6-8 lines and an explanation for the overall score and each criterion scores]"
    }}
    ```

    Ensure the JSON is properly formatted with no additional text outside the JSON block.
    """