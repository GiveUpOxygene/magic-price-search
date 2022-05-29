from email import message
import googlesearch as gr
import requests as r
import re
import numpy as np
import os
from guizero import App, Text

class Card:
    def __init__(self, name = None, url = None, price = 0.25):
        self.name = name
        self.url = url
        self.price = price
        
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
        if self.url != None:
            req = r.get(self.url, 'html.parser')
            occurs = re.compile('"prix_full">(?P<price>[0-9]*\.[0-9]{2})').findall(req.text)
            while('1.12' in occurs):
                occurs.remove('1.12')
            print(occurs)
            if (self.url in "Montagne Île Plaine Forêt Marais") or (occurs == []):
                price = 0.25
            else:
                price = float(occurs[0])
            print(get_card_name_from_url(self.url) + " : " + str(price))
            return price
        
    def read_price(self):
        req = r.get(self.url, 'html.parser')
        with open('temp_file.txt', 'w') as f:
            f.write(req.text)
        price = []
        with open("temp_file.txt", 'r') as f:
            for line in f.readlines():
                if "prix_full" in line:
                    temp = line.replace('<div class="prix_full">', "")
                    temp = temp.replace('&nbsp;€</div>\n', "")
                    temp = temp.replace(',', ".")
                    price.append(float(temp))
        os.remove('temp_file.txt')
        print(price)

class Deck:
    def __init__(self, name, card_list = None, url = None, deck_type = "Commander"):
        self.name = name
        self.url = url
        if self.url == None:
            self.get_url()
        self.deck_type = deck_type
        if card_list != None:
            self.card_list = self.read_card_list(card_list)

    
    def get_url(self):
        query = "deck commander " + self.name.lower() + " play in magic bazar"
        url = gr.search(query, num = 1, stop = 1)[0]
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
            card_dict = {}
            for index in range(len(occurs_deck_list)):
                card_dict[occurs_deck_list[index]] = int(occurs_deck_number[index])
        return card_dict

def get_card_name_from_url(card_url):
    req = r.get(card_url, 'html.parser')
    # occurs = re.compile("'<title>(?P<name>[0-9a-zA-Z,'\- éèàêëîœÀÉÈÇŒÎ]*)<\\title>").findall(req.text)
    with open('temp_file.txt', 'w') as f:
        f.write(req.text)
    with open('temp_file.txt', 'r') as f:
        card_name = f.readlines()[3]
    os.remove('temp_file.txt')
    return card_name[7:-60].split(" - ")[0]

def card_price(card_name):
    #retourne le prix d'une carte trouvé sur play-in, et 0.25€ si la carte n'est pas trouvée
    query = card_name.lower() + "play in magic bazar"
    for url in gr.search(query, tld="co.in", num=1, stop=1, pause=2):
        req = r.get(url, 'html.parser')
        occurs = re.compile(r'(?P"prix_full">[0-9],[0-9]{2})').findall(req.text)
        while('1.12' in occurs):
            occurs.remove('1.12')
        print(occurs)
        if (card_name in "Montagne Île Plaine Forêt Marais") or (occurs == []):
            price = 0.15
        else:
            price = float(occurs[0])
        print(card_name + " : " + str(price))
        return price

def card_price_list(card_name):
    #retourne une liste contenant tous les prix d'une carte listés sur play-in
    query = card_name.lower() + "play in magic bazar"
    for url in gr.search(query, tld="co.in", num=1, stop=1, pause=2):
        req = r.get(url, 'html.parser')
        occurs = re.compile(r'"prix_full">(?P<price>[0-9]*\.[0-9]{2})').findall(req.text)
        while('1.12' in occurs):
            occurs.remove('1.12')
        print(occurs)
        if (card_name in "Montagne Île Plaine Forêt Marais"):
            price = 0.15
        elif (occurs == []):
            price = 0.00
            print("card not found or not listed")
        else:
            price = float(occurs[0])
        print(card_name + " : " + str(price))
        return price

def card_price_from_url(card_url):
    req = r.get(card_url, 'html.parser')
    occurs = re.compile('"prix_full">(?P<price>[0-9]*\.[0-9]{2})').findall(req.text)
    while('1.12' in occurs):
        occurs.remove('1.12')
    print(occurs)
    if (card_url in "Montagne Île Plaine Forêt Marais") or (occurs == []):
        price = 0.25
    else:
        price = float(occurs[0])
    print(get_card_name_from_url(card_url) + " : " + str(price))
    return price

def get_deck_card_list(deck_name):
    query = "deck commander " + deck_name.lower() + " play in magic bazar"
    for url in gr.search(query, tld="co.in", num=1, stop=1, pause=2):
        req = r.get(url, 'html.parser')
        occurs = re.compile('/api/[0-9a-zA-Z.?=]*').findall(req.text)
        deck_list_url ='https://www.play-in.com' + occurs[0]
        req_deck_list = r.get(deck_list_url, 'html.parser')
        occurs_deck_list = re.compile("(?P<name>\/magic\/carte\/[0-9a-zA-Z,'\- éèàêëîœÀÉÈÇŒÎ]*)").findall(req_deck_list.text)
        occurs_deck_number = re.compile("\<span\>(?P<number>[0-9]*) x\</span\>").findall(req_deck_list.text)
        print(occurs_deck_number)
        for card in occurs_deck_list:
            print("card1 = " + card)            
    return occurs_deck_list, occurs_deck_number




#print(get_card_name_from_url("https://www.play-in.com/magic/carte/19655-omnath_locus_de_rage"))
# print(card_price_from_url("https://www.play-in.com/magic/carte/19655-omnath_locus_de_rage"))
# app = App(title = "Magic price finder")
# deck_list, deck_number = get_deck_card_list("aura de courage")
omnath = Card(name = "Omnath, Locus de rage")
omnath.url = omnath.get_url()
print(omnath.url)
omnath.read_price()

# print(deck_list)
# for index in range(np.size(deck_list)):
#     url = ("https://www.play-in.com" + deck_list[index]).replace(" ", "_")
#     print("card0 = " + get_card_name_from_url(url))
#     my_card_price = card_price_from_url(url)
#     deck_price += float(deck_number[index]) * my_card_price
# message = Text(app, text = "deck price = " + str(deck_price))
# app.display()