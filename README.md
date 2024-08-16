# Project title : Query and Summarize PDFs

# Overview:
The Query and Summarize PDFs project utilizes OpenAI and Anthropic to summarize and evaluate PDF files in a specified folder. The project is implemented in Python and leverages a Streamlit app for user interaction

# Features
    1. Summarizes and evaluates PDFs based on provided criteria.
    2. Uses OpenAI and Anthropic APIs for analysis.
    3. Generates a downloadable CSV file with the evaluation results.

# Requirements
    1. Python 3.10
    2. OpenAI API Key
    3. Anthropic API Key

# Installation
    1. Clone the repository:
        git clone https://github.com/AgentYuga/QUERY_Pdfs.git
        cd Query_Pdfs
    2. Create a virtual environment:
        conda create -p venv python==3.10 -y
        conda activate.bat venv/
    3. Install the required dependencies:
        pip install -r requirements.txt
    4. Set up your API keys in the `src/config/.env` file:
        OPENAI_API_KEY=""
        ANTHROPIC_API_KEY=""
# Running the app
    1. Navigate to the root folder of the Project
    2. Run the streamlit app : streamlit run src/app/app.py
    3. Follow the instructions in the app to input:
        Job description
        Criteria for resume evaluation
        LLM model to analyze the resumes
        Path to the resume/PDF folder
The output will be a downloadable CSV file containing the evaluation results.

License
This project is licensed under the MIT License. See the LICENSE file for details.
