# Correction de G. Poux-Médard, 2021-2022

# =============== 2.1 : La classe Document ===============
class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

# =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}\nSource: {self.getType()}"
    
    def getType(self):
        pass



# =============== 2.4 : La classe Author ===============
class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
# =============== 2.5 : ADD ===============
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"
    

    #Partie 1 : classe RedditDocument

class RedditDocument(Document):
    def __init__(self, title, num_comments, auteur, date, url, texte, document_type="Reddit"):
        super().__init__(title, auteur, date, url, texte)
        self.__num_comments = num_comments
        self.document_type=document_type
        

    def get_num_comments(self):
        return self.__num_comments

    def set_num_comments(self, num_comments):
        self.__num_comments = num_comments

    def __str__(self):
        return f"{super().__str__()}\nNumber of Comments: {self.__num_comments}"
    
    def getType(self):
        return self.document_type


#Partie 2 : classe ArxivDocument

class ArxivDocument(Document):
    def __init__(self, title, auteur, date, url, texte, co_authors=[], document_type="Arxiv"):
        super().__init__(title, auteur, date, url, texte)
        self.__co_authors = co_authors
        self.document_type=document_type

    def get_co_authors(self):
        return self.__co_authors

    def set_co_authors(self, co_authors):
        self.__co_authors = co_authors

    def add_co_author(self, co_author):
        self.__co_authors.append(co_author)

    def remove_co_author(self, co_author):
        if co_author in self.__co_authors:
            self.__co_authors.remove(co_author)

    def __str__(self):
        co_authors_str = ", ".join(self.__co_authors)
        return f"{super().__str__()}\nCo-authors: {co_authors_str}"
    
    def getType(self):
        return self.document_type


