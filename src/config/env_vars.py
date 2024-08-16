import os
from dotenv import load_dotenv

def load_env_vars():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)