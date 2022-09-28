import googlesearch as gr
import requests as r
import re
import numpy as np
import os
from guizero import App, Text, TextBox, PushButton, Box

class Card:
    def __init__(self, name = None, url = None, price = 0.25):
        self.name = name
        self.url = url
        self.price = price
        if not (self.name in "Montagne Île Plaine Forêt Marais"):
            self.get_url()
        self.get_name()
        
    def get_url(self):
        if self.name == None:
            print("No name")
            return None
        for url in gr.search(self.name + "playin magic bazar", num = 1, stop = 1):
            self.url = url
        return self.url
        
    def get_name(self):
        if self.url == None:
            print("No url")
            return None
        req = r.get(self.url, 'html.parser')
        with open('temp_file.txt', 'w') as f:
            f.write(req.text)
        with open('temp_file.txt', 'r') as f:
            card_name = f.readlines()[3]
        os.remove('temp_file.txt')
        self.name = card_name[7:-60].split(" - ")[0]
    
    def get_price(self):
        if self.name in "Montagne Île Plaine Forêt Marais" :
            return 0.25
        if self.url != None:
            req = r.get(self.url, 'html.parser')
            occurs = re.compile('"prix_full">(?P<price>[0-9]+\.[0-9]{2})&nbsp;€').findall(req.text)
            while('1.12' in occurs):
                occurs.remove('1.12')
            print(occurs)
            if (occurs == []):
                price = 0.25
            else:
                price = float(occurs[0])
            print(self.name + " : " + str(price))
        return price
        
    def get_card_info(self):
        req = r.get(self.url, 'html.parser')
        with open('temp_file.txt', 'w') as f:
            f.write(req.text)
        price = []
        lang = []
        foil = []
        state = []
        
        with open("temp_file.txt", 'r') as f:
            for line in f.readlines():
                if "prix_full" in line:
                    temp = line.replace('<div class="prix_full">', "").replace('&nbsp;€</div>\n', "").replace(',', ".")
                    price.append(float(temp))
                if 'data-foil="' in line :
                    temp = line.split('data')
                    #temp[0] : inutile
                    #temp[1] : foil
                    foil.append(temp[1].split('"')[0])
                    #temp[2] : langue abrégée
                    lang.append(temp[2].split('"')[1])
                    #temp[3] : état + inutile
                    state.append(int(temp[3].split('"')[1]))
                    # foil.append(foil_state[temp])
        os.remove('temp_file.txt')
        self.price = price[0]
        return(price, lang, foil, state)

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

def deck_search(name):
    remove_former_screen()
    searched_deck = Deck(name)
    searched_deck.get_card_list()
    deck_price = 0
    for card in searched_deck.card_list:
        print(card)
        my_card = Card(card)
        deck_price += my_card.get_price()
        text_list.append(Text(app, text = "prix du deck : " + "{:.2f}".format(deck_price)))
        
    
def card_search(name):
    remove_former_screen()
    searched_card = Card(name)
    searched_card.url = searched_card.get_url()
    print(searched_card.url)
    price_tab, lang_tab, foil_tab, state_tab = searched_card.get_card_info()
    text_list.append(Text(app, text = searched_card.name, size = 20))
    for index in range(len(price_tab)):
        text_list.append(Text(app, text = "Prix : " + "{:.2f}".format(price_tab[index]) + "€, " + card_state[state_tab[index]] + ", " + lang_tab[index]))
    app.display()

def remove_former_screen():
    print(text_list)
    for text in text_list:
        text.destroy()
    text_list.clear()

# ---Main---
card_state = ["?", "Mint,Nmint", "Played", "?", "?", "?", "Exc", "?", "?", "?", "?", "Poor"]
foil_state = {"O" : "Foil", "N" : "Non-Foil"}
text_list = []
app = App(title = "Magic price finder")
title = Text(app, text = "Magic price finder", size = 30, color = "black")
my_text = TextBox(app, text = "Magic", width="fill")
button_box = Box(app, align="top", width="fill")
card_button = PushButton(button_box, text = "Find card", command = lambda: card_search(my_text.value),align="left",width="fill")
deck_button = PushButton(button_box, text = "Find deck", command = lambda: deck_search(my_text.value),align="left",width="fill")
app.display()




# deck_list, deck_number = get_deck_card_list("aura de courage")
# print(deck_list)
# for index in range(np.size(deck_list)):
#     url = ("https://www.play-in.com" + deck_list[index]).replace(" ", "_")
#     print("card0 = " + get_card_name_from_url(url))
#     my_card_price = card_price_from_url(url)
#     deck_price += float(deck_number[index]) * my_card_price

