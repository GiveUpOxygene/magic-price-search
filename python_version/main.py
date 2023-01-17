import googlesearch as gr
import requests as r
import re
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from bs4 import BeautifulSoup as BS

class Card:
    def __init__(self, name = None, url = None):
        self.url = url
        self.url = self.get_url(name)
        self.name = self.get_name()
        self.filename = ""
        self.info_tab = self.get_info()
        
    def get_url(self, name):
        if name == None:
            print("No name")
            return None
        for my_url in gr.search("site:https://boutique.magiccorporation.com/ " + name, num = 1, stop = 1):
            self.url = my_url
        return self.url
        
    def get_name(self):
        '''Gets the name of the card from the url'''
        if self.url == None:
            print("No url")
            return None
        # TODO : get the name of the card with some good code and not this clusterfuck
        self.name = ' '.join(self.url.split('/')[-1].split('-')[3:]).replace('-', ' ').replace('.html', '')
        return self.name

    
    def get_info(self, debug = False):
        '''
        Récupère les informations d'achat
        
        Renvoie un dictionnaire contenant les informations sur les différentes éditions de la carte
        et leur prix
        ----------
        Parameters
        ----------
        self : Card
            La carte dont on veut récupérer les informations
        debug : bool
            Si True, affiche les informations récupérées au cours du parsing
            
        ----------
        Returns
        ----------
        dico : dict
            {edition : (prix, quantité, condition)}
        '''
        # initialisation de variables
        edition = []
        quantity = []
        condition = []
        price = []
        # vérification de l'url
        if self.url != None:
            req = r.get(self.url, 'html.parser')
        
        self.filename = self.name.replace(' ', '_') + '.html'
        with open(f"./cards/{self.filename}", 'w', encoding="utf8") as f:
            f.write(req.text)
        with open(f"./cards/{self.filename}", 'r', encoding="utf8") as f:
            text = f.read()

        # parsing du code html
        soup = BS(text,"lxml")
        for p in soup.find_all('div'):
            if p.get('class') == ['dispo']:
                for p3 in p.find_all('td'):
                    if p3.get_text() != "" :
                        if p3.find('select') != None:
                            if debug:
                                print("Quantité : " + p3.get_text()[-1])
                            quantity.append(p3.get_text()[-1])
                        elif p3.get('style') == None:
                            if p3.find('img') != None:
                                if debug:
                                    print("Edition : " + p3.get_text())
                                edition.append(p3.get_text())
                            else:
                                if debug:
                                    print("Condition : " + p3.get_text())
                                condition.append(p3.get_text())
                        else:
                            if debug:
                                print("Prix : " + p3.get_text())
                            price.append(p3.get_text())
                            
        dico = {x:y for x,y in zip(edition, zip(price, quantity, condition))}
        self.info_tab = dico
        if debug == False:
            os.remove(f"./cards/{self.filename}")
        return dico

    
    def debug_info(self):
        print("Name : " + self.name)
        print("Url : " + str(self.url))
        print("Price : " + str(self.info_tab))
        
        
class Deck:
    def __init__(self, name, card_list_file = None, url = None, deck_type = "Commander"):
        self.name = name
        self.url = url
        self.deck_price = 0
        self.card_number = []
        if self.url == None:
            self.get_url()
        self.deck_type = deck_type
        if card_list_file != None:
            self.card_list = self.read_card_list(card_list_file)
    
    def get_url(self):
        query = "deck commander " + self.name.lower() + " play in magic bazar"
        for url in gr.search(query, num = 1, stop = 1):
            self.url = url
        print(url)
    
    def read_card_list(self, card_list):
        #lit le fichier card_list et retourne une liste de cartes sous forme de dictionnaire
        #contenant les noms des cartes et leur nombre
        card_dict = {}
        with open(card_list, 'r') as f:
            for line in f.readlines:
                values = line.split(":")
                card_dict[values[0]] = int(values[1])
        return card_dict
    
    def get_card_list(self):
        #récupère la liste depuis internet
        query = "deck commander " + self.name.lower() + " play in magic bazar"
        for url in gr.search(query, tld="co.in", num=1, stop=1, pause=2):
            req = r.get(url, 'html.parser')
            occurs = re.compile('/api/[0-9a-zA-Z.?=]*').findall(req.text)
            deck_list_url ='https://www.play-in.com' + occurs[0]
            req_deck_list = r.get(deck_list_url, 'html.parser')
            occurs_deck_list = re.compile("(?P<name>\/magic\/carte\/[0-9a-zA-Z,'\- éèàêëîœÀÉÈÇŒÎ]*)").findall(req_deck_list.text)
            occurs_deck_number = re.compile("\<td\>\<span\>(?P<number>[0-9]{1-2}) x\</span\>").findall(req_deck_list.text)
            print(occurs_deck_number)
        self.card_list = occurs_deck_list
        self.card_number = occurs_deck_number



# ---Main---


def main():
    # app = QApplication([])
    # window = QWidget()
    # window.setGeometry(300, 300, 500, 500)
    # window.setWindowTitle("Magic Card Price")
    
    # label = QLabel(window)
    # label.setText("Hello World")
    # label.setFont(QFont("Arial", 20))
    
    # layout = QVBoxLayout()
    
    # label = QLabel("Press Button")
    # button = QPushButton("Click Me")
    
    # window.show()
    # app.exec_()
    my_card = Card("galea embraseuse d'espoir")
    my_card.debug_info()
    
    
if __name__ == "__main__":
    main()
