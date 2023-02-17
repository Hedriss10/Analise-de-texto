import re
import praw
import config
import numpy as np 
import matplotlib as plt 
import seaborn as sns 

# load the iA
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

#load env 
from Settings import CLIENT_ID, SECRET_KEY, DATABASE_AGENT
from Settings import DATABASE_AGENT, USERNAME_ID




# load env
from Settings import CLIENT_ID, SECRET_KEY, DATABASE_PASSOWRD
from Settings import DATABASE_AGENT, USERNAME_ID


# Carregamento de dados
# Listar de temas que usaremos para buscar no Reddit
# Essas serão as classes que usaremos no target
assuntos = ['datascience', 'machinelearning', 'physics', 'astrology', 'conspiracy']


# Função para carregar os dados
def load_data():
    global data 
    global labels
    # Primeiro extraimos os dados do reddit acessando via API
    api_reddit = praw.Reddit(client_id=CLIENT_ID,
                             client_secret=SECRET_KEY,
                             password=DATABASE_PASSOWRD,
                             user_agent=DATABASE_AGENT,
                             username=USERNAME_ID)

    # Contando o número de carectres usando expressão regulares

    def char_count(post): return len(re.sub("\W|\d", '', post.selftext))
    """Condit,
    Definimos a condição para filtrar os posts(retornaremos somentes os posts com 100 ou mais carecateres..)
    """
    def mask(post): return char_count(post) >= 100

    # Lista para resultados
    data = []
    labels = []

    # lop
    for i, assunto in enumerate(assuntos):

        # Extrair posts
        subreddit_data = api_reddit.subreddit(assunto).new(limit=1000)

        # Filtrar os posts que não satisfazem nossa condição
        posts = [post.selftext for post in filter(mask, subreddit_data)]

        # Adicionar o posts e labels as listas
        data.append(posts)
        labels.extend([i] * len(posts))

        # Print
        print(f'Número de posts com assuntos r/{assunto}:{len(posts)}',
              f'\nUm dos posts extraídos: {posts[0][:600]}...\n', "-" * 80 + '\n')

    return data, labels



TESTE_SIZE = .2
RANDOM_STATE = 0

def split_data():
    
    print(f'Split {100 * TESTE_SIZE}% dos dados para teste e avaliação do modelo')
    
    #Split dos dados 
    
    X_treino, X_test, y_treino, y_test = train_test_split(data,
                                                          labels,
                                                          test_size=TESTE_SIZE, 
                                                          random_state=RANDOM_STATE)
    
    
    print(f'{len(y_test)} Amostragem dos testes.')
    
    
    return X_treino, X_test, y_test, y_treino


## Pré-Processamento de Dados e Extração de Atributos

# - Remove símbolos, números e strings semelhantes a url com pré-processador personalizado
# - Vetoriza texto usando o termo frequência inversa de frequência de documento
# - Reduz para valores principais usando decomposição de valor singular
# - Particiona dados e rótulos em conjuntos de treinamento / validação


#Variaveis de controle 
MIN_DOC_FRQUEC = 1
N_COMPONENTES = 1000
N_ITER = 30


#Função para pipeline de pré-processamento 
def preprocessing_pipeline():
    
    #Removendo caracteres não "alfabeticos"
    patter = r'\W|d|http.*\s|www.*\s+'
    preprocessor =  lambda text: re.sub(patter, ' ', text)