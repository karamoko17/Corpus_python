# coding: utf-8
 
from tkinter import * 
import string

fenetre = Tk()

label = Label(fenetre, text="Recherche de textes")
label.pack()
value = StringVar() 
value.set("texte par défaut")
entree = Entry(fenetre, textvariable=string, width=30)
entree.pack()
bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()


fenetre.mainloop()