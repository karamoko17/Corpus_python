from Document import Document

#Partie 1 : classe RedditDocument

class RedditDocument(Document):
    def __init__(self, title, num_comments, auteur, date, url, texte):
        super().__init__(title, auteur, date, url, texte, document_type="Reddit")
        self.__num_comments = num_comments
        

    def get_num_comments(self):
        return self.__num_comments

    def set_num_comments(self, num_comments):
        self.__num_comments = num_comments

    def __str__(self):
        return f"{super().__str__()}\nNumber of Comments: {self.__num_comments}"

# Exemple d'utilisation
reddit_doc = RedditDocument("Title of Reddit Post", "Content of Reddit Post", 20)
print(reddit_doc)

#Partie 2 : classe ArxivDocument

class ArxivDocument(Document):
    def __init__(self, title, auteur, date, url, texte, co_authors=[]):
        super().__init__(title, auteur, date, url, texte, document_type="Arxiv")
        self.__co_authors = co_authors

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


# Exemple d'utilisation
arxiv_doc = ArxivDocument("Title of Arxiv Paper", "Content of Arxiv Paper", ["Author1", "Author2"])
arxiv_doc.add_co_author("Author3")
print(arxiv_doc)


#Partie 3 : mise `a jour de la classe Corpus

#test corpus

class Corpus:
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def display_documents(self):
        for document in self.documents:
            print(document)
            print("-" * 30)


# Création d'objets RedditDocument et ArxivDocument
reddit_doc = RedditDocument("Title of Reddit Post", "Content of Reddit Post", 20)
arxiv_doc = ArxivDocument("Title of Arxiv Paper", "Content of Arxiv Paper", ["Author1", "Author2"])

# Création d'un objet Corpus et ajout des documents
corpus = Corpus()
corpus.add_document(reddit_doc)
corpus.add_document(arxiv_doc)

# Affichage des documents dans le corpus
corpus.display_documents()

#Partie 4 : Patrons de conception

#4.1

class CorpusSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CorpusSingleton, cls).__new__(cls)
            cls._instance.documents = []
        return cls._instance

    def add_document(self, document):
        self.documents.append(document)

    def display_documents(self):
        for document in self.documents:
            print(document)
            print("-" * 30)


# Exemple d'utilisation avec Singleton
corpus_singleton1 = CorpusSingleton()
reddit_doc = RedditDocument("Title of Reddit Post", "Content of Reddit Post", 20)
corpus_singleton1.add_document(reddit_doc)

corpus_singleton2 = CorpusSingleton()  # Cela renvoie la même instance que corpus_singleton1

arxiv_doc = ArxivDocument("Title of Arxiv Paper", "Content of Arxiv Paper", ["Author1", "Author2"])
corpus_singleton2.add_document(arxiv_doc)

# Les deux instances partagent le même corpus
corpus_singleton1.display_documents()
corpus_singleton2.display_documents()

#4.2

from abc import ABC, abstractmethod


# Produit abstrait
class Document(ABC):
    @abstractmethod
    def __str__(self):
        pass

# Produits concrets
class RedditDocument(Document):
    def __init__(self, title, content, num_comments):
        self.title = title
        self.content = content
        self.num_comments = num_comments

    def __str__(self):
        return f"Type: Reddit\nTitle: {self.title}\nContent: {self.content}\nNumber of Comments: {self.num_comments}"


class ArxivDocument(Document):
    def __init__(self, title, content, co_authors=[]):
        self.title = title
        self.content = content
        self.co_authors = co_authors

    def __str__(self):
        co_authors_str = ", ".join(self.co_authors)
        return f"Type: Arxiv\nTitle: {self.title}\nContent: {self.content}\nCo-authors: {co_authors_str}"

# Fabrique abstraite
class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self):
        pass

# Fabriques concrètes
class RedditDocumentFactory(DocumentFactory):
    def create_document(self, title, content, num_comments):
        return RedditDocument(title, content, num_comments)

class ArxivDocumentFactory(DocumentFactory):
    def create_document(self, title, content, co_authors=[]):
        return ArxivDocument(title, content, co_authors)

# Exemple d'utilisation
reddit_factory = RedditDocumentFactory()
arxiv_factory = ArxivDocumentFactory()

reddit_doc = reddit_factory.create_document("Title of Reddit Post", "Content of Reddit Post", 20)
arxiv_doc = arxiv_factory.create_document("Title of Arxiv Paper", "Content of Arxiv Paper", ["Author1", "Author2"])

print(reddit_doc)
print("-" * 30)
print(arxiv_doc)

#Partie 5 : Interface notebook

#5.1

def main():
    # Utilisons votre programme ici

    # Exemple d'utilisation
    reddit_factory = RedditDocumentFactory()
    arxiv_factory = ArxivDocumentFactory()

    reddit_doc = reddit_factory.create_document("Title of Reddit Post", "Content of Reddit Post", 20)
    arxiv_doc = arxiv_factory.create_document("Title of Arxiv Paper", "Content of Arxiv Paper", ["Author1", "Author2"])

    corpus = Corpus()
    corpus.add_document(reddit_doc)
    corpus.add_document(arxiv_doc)

    corpus.display_documents()

if __name__ == "__main__":
    main()

#5.2


import ipywidgets as widgets
from IPython.display import display

# Définissons une fonction pour traiter les paramètres saisis par l'utilisateur
def process_parameters(keyword, num_articles):
    # Utilisons les valeurs pour configurer votre application
    print(f"Keyword: {keyword}")
    print(f"Number of Articles: {num_articles}")


# Créons des widgets pour le formulaire
keyword_input = widgets.Text(value='python', description='Keyword:')
num_articles_input = widgets.IntSlider(value=10, min=1, max=100, step=1, description='Number of Articles:')

# Créons un bouton pour soumettre le formulaire
submit_button = widgets.Button(description='Submit')

# Définissons une fonction pour être appelée lors du clic sur le bouton
def on_submit_button_click(b):
    process_parameters(keyword_input.value, num_articles_input.value)

# Associons la fonction de clic au bouton
submit_button.on_click(on_submit_button_click)

# Affichons le formulaire
display(keyword_input, num_articles_input, submit_button)
