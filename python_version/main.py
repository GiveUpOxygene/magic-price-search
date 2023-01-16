import googlesearch as gr
import requests as r
import re
import numpy as np
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from bs4 import BeautifulSoup as BS

class Card:
    def __init__(self, name = None, url = None):
        self.url = url
        self.url = self.get_url(name)   
        self.name = self.get_name()
        self.price_tab = None
        self.price_tab = self.get_price_tab()
        
    def get_url(self, name):
        if name == None:
            print("No name")
            return None
        for my_url in gr.search("site:https://boutique.magiccorporation.com/ " + name, num = 1, stop = 1):
            self.url = my_url
        return self.url
        
    def get_name(self):
        if self.url == None:
            print("No url")
            return None
        # TODO : get the name of the card with some good code and not this clusterfuck
        self.name = ' '.join(self.url.split('/')[-1].split('-')[3:]).replace('-', ' ').replace('.html', '')
        return self.name
    
    # def get_price(self):
    #     if self.name in "Montagne Île Plaine Forêt Marais" :
    #         return 0.25
    #     if self.url != None:
    #         req = r.get(self.url, 'html.parser')
    #         occurs = re.compile('images/magic/editions/sigles/(?P<edition>.+)/').findall(req.text)
    #         occurs2 = re.compile('[0-9]+[.][0-9]+ €').findall(req.text)
    #         dico = {x:y for x,y in zip(occurs, occurs2)}
    #         if (occurs == []):
    #             price = "No price"
    #         else:
    #             price = float(occurs[0].replace(' €', ''))
    #         print(self.name + " : " + str(price))
    #     return price
        
    def get_price_tab(self):
        if self.name in "Montagne Île Plaine Forêt Marais" :
            return 0.25
        if self.url != None:
            req = r.get(self.url, 'html.parser')
            #create new file called card.html and write the html code of the card
            with open("card.html", 'w', encoding="utf8") as f:
                f.write(req.text)
                
            with open("card.html", 'r', encoding="utf8") as f:
                text = f.read()
            
            soup = BS(text)
            for p in soup.find_all('div'):
                print (p.get("class"))
            occurs = re.compile('images/magic/editions/sigles/(?P<edition>.+)/').findall(text)
            if (occurs == []):
                print("No price")
                exit(1)
            occurs2 = re.compile('[0-9]+[\.][0-9]+ €').findall(text)
            self.price_tab = {x:y for x,y in zip(occurs, occurs2)}
        return self.price_tab

    
    def debug_info(self):
        print("Name : " + self.name)
        print("Url : " + str(self.url))
        print("Price : " + str(self.price_tab))
        
        
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
    my_card = Card("distortion chaotique")
    my_card.debug_info()
    
    
if __name__ == "__main__":
    main()
