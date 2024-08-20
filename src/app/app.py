import sys
import os

# Ensure the src directory is in the path for module imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

import streamlit as st
import pandas as pd
from handler.pdf_utils import get_resume_files, load_single_resume
from resume_analyzer.analyzer import analyze_resume
from handler.env_vars import load_env_vars

def main():
    load_env_vars()
    
    st.title("HR Resume Matcher")
    
    job_description = st.text_area("Job Description", height=150)
    
    st.subheader("Evaluation Criteria")
    num_criteria = st.number_input("Number of evaluation criteria", min_value=1, value=1)
    evaluation_criteria = []
    for i in range(num_criteria):
        criterion = st.text_input(f"Criterion {i+1}")
        evaluation_criteria.append(criterion)

    model_choice = st.selectbox("Choose Model", [
        "OpenAI GPT-4o", "OpenAI GPT-4", "OpenAI GPT-3.5 Turbo",
        "Anthropic claude-3-5-sonnet-20240620",
        'Llama 3.1'
    ])
    
    resume_folder = st.text_input("Resume Folder Path")

    if st.button("Analyze Resumes"):
        if job_description and evaluation_criteria and resume_folder:
            resume_files = get_resume_files(resume_folder)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for i, filename in enumerate(resume_files):
                status_text.text(f"Analyzing resume {i+1} of {len(resume_files)}")
                filename, content = load_single_resume(resume_folder, filename)
                result = analyze_resume(job_description, evaluation_criteria, filename, content, model_choice)
                results.append(result)
                progress_bar.progress((i + 1) / len(resume_files))
            
            df = pd.DataFrame(results)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="resume_analysis.csv",
                mime="text/csv",
            )
        else:
            st.warning("Please fill in all required fields.")

if __name__ == "__main__":
    main()