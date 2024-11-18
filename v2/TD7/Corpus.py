# Correction de G. Poux-Médard, 2021-2022

from Classes import Author
from decorateurs import singleton
import re
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import csr_matrix
import nltk
nltk.download('stopwords')
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
    
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.concatenated_text = ""

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

        # Ajouter le texte du document à la chaîne concaténée
        self.concatenated_text += doc.texte + " "

# =============== 2.8 : REPRESENTATION ===============
    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
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
    
    def concordance(self, keyword, context_size=50):
        results = []

        # Utiliser re.finditer sur la chaîne concaténée
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

        # Créer un DataFrame pandas à partir des résultats
        df = pd.DataFrame(results, columns=['left_context', 'matched_text', 'right_context'])
        return df
    

    def nettoyer_texte(self, texte):
        
        # Mettre en minuscules et remplacer les retours à la ligne
        cleaned_text = texte.lower().replace('\n', '')
        tokens = cleaned_text.split()
        # print(tokens)
        # Remplacer la ponctuation et les chiffres par des espaces
        # cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)

        # Supprimer les chiffres
        # cleaned_text = re.sub(r'\d', '', cleaned_text)

        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        # remove punctuation from each word
        tokens = [re_punc.sub('', w) for w in tokens]
        # remove remaining tokens that are not alphabetic
        tokens = [word for word in tokens if word.isalpha()]

        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        # filter out short tokens
        tokens = [word for word in tokens if len(word) > 1]

        return tokens
    
    def stats(self, n_most_common=10):
        tokens = self.nettoyer_texte(self.concatenated_text)

        # Calculer le nombre de mots différents dans le corpus
        # words = cleaned_text.split()
        unique_words_count = len(set(tokens))        

        # print(f"Nombre de mots différents dans le corpus : {unique_words_count}")

        # Afficher les n mots les plus fréquents
        word_counts = Counter(tokens)
        most_common_words = word_counts.most_common(n_most_common)


        # print(f"\nLes {n_most_common} mots les plus fréquents dans le corpus :")
        # for word, count in most_common_words:
           #  print(f"{word}: {count}")

         # Calculer le document frequency
        
        # ================== a revoir
        freq = pd.DataFrame(word_counts.items(), columns=["Mots", "Occurrence"])
        freq = freq.sort_values(by='Mots', ascending=True)
        
        

        return freq
    
    def construire_vocab(self, freq):
        document_frequency = Counter()
        for doc in self.id2doc.values():
            mots_du_document = set(self.nettoyer_texte(doc.texte))
            document_frequency.update(mots_du_document)

        # Ajouter une colonne au DataFrame représentant le document frequency de chaque mot
        freq['Document_Frequency'] = freq['Mots'].apply(lambda x: document_frequency[x])
        
        return freq

#"""""""""""""""""2"""""""""""""""""""""""""""""""
    def construire_matrice_tf(self, vocab):

        # Initialiser le vectoriseur CountVectorizer
        vectoriseur = CountVectorizer()

        # Appliquer le vectoriseur sur les textes pour construire la matrice de Term Frequency (TF)
        X = vectoriseur.fit_transform(vocab)
        
        # Conversion de la matrice creuse en sparse.csr_matrix
        mat_TF = csr_matrix(X)

        return mat_TF



#"""""""""""""""""4"""""""""""""""""""""""""""""""
    def calculer_matrice_TFxIDF(self, documents):
  
        # Création d'une instance de CountVectorizer pour extraire les termes-fréquence
        tfidf_vectorizer = TfidfVectorizer()
        mat_TFxIDF = tfidf_vectorizer.fit_transform(documents)
        # print(tfidf_vectorizer.get_feature_names_out())
        print(mat_TFxIDF.shape)
        return mat_TFxIDF

#"""""""""""""Partie 2 : moteur de recherche"""""""""""""

    def moteur_de_recherche(mots_cles, matrice_TFxIDF, documents):
        # Prétraitement des mots-clés
        mots_cles_traites = [mot.lower() for mot in mots_cles]

        # Transformez les mots-clés en un vecteur sur le vocabulaire précédemment construit
        '''vecteur_requete = vectorizer.transform([" ".join(mots_cles_traites)])

        # Calculez la similarité cosinus entre le vecteur requête et tous les documents
        similarite = cosine_similarity(vecteur_requete, matrice_TFxIDF).flatten()

        # Triez les scores de similarité et affichez les meilleurs résultats
        resultats_indices_tries = similarite.argsort()[::-1]

        # Affichage des résultats
        for i, idx in enumerate(resultats_indices_tries):
            print(f"Résultat {i + 1}: Similarité = {similarite[idx]}, Document : {documents[idx]}")

        # Exemple d'utilisation avec des mots-clés saisis par l'utilisateur
        mots_cles_utilisateur = input("Entrez quelques mots-clés : ").split()
        moteur_de_recherche(mots_cles_utilisateur, matrice_TFxIDF_resultante, documents)'''




def __repr__(self):
    docs = list(self.id2doc.values())
    docs = list(sorted(docs, key=lambda x: x.titre.lower()))

    return "\n".join(list(map(str, docs)))

