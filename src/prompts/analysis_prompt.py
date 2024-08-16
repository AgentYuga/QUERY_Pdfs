def get_analysis_prompt(job_description, evaluation_criteria, filename, content):
    return f"""
    Analyze the following resume based on this job description and evaluation criteria:

    Job Description: {job_description}

    Evaluation Criteria:
    {' '.join([f'{i+1}. {criterion}' for i, criterion in enumerate(evaluation_criteria)])}

    Resume Filename: {filename}
    Resume Content: {content[:4000]}...

    Provide the following information in a structured format:
    1. Candidate Name: [Extract the full name from the resume]
    2. Email: [Extract the email address from the resume]
    3. Overall Score: [Provide a score out of 100]
    4. Scores for each evaluation criterion:
       {' '.join([f'- {criterion}: [Score out of 100]' for criterion in evaluation_criteria])}
    5. Brief explanation: [Explain the overall score in max 50 words]

    Ensure all fields are filled. If information is not available, state 'Not found in resume'.
    """