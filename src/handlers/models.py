import os
from handlers.env_vars import load_env_vars
from openai import OpenAI
from anthropic import Anthropic
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_env_vars()

def openai_client():
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def anthropic_client():
    return Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def groq_client():
    return ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY'), model_name="Llama3-8b-8192")

def openai_model(model_choice, prompt):
    client = openai_client()
    model = {
        "OpenAI GPT-3.5": "gpt-3.5-turbo",
        "OpenAI GPT-4": "gpt-4",
        "OpenAI GPT-4o": "gpt-4o"
    }.get(model_choice)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an HR assistant analyzing resumes."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def anthropic_model(model_choice,prompt):
    client = anthropic_client()
    model = {
        "Anthropic claude-3-5-sonnet-20240620":"claude-3-5-sonnet-20240620",
        "Anthropic claude-3-opus-20240229":"claude-3-opus-20240229"
    }.get(model_choice)
    response = client.messages.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7
    )
    return response.content[0].text.strip()

def groq_model(prompt):
    chat = groq_client()
    system = "You are an HR assistant analyzing resumes."
    human = "{text}"

    prompt_template = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    chain = prompt_template | chat
    response = chain.invoke({"text": prompt})
    return response.content.strip()
