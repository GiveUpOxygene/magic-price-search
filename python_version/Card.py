import sys
import os
import googlesearch as gr
from bs4 import BeautifulSoup as BS
import bs4
import requests as r

def fprint(string:str, output="out.txt"):
    with open(output, "a") as f:
        f.write("test : " + string + "\n")
    

class Card:
    def __init__(self, name = None):
        # /!\ le nom de la carte doit être en anglais jusqu'à ce que je trouve un moyen fiable de traduire
        self.cm_url = "https://www.cardmarket.com/fr/Magic/Cards/"
        self.mc_url = ""
        fprint("name : " + str(name))
        if name == None:
            raise ValueError("No name")
        
        self.name = name
        self.get_mc_url()
        self.get_name()
        
        self.cm_filename = "cm_" + self.name.replace(' ', '_') + '.html'
        self.mc_filename = "mc_" + self.name.replace(' ', '_') + '.html'
        self.cm_tab = self.get_cardmarket_info()
        self.info_tab = self.get_info()
        
    def traduction(self):
        """Traduit le nom de la carte en anglais
        """
        with open(self.mc_filename, "r", encoding="utf-8") as f:
            soup = BS(f.read(), "html.parser", parse_only=bs4.SoupStrainer("h1"))
            name_and_trad = soup.h1.get_text()
            index = name_and_trad.find(self.name)
            if (index == -1):
                raise ValueError("No name")
            
            if (index==0):
                self.name = name_and_trad[name_and_trad.find("(")+1:name_and_trad.find(")")]
            if (index>0):
                print("Name already in english")
        
    def get_mc_url(self):
        """récupère l'url de la carte sur magiccorporation.com

        Raises:
            ValueError: Si le nom de la carte n'est pas renseigné
        """
        if self.name == None:
            raise ValueError("No name")
        # get the first google result for the card on magiccorporation website
        for my_url in gr.search('site:"https://boutique.magiccorporation.com/"' + self.name, num = 1, stop = 1):
            self.mc_url = my_url
            fprint(self.mc_url)
        
    def get_cm_url(self):
        """récupère l'url de la carte sur cardmarket.com
        
        Raises:
            ValueError: Si le nom de la carte n'est pas renseigné
        """
        if self.name == None:
            raise ValueError("No name")
        self.cm_url += self.name.replace(' ', '-')
        fprint(self.cm_url)
        
        
    def get_name(self):
        """Récupère le nom de la carte à partir de l'url"""
        if self.mc_url == None:
            print("No url")
            return None
        # TODO : get the name of the card with some good code and not this clusterfuck
        self.name = ' '.join(self.mc_url.split('/')[-1].split('-')[3:]).replace('-', ' ').replace('.html', '')
        # return self.name
        
    def get_cardmarket_info(self, debug=False):
        """Renvoie les informations sous la forme d'un dictionnaire :
        nad : Nombre d'articles disponibles
        nv : Nombre de versions
        lowest : A partir de
        avg : Tendance du prix

        Args:
            debug (bool, optional): _description_. Defaults to False.
        """
        
        pass
    
    def get_cardmarket_prices(self, debug=False):
        """Récupère la table des prix de la page cardmarket

        Args:
            debug (bool, optional): prints additionnal debug info. Defaults to False.
        """
        pass
    
    
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
        if self.cm_url != '':
            req = r.get(self.mc_url, 'html.parser')
        
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
        print("Url : " + str(self.mc_url))
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
            
            
"""def get_price_from(source_url:str = "magiccorp", debug:bool = False):
    if (source_url == "magiccorp"):
        edition = []
        price = []
        quantity = []
        condition = []
        #get the html from the url
        text = r.get(self.url, 'html.parser').text
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
"""

def cleanup():
    for file in os.listdir("./cards"):
        os.remove("./cards/" + file)

if __name__ == "__main__":
    args = sys.argv
    my_card = Card(" ".join(args[1:]).replace('_', ' '))
    my_card.get_cm_url()
    # print(type(args[1]))
    # my_card = Card(args[1].replace('_', ' '))
    # my_card.get_info(debug=True)
    # my_card.debug_info()
    # cleanup()