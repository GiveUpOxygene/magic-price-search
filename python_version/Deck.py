import Card

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

def debug_main():
    pass


if __name__ == "__main__":
    debug_main()