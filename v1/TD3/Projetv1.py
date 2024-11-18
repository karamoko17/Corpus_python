import praw 
import pandas as pd
import urllib.request
import xmltodict
import matplotlib.pyplot as plt

reddit = praw.Reddit(client_id='cUy4n6lGXvtlL6L2x1B_eg', client_secret='-GMewaLO4k59tqNMiSQDBFVlVQc84Q', user_agent='Mon Application')

#Partie 1 : chargement des donnees
#1.1)

# get 10 hot posts from the MachineLearning subreddit
hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
#print(hot_posts)

#nous avons les champs suivants: 'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'
#le champs qui contient le contenu textuel est :Title

"""for post in hot_posts:
 print(post.title)
    

# get hottest posts from all subreddits
hot_posts = reddit.subreddit('all').hot(limit=10)
for post in hot_posts:
    print(post.title)

    
docs = []
ml_subreddit = reddit.subreddit('MachineLearning')
for post in ml_subreddit.hot(limit=10):
    content = post.selftext.replace('\n', ' ')
    docs.append(content)
 
for doc in docs:
    print(doc)
"""
docs = []

#1.2)



base_url = 'http://export.arxiv.org/api/query?'
search_query = 'search_query=cat:cs.CV&start=0&max_results=10'
url = base_url + search_query

response = urllib.request.urlopen(url)
data = response.read()



arxiv_data = xmltodict.parse(data)

# Accédez aux résultats des articles
articles = arxiv_data['feed']['entry']

for article in articles:
    title = article['title']
    summary = article['summary']
    # Ajoutez le titre et le résumé à la liste docs
    docs.append(f"Titre : {title}\nRésumé : {summary}\n")


#print(docs)


#Partie 2 : sauvegarde des donnees

#2,1


# Créez une liste de dictionnaires en utilisant une boucle
data = []
origine = []
for origines in docs:
        if "Reddit" in origines:
            origine.append("Reddit")
        else:
            origine.append("Arxiv")
            
for i in range(len(docs)):
        entree = {'Id':  i + 1 , 
                'Texte': docs[i], 
                'origine':origine[i]
                }
        data.append(entree)


"""# Affichez la liste de dictionnaires
for entree in data:
    print(entree)
    
"""   

df = pd.DataFrame(data)
df_replace = df.replace('\n', ' ',regex=True)
# print(df_replace)
 
#2,2


nom_fichier = 'MyData.csv'

# Sauvegarder le DataFrame dans un fichier CSV en utilisant la tabulation comme séparateur
df_sauv = df_replace.to_csv(nom_fichier, sep='\t', index=False)


#2,3

# Charger le fichier CSV en mémoire
df_memoire = pd.read_csv(nom_fichier, sep='\t')

#Partie 3 : premieres manipulation des donnees


#3,1

nombre_de_documents = df_memoire.shape[0]
#print("Le corpus contient", nombre_de_documents, "documents.")

#3,2

# Fonction pour compter les mots dans un texte
def compter_mots(texte):
    mots = texte.split()  # Sépare le texte en mots en utilisant les espaces comme séparateur
    return len(mots)

# Fonction pour compter les phrases dans un texte
def compter_phrases(texte):
    phrases = texte.split('.')  # Sépare le texte en phrases en utilisant le point comme séparateur
    return len(phrases)

# Ajouter deux nouvelles colonnes au DataFrame pour le nombre de mots et de phrases
df_memoire['Nombre de Mots'] = df_memoire['Texte'].apply(compter_mots)
df_memoire['Nombre de Phrases'] = df_memoire['Texte'].apply(compter_phrases)

#print(df_memoire)

#3,3


# Filtrer les documents qui contiennent moins de 20 caractères
df_memoire1 = df_memoire[df_memoire['Texte'].str.len() >= 20]

# Réinitialiser l'index du DataFrame
df_memoire1.reset_index(drop=True, inplace=True)

#print(df_memoire)

#3,4

# Créer une liste pour stocker les textes de chaque document
textes = df_memoire['Texte'].tolist()

corpus = '\n'.join(textes) # Ajoute un saut de ligne entre chaque document

# Afficher la taille du corpus (nombre de caractères)
taille_corpus = len(corpus)

#print("La taille du corpus est de", taille_corpus, "caractères.")