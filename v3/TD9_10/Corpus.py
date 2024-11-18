from Classes import Author
from decorateurs import singleton
import re
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import csr_matrix
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfTransformer

# =============== 2.7 : CLASSE CORPUS ===============

class Corpus:
    '''_self = None

    def __new__(cls, nom):
        if cls._self is None:
            cls._self = super().__new__(cls)
            cls._self.__init__(nom)
        return cls._self'''
    
    def __init__(self, nom, lang):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = pd.DataFrame(columns=["id", "doc", "doc_text"])
        self.ndoc = 0
        self.naut = 0
        self.concatenated_text = ""
        self.vectorizer = None # on en aura besoin pour la matrice TF_IDF et pour la recherche de similarité
        self.language = lang

    def add(self, doc):
        
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        
        doc_data = pd.Series({"id": self.ndoc, "doc" : doc, "doc_text": doc.texte})

        self.id2doc = pd.concat([self.id2doc, doc_data.to_frame().T], ignore_index=True)
        self.ndoc += 1
        # Ajouter le texte du document à la chaîne concaténée
        self.concatenated_text += doc.texte + " " # contient tous les textes du corpus


    def show_text(self):
        return self.id2doc

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = self.id2doc["doc"].to_list()
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))


    def search(self, keyword):
        results = []

        # Utiliser re.finditer sur la chaîne concaténée
        matches = re.finditer(rf'\b{re.escape(keyword)}\b', self.concatenated_text, flags=re.IGNORECASE)
        for match in matches:
            result = {
                'match_start': match.start(),
                'match_end': match.end(),
                'matched_text': match.group()
            }
            results.append(result)

        return results
    
    # concordance des textes
    def concordance(self, keyword, context_size=50):
        results = []

        # Utilisons re.finditer sur la chaîne concaténée
        matches = re.finditer(rf'\b{re.escape(keyword)}\b', self.concatenated_text, flags=re.IGNORECASE)
        for match in matches:
            start_index = max(0, match.start() - context_size)
            end_index = min(len(self.concatenated_text), match.end() + context_size)

            left_context = self.concatenated_text[start_index:match.start()]
            right_context = self.concatenated_text[match.end():end_index]

            result = {
                'left_context': left_context,
                'matched_text': match.group(),
                'right_context': right_context
            }
            results.append(result)

        df = pd.DataFrame(results, columns=['left_context', 'matched_text', 'right_context'])
        return df
    

    def nettoyer_texte(self, texte):
        
        # Mettre en minuscules et remplacer les retours à la ligne
        cleaned_text = texte.lower().replace('\n', '')
        tokens = cleaned_text.split(" ")

        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        # remove punctuation from each word
        tokens = [re_punc.sub('', w) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]

        stop_words = set(stopwords.words(self.language)) # add option for french too
        tokens = [w for w in tokens if not w in stop_words]
        # tokens = self.remove_stopwords(tokens)
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]
        #tokens = [word.strip() for word in tokens]

        cleaned_text = " ".join(tokens)
        # print(cleaned_text)
        return cleaned_text
    
    def stats(self, n_most_common=20):
        cleaned_text = []
        all_words = []
        words_set = set()

        if "doc_cleaned" not in self.id2doc.columns: # alors les doc ne sont pas nettoyé
            self.clean_all_doc() # procéder au nettoyage
        cleaned_text = self.id2doc["doc_cleaned"].to_list()
        

        # Calculer le nombre de mots différents dans le corpus
        # words = cleaned_text.split()
        
        for doc_cleaned_text in cleaned_text:
            tokens = doc_cleaned_text.split(" ")
            all_words = all_words + tokens # on combine tous les mots de tous les documents
            words_set = words_set.union(set(tokens))
                   

        print(f"Nombre de mots différents dans le corpus : {len(words_set)}")

        # Afficher les n mots les plus fréquents dans tout le corpus
        word_counts = Counter(all_words) # les mots uniques
        most_common_words = word_counts.most_common(n_most_common) # sélections de smots les plus fréquents

        # décommenter pour voir les n mots les plus fréquents du corpus 

        #print(f"\nLes {n_most_common} mots les plus fréquents dans le corpus :")
        #for word, count in most_common_words:
        #    print(f"{word}: {count}")

        # Calculer le document frequency
        
        freq = pd.DataFrame(word_counts.items(), columns=["Mots", "Occurrence"])
        freq = freq.sort_values(by='Occurrence', ascending=False)
        freq = freq.reset_index(drop=True)

        return freq
    


    def construire_vocab(self, freq):
        n_docs = self.id2doc.shape[0]
        n_words = freq.shape[0]
        # print(n_docs, n_words) # shape of vocab
        vocab = pd.DataFrame(np.zeros((n_docs, n_words)), columns=freq['Mots'].values)
        
        for index, doc_cleaned in enumerate(self.id2doc['doc_cleaned']):
            mots = doc_cleaned.split()
            for word in freq['Mots'].values:
                occurrences_mot = mots.count(word)
                # print(index, word, "=", occurrences_mot)
                vocab.at[index, word] = occurrences_mot 
        # print(vocab)
        return vocab # vocabulaire qui contient la fréquence de chaque mots de freq dans chaque documents
                 

#"""""""""""""""""4"""""""""""""""""""""""""""""""
    def construire_matrice_tf_idf(self, freq):
        vectorizer = TfidfVectorizer(vocabulary=freq['Mots'].values)
        mat_TFxIDF = vectorizer.fit_transform(self.id2doc['doc_cleaned'])
        self.vectorizer = vectorizer
        return mat_TFxIDF  # contient pour les mots , leur fréquences dans chaque document


#"""""""""""""Partie 2 : moteur de recherche"""""""""""""

    def moteur_de_recherche(self, keywords, matrice_TFxIDF):
        mots_cles_traites = [mot.lower() for mot in keywords]
        # on tranforme les mots-clés en un vecteur sur le vocabulaire précédemment construit
        vecteur_requete = self.vectorizer.transform([" ".join(mots_cles_traites)])
        # Calculons la similarité cosinus entre le vecteur requête et tous les documents
        similarite = cosine_similarity(vecteur_requete, matrice_TFxIDF).flatten()
        # scores de similarité entre mots clés et docs et affichez les meilleurs résultats par ordre décroissant
        resultats_indices_tries = similarite.argsort()[::-1]
        # Affichage des résultats
        for i, idx in enumerate(resultats_indices_tries):
            print(f"Résultat {i + 1}: Similarité = {similarite[idx]}\n Doc no {idx}")
        return resultats_indices_tries


    '''def remove_stopwords(self, words):
        

        # Liste de stop words génériques en anglais et français
        # ======= améliorer en utilisant la library
        common_stopwords = set([
            "the", "and", "of", "in", "to", "a", "is", "that", "for", "it", "was", "with", "as", "on", "by", "at", "an", "would", "should", "must", "could", "have", "I", "we", "they", "this", "our", "us",
            "le", "la", "de", "du", "et", "en", "à", "un", "une", "est", "que", "pour", "ce", "avec", "sur", "par", "au", "aux", "a", "il", "elle", "ils", "je", "tu"
        ])

        # Supprimer les stop words du texte
        filtered_words = [word for word in words if word.lower() not in common_stopwords]

        return filtered_words'''

    def clean_all_doc(self): # un code pour nettoyer les textes du corpus et les stocker dans la colonne doc_cleaned pour faciliter l'accès
        cleaned_doc = []
        for text in self.id2doc["doc_text"]:
            cleaned_doc.append(self.nettoyer_texte(text))
        
        self.id2doc["doc_cleaned"] = cleaned_doc


    def __repr__(self):
        docs = self.id2doc["doc"].to_list()
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))

