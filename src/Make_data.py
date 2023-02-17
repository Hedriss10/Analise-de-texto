import praw
import re
import config


# load env
from Settings import CLIENT_ID, SECRET_KEY, DATABASE_PASSOWRD
from Settings import DATABASE_AGENT, USERNAME_ID


# Carregamento de dados
# Listar de temas que usaremos para buscar no Reddit
# Essas serão as classes que usaremos no target
assuntos = ['datascience', 'machinelearning', 'physics', 'astrology', 'conspiracy']




# Função para carregar os dados
def load_data():

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


load_data()