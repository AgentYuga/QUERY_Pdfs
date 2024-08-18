# import os
# from dotenv import load_dotenv

# def load_env_vars():
#     env_path = os.path.join(os.path.dirname(__file__), '.env')
#     load_dotenv(env_path)

import os
from dotenv import load_dotenv

def load_env_vars():
    handler_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(handler_dir, '.env')
    load_dotenv(env_path)