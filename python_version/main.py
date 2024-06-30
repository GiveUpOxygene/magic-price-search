import googlesearch as gr
import requests as r
import re
import os
from bs4 import BeautifulSoup as BS
from enum import Enum

class WebSites(Enum):
    magiccorp = "https://boutique.magiccorporation.com/"
    cardmarket = "https://www.cardmarket.com/fr/Magic/"

class Card:
    def __init__(self, name = None, url = None):
        self.url = url
        self.url = self.get_url(name)
        print(self.url)
        self.name = self.get_name()
        print(self.name)
        self.filename = ""
        self.info_tab = self.get_info()
        
    def get_url(self, name, site = "https://boutique.magiccorporation.com/"):
        if name == None:
            print("No name")
            return None
        for my_url in gr.search("site:" + name, num = 1, stop = 1):
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
        # if debug == False:
        #     print("Suppression du fichier " + self.filename)
        #     os.remove(f"./cards/{self.filename}")
        return dico

    def debug_info(self):
        print("Name : " + self.name)
        print("Url : " + str(self.url))
        print("Price : " + str(self.info_tab))
        
    def best_price(self, quantity=1):
        min_price = 1_000_000 # prix supérieur à celui de n'importe quelle carte
        min_price_edition = ""
        for edition in self.info_tab:
            if (min_price > float(self.info_tab[edition][0][:-2])) and (float(self.info_tab[edition][1][:-2]) >= quantity):
                min_price = self.info_tab[edition][0]
                min_price_edition = edition
        if min_price_edition == "":
            return None
        else:
            return (min_price_edition, min_price)
            
            
def get_price_from(source_url:str = "magiccorp", debug:bool = False):
    if (source_url == "magiccorp"):
        edition = []
        price = []
        quantity = []
        condition = []
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
    elif (source_url == "cardmarket"):
        soup = BS(text, "html.parser")    
        dd = [d.text for d in soup.find_all("dd")]
        dt = [d.text for d in soup.find_all("dt")]

        dico = dict(zip(dt, dd))
        for k, v in dico.items():
            print(k, v)
        return
        
class Deck:
    def __init__(self, name, card_list_file = None, url = None, deck_type = "Commander", auto = True):
        if auto:
            self.deck_type = deck_type
            self.name = name
            self.url = url
            self.deck_price = 0
            if self.url == None:
                self.get_url()
            self.deck_list = self.get_card_list(self.url)
            
        else:
            self.name = name
            self.url = None
            self.deck_type = deck_type
            if card_list_file != None:
                self.deck_list = self.read_card_list(card_list_file)
            else:
                print("No card list file")
                exit(1)
            
    def get_url(self):
        query = "site:https://www.play-in.com/ deck " + self.deck_type + " " + self.name.lower()
        for url in gr.search(query, num = 1, stop = 1):
            self.url = url
        print(url)
    
    def read_card_list(self, card_list, debug = False):
        '''Récupère la liste des cartes du deck depuis un fichier.cod (format cockatrice)'''
        dico = {}
        with open(card_list, 'r') as f:
            text = f.read()
        soup = BS(text, "lxml")
        for p in soup.find_all('card'):
            dico[p.get('name')] = p.get('number')
            if debug:
                print(p.get('name') + " " + p.get('number'))
        return dico
        
    def write_card_list(self, deck_name):
        '''Ecrit la liste des cartes du deck dans un fichier.cod (format cockatrice)'''
        with open("./decks/" + deck_name.replace(" ", "_") + ".cod", 'w', encoding="UTF8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<cockatrice_deck version="1">\n')
            f.write('\t<deckname>' + self.name + '</deckname>\n')
            f.write('\t<comments>généré automatiquement</comments>\n')
            f.write('\t<zone name="main">\n')
            for card in self.deck_list.keys():
                f.write('\t\t<card number="' + str(self.deck_list[card]) + '" name="' + card + '"/>\n')
            f.write('\t</zone>\n')
            f.write('</cockatrice_deck>')
    
    def get_card_list(self, write = False, debug = False):
        #récupère la liste depuis internet
        query = "site:https://www.play-in.com deck " + self.deck_type + " " + self.name.lower() + " play in magic bazar"
        for url in gr.search(query, tld="co.in", num=1, stop=1, pause=2):
            req = r.get(url, 'html.parser')
        #récupération de la page contenant la liste des cartes
        occurs = re.compile('/api/[0-9a-zA-Z.?=]*').findall(req.text)
        deck_list_url ='https://en.play-in.com' + occurs[0]
        req_deck_list = r.get(deck_list_url, 'html.parser')
        # with open("./temp/deck.html", 'w') as f:
        #     f.write(req_deck_list.text)
        # with open("./temp/deck.html", 'r') as f:
        #     text = f.read()
        
        # récupération des cartes et de leur nombre
        card_list = []
        card_number = []
        soup = BS(req_deck_list.text, "lxml")
        cache = False
        for card in soup.div.find_all("div"):
            if card.get("title") != None:
                if debug:
                    print(card.get("title"))
                card_list.append(card.get("title"))
            if card.span != None:
                if cache:
                    if debug:
                        print(card.span.get_text()[0])
                    card_number.append(card.span.get_text()[0])
                    cache = False
                else:
                    cache = True
        self.deck_list = {x:y for x,y in zip(card_list, card_number)}
        if write:
            self.write_card_list(self.name)
        return self.deck_list
            
    def get_deck_price(self, debug = False):
        #récupère le prix du deck depuis internet
        self.deck_price = 0
        for card in self.deck_list.keys():
            if debug:
                print(card)
            c = Card(card)
            if c.best_price()[1] != None:
                self.deck_price += c.best_price()[1] * int(self.deck_list[card])
            else :
                print(card + " not available")
        return self.deck_price
                



# ---Main---


def main():
    return
    

def cleanup():
    for file in os.listdir("./cards"):
        os.remove("./cards/" + file)
    
def debug_main():
    card = Card("pas de ce monde") 
    card.get_info(debug=True)
    card.debug_info()
    cleanup()
    
    # deck = Deck("pouvoirs de la ruine")
    # deck.write_card_list(deck.name)
    # print(deck.get_deck_price())
    
    
if __name__ == "__main__":
    debug_main()
