# coding: utf-8
 
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk
import string
from functions import research

def rechercher():
    keywords_value = keywords.get()
    nb_doc_value = nb_doc.get()
    author_value = author.get()
    year_value = year.get()
    source_value = source.get()
    lang_value = lang.get()

    if not keywords_value or not nb_doc_value or not source_value:
        messagebox.showerror("Erreur", "Veuillez remplir les champs obligatoires (*)")
        return  
    res, msg = research(keywords_value, nb_max_doc=nb_doc_value, publication_year=year_value, author=author_value, source=source_value, lang=lang_value)
    if res == False:
        messagebox.showerror("Erreur", "Une erreur est survenue. Veuillez rééssayer")
    else:
        messagebox.showinfo("Info", "Vos résultats de recherches sont enregistrés dans le fichier documents.txt")



win = Tk()

win.title('Recherche de documents')


screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
window_width = 400
window_height = 400
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Définir les dimensions et position de la fenêtre
win.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
win.resizable(False, False)

search_doc = Frame(win)
search_doc.pack(padx=10, pady=10)

keywords = StringVar()
nb_doc = IntVar(value=4)
author = StringVar()
year = IntVar(value=2023)
source = StringVar(value="Arxiv")
lang = StringVar(value="Anglais")

Label(search_doc, text="Mots clés à rechercher (séparés par des virgules)*").pack()
Entry(search_doc, textvariable=keywords).pack(fill='x', expand=True)

Label(search_doc, text="Nombre de documents*").pack()
Entry(search_doc, textvariable=nb_doc).pack(fill='x', expand=True)

Label(search_doc, text="Auteur").pack()
Entry(search_doc, textvariable=author).pack(fill='x', expand=True)

Label(search_doc, text="Année de publication").pack()
Entry(search_doc, textvariable=year).pack(fill='x', expand=True)

Label(search_doc, text="Source*").pack()
source_box = ttk.Combobox(search_doc, width = 27, textvariable = source, state="readonly") 
   
source_box['values'] = ('Reddit',  
                          'Arxiv') 
source_box.pack(fill='x', expand=True)

Label(search_doc, text="Langue*").pack()

lang_box = ttk.Combobox(search_doc, width = 27, textvariable = lang, state="readonly") 
   
lang_box['values'] = ('Anglais',  
                          'Français') 
lang_box.pack(fill='x', expand=True)

ttk.Button(search_doc, text="Rechercher", command=rechercher).pack(pady=10)


win.mainloop()

