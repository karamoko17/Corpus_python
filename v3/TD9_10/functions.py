import urllib, urllib.request
import xmltodict
import praw
import datetime
from Classes import *
from Corpus import Corpus
import pickle
import os
import re


collection = []
docs_bruts = []
docs = []
err_msg = ""
lang = "en"

def research(keywords, nb_max_doc, author=None, publication_year=None, source="Arxiv", lang="Anglais"):
    keywords_list = keywords_to_list(keywords)
    # mots_cles = keywords_list
    #keywords_list = "+".join(keywords_list)
    limit = int(nb_max_doc)

    if lang == "Anglais":
        lang = "english"
    else:
        lang = "french" # la langue est particulièrement importante pour le traitement des mots du corpus

    reinitialise() 

    if source == "Reddit":
        docs = search_from_reddit(keywords_list=" AND ".join(keywords_list), limit=limit, lang=lang, author=author)
    if source == "Arxiv":
        docs = search_from_arxiv(keywords_list=keywords_list, limit=limit, author=author, year=publication_year) 


    if docs != None:
        docs = list(set(docs)) # suppression des doublons
    

        for i, doc in enumerate(docs):
            print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
            if len(doc)<100:
                docs.remove(doc)

        # longueChaineDeCaracteres = " ".join(docs)
        #print(docs_bruts)

        # =============== PARTIE 2 =============

        # =============== 2.3 : MANIPS ===============


        for nature, doc in docs_bruts:
            if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
                #showDictStruct(doc)

                titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
                try:
                    authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
                except:
                    authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
                summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
                date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime
                author_list = authors.split(", ")
                if len(author_list) > 1:
                # Récupérons les noms des coauteurs (à partir de la deuxième virgule) car le premier correspond au premier auteur
                    coauthors = ", ".join(author_list[1:])
                else:
                    coauthors = ""
                # doc_classe = Document(titre, authors, date, doc["id"], summary)  # Création du Document
                # Adding ArxivDocument
                arxiv_doc = ArxivDocument(title=titre, auteur=authors, date=date, url=doc["id"], texte=summary, co_authors=coauthors)

                collection.append(arxiv_doc)  # Ajout du Document à la liste.

            elif nature == "Reddit":
                #print("".join([f"{k}: {v}\n" for k, v in doc.__dict__.items()]))
                titre = doc.title.replace("\n", '')
                auteur = str(doc.author)
                date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
                url = "https://www.reddit.com/"+doc.permalink
                texte = doc.selftext.replace("\n", "")
                num_comments = int(doc.num_comments)
                # Adding RedditDocument
                reddit_doc = RedditDocument(title=titre, auteur=auteur, date=date, url=url, texte=texte, num_comments=num_comments)
                # doc_classe = Document(titre, auteur, date, url, texte)
                
                collection.append(reddit_doc)


        # =============== 2.4, 2.5 : CLASSE AUTEURS ===============
        from Classes import Author

        # =============== 2.6 : DICT AUTEURS ===============
        authors = {}
        aut2id = {}
        num_auteurs_vus = 0

        # Création de la liste+index des Auteurs
        for doc in collection:
            if doc.auteur not in aut2id:
                num_auteurs_vus += 1
                authors[num_auteurs_vus] = Author(doc.auteur)
                aut2id[doc.auteur] = num_auteurs_vus

            authors[aut2id[doc.auteur]].add(doc.texte)


        corpus = create_corpus(language=lang)
        freq = corpus.stats()
        vocab = corpus.construire_vocab(freq=freq) # creation du vocabulaire à partir de la frequence des mots
        print("======= Vocabulaire =========")
        print(vocab)
        mat_TFxIDF = corpus.construire_matrice_tf_idf(freq=freq) # creation de la matrice tf_idf
        print("======= mat_TFxIDF =========")
        print(mat_TFxIDF)

        ordered_doc = corpus.moteur_de_recherche(keywords=keywords_list, matrice_TFxIDF=mat_TFxIDF)
        # print(ordered_doc)
        retrieve_doc(corpus.id2doc, ordered_doc)
        
        # prochaine étape suppression corpus

        del corpus
        return True, "success"

    else:
        return False, err_msg
    
def retrieve_doc(id2doc, ordered_doc):
        
        documents = id2doc.sort_values(by='id', key=lambda x: x.map({id_: i for i, id_ in enumerate(ordered_doc)})) # re ordonne le dataframe suivant l'ordre de similarite
        with open("documents.txt", "w", encoding="utf-8") as fichier_texte:
            # Itérer sur la colonne "doc" et écrire chaque document dans le fichier
            for index, document in documents.iterrows():
                fichier_texte.write(str(document["doc"]))


def search_from_reddit(keywords_list, limit, author=None, lang="en"):
    
    try:
        reddit = praw.Reddit(client_id='QyizTPZdvFMfbmCtobzj1g', client_secret='TkvCDzi73SAaAge2LDOgEFHb6sF0NA', user_agent='test')
        search_query = f"{keywords_list} language:{lang}"

        if author:
            search_query += f" author:{author}"
        # il n'est pas possible de rechercher exclsivement des posts par date sur reddit
        posts = reddit.subreddit("all").search(search_query, sort='relevance', limit=limit)
        
        # Récupération du texte
        #print(hot_posts)
        docs = []
        afficher_cles = False
        for i, post in enumerate(posts):
            if i%10==0: print("Reddit:", i, "/", limit)
            if afficher_cles:  # Pour connaître les différentes variables et leur contenu
                for k, v in post.__dict__.items():
                    pass
                    print(k, ":", v)

            if post.selftext != "":  # on se passe des posts sans texte
                pass
                #print(post.selftext)
            docs.append(post.selftext.replace("\n", " "))
            docs_bruts.append(("Reddit", post))

        #print(docs)
        return docs
    except Exception as e:
        err_msg = f"Une erreur est survenue. Veuillez rééssayer {e}"
        print(err_msg)
        return None


def search_from_arxiv(keywords_list, limit, author=None, year=None, lang="en"):
    docs = []
    
    try:
         # Requête
        url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(keywords_list)}:{lang}&start=0&max_results={limit}'
        data = urllib.request.urlopen(url)

        # Format dict (OrderedDict)
        data = xmltodict.parse(data.read().decode('utf-8'))

        #showDictStruct(data)

        # Ajout résumés à la liste
        for i, entry in enumerate(data["feed"]["entry"]):
            if i%10==0: print("ArXiv:", i, "/", limit)
            docs.append(entry["summary"].replace("\n", ""))
            docs_bruts.append(("ArXiv", entry))
            #showDictStruct(entry)
        return docs
    except Exception as e:
        err_msg = f"Une erreur est survenue. Veuillez rééssayer {e}"
        print(err_msg)
        return None


def keywords_to_list(keywords):
    # Supprimer tous les caractères spéciaux sauf la virgule
    keywords = re.sub(r'[^a-zA-Z0-9,]', '', keywords)
    keywords_list = keywords.split(",")
    return keywords_list

def create_corpus(name="Mon corpus", language="english") :
    corpus = Corpus(name, language)
    # Construction du corpus à partir des documents
    for doc in collection:
        corpus.add(doc,)
    # corpus.show(tri="abc")
    
    # =============== 2.9 : SAUVEGARDE ===============
    
    
    # Ouverture d'un fichier, puis écriture avec pickle
    with open("corpus.pkl", "wb") as f:
        pickle.dump(corpus, f)

    '''
    mat_TF = corpus.construire_matrice_tf(vocab=freq)

    mat_TFxIDF = corpus.calculer_matrice_TFxIDF(documents=vocab['Mots'])
    # print("=====mat===== ", mat_TFxIDF)

    

    # Supression de la variable "corpus"
    del corpus

    
    '''
    return corpus
    
def read_corpus() :
    # Ouverture du fichier, puis lecture avec pickle
    with open("corpus.pkl", "rb") as f:
        corpus = pickle.load(f)
    
    return corpus

def reinitialise() :
    global collection, docs_bruts, docs, err_msg
    # suppression du documents, résultats des recherches s'il existe 
    if os.path.exists("documents.txt"):
        # Supprimer le fichier
        os.remove("documents.txt")
        print("Le fichier documents.txt a été supprimé.")

    if os.path.exists("corpus.pkl"):
        # Supprimer le fichier pickle
        os.remove("corpus.pkl")
        print("Le fichier corpus.pkl a été supprimé.")
    
    collection = []
    docs_bruts = []
    docs = []
    err_msg = "" 



