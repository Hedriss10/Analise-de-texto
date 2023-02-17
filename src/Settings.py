# Carregamento e configuração das variaveis de ambiente

import os 

from os.path import dirname, join
from dotenv import load_dotenv

#Path 
dotenv_path = join(dirname(dirname(__file__)), '.env')
load_dotenv(dotenv_path)

CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_PASSOWRD = os.environ.get("DATABASE_PASSOWRD")
DATABASE_AGENT = os.environ.get("DATABSE_AGENT")
USERNAME_ID = os.environ.get("USERNAME_ID")