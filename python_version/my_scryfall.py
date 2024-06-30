import sys
import sqlite3

## Chemin vers la base
SQLITE_DATABASE = './data/AllPrintings.sqlite'
# https://mtgjson.com/api/v5/AllPrintings.sqlite
# https://mtgjson.com/api/v5/AllPrintings.sqlite.zip

## Connexion à la base
conn = sqlite3.connect(SQLITE_DATABASE)
c = conn.cursor()

""" TO-DO
colors : done
set : done
block : to-do
type : done
oracle : done
mana : to-do
power/toughness/loyalty : to-do
multi-faced : to-do
rarity : to-do
legalities : to-do
spell/permanents/historic : to-do
funny/scheme/phenomenon/vanguard : to-do
cubes : to-do
artist/flavor-text : to-do
border : to-do
year : to-do
reprint : to-do
languages : to-do
"""

"""Indices :
legalities :
SELECT c.name, l.format, l.status
FROM cards c
JOIN legalities l ON l.uuid=c.uuid

isfunny :
SELECT c.name, c.isFunny
FROM cards c

mana :
manacost for color symbols
convertedManaCost

"""


class Request:
    def __init__(self, debug = False):
        self.Select = ["c.name"]
        self.From = ["cards c"]
        self.Where = []
        self.debug = debug
        
    def input_req(self):
        text = input("Recherche: ")
        self.parse(text)
        
    def parse(self, text:str):
        req_list=text.split(' ')
        for req in req_list:
            if req[0:1] == 'c:':
                self.colors(req)
            elif req[0:4] == 'set:':
                self.sets(req)
            elif req[0:6] == 'type:' or req[0:1] == 't':
                self.types(req)
            elif req[0:1] == 'o:':
                self.text(req)
            else:
                raise Exception("Requête invalide")
        
    def full_request(self):
        query = "SELECT " + "".join(self.Select) + ' FROM ' + "".join(self.From) + ' WHERE ' + " and ".join(self.Where)
        return query

    def colors(self, string:str):
        """récupère une string de la forme "c:WUBRG" et la transforme en bout de requète SQL

        Args:
            string (str): _description_
        """
        aliases = {"azorius":"WU", "orzhov":"WB", "boros":"WR", "selesnya":"WG", "dimir":"UB", "izzet":"UR", "golgari":"BG", "simic":"UG", "rakdos":"BR", "gruul":"RG",
                   "abzan":"WBG", "bant":"WUG", "esper":"WUB", "grixis":"UBR", "jeskai":"URW", "jund":"BRG", "mardu":"BRW", "naya":"RGW", "sultai":"BGU", "temur":"GUR",
                   "dune":"WBRG", "glint":"UBRG", "ink":"WURG", "witch":"WUBG", "yore":"WUBR",
                   "plunder":"WBRG", "artifice":"WURG", "reanimator":"WUBG", "colorless":"c"}
        
        # on remplace les alias par leur valeur
        for alias in aliases.keys():
            string = string.replace(alias, aliases[alias])
        
        res = []
        if string[0] != 'c':
            raise Exception("La string n'est pas de la forme 'c:WUBRG'")
        
        if string[2] == 'c':
            res.append("c.colorIdentity IS NULL")
        
        # de la forme "c:WUBRG" ou c=WUBRG"
        if string[1] == ':' or string[1] == '=':
            separateur = ' and '
            l = self.isLike(string[3:])
            for color in l:
                res.append("c.colorIdentity " + color)
        
        
        # de la forme "c>=WUBRG"
        if string[1] == '>':
            if string[2] == '=':
                start = 3
            else:
                start = 2
            separateur = ' or '
            for color in string[start:]:
                if (color not in 'wubrgWUBRG'):
                    raise Exception('mauvaise couleur, doit être dans wubrg ou WUBRG')
                res.append("c.colorIdentity LIKE '%" + color + "%'")
        
        # de la forme "c<=WUBRG"
        if string[1] == '<':
            if string[2] == '=':
                start = 3
            else:
                start = 2
            separateur = ' and '
            l = self.isLike(string[start:])
            for color in l:
                if color[0] == 'L':
                    res.append("c.colorIdentity " + color)



        self.Where.append(separateur.join(res))
        self.Select.append(",c.colorIdentity")
        
        if self.debug:
            print(self.Where)
            
    def isLike(self, string:str):
        """renvoie une suite de LIKE et NOT LIKE pour une string de la forme "WUBRG"

        Args:
            string (str): caractères de la forme "WUBRG"
        """
        colors = ['W', 'U', 'B', 'R', 'G']
        flags = [False, False, False, False, False]
        res = []
        string = string.upper()
        for color in string:
            if color not in colors:
                raise Exception('mauvaise couleur, doit être dans wubrg ou WUBRG')
            flags[colors.index(color)] = True
        
        for color in colors:
            if flags[colors.index(color)]:
                res.append("LIKE '%" + color + "%'")
            else:
                res.append("NOT LIKE '%" + color + "%'")
        return(res)
        
    def sets(self, string:str):
        if string[0:3] != 'set:':
            raise Exception("La string n'est pas de la forme 'set:CODE'")
        
        self.Where.append("c.setCode = '" + string[4:] + "'")
        
    def types(self, string:str):
        if (string[0:5] != 'type:') or (string[0:1] != 't:'):
            raise Exception("La string n'est pas de la forme 'type:TYPE'")
        
        if string[0:5] == 'type:':
            start = 6
        else:
            start = 2
            
        if string[start:] == 'legendary':
            self.Where.append("c.supertypes IS NOT NULL")
            
        types = ['artifact', 'creature', 'enchantment', 'instant', 'land', 'planeswalker', 'sorcery']
        if string[start:] in types:
            self.Where.append("c.type LIKE '%" + string[start:] + "%'")
        else:
            self.Where.append("c.subtypes LIKE '%" + string[start:] + "%'")
            

    def cmc(self, string:str):
        if string[0:3] != 'cmc:':
            raise Exception("La string n'est pas de la forme 'cmc:NUMBER'")
        
        self.Where.append("c.ConvertedManaCost = " + string[4:])
        
    def manaPips(self, string:str):
        if string[0:3] != 'pip:':
            raise Exception("La string n'est pas de la forme ':WUBRG'")
        
        self.Where.append("c.manaCost LIKE '%" + string[4:] + "%'")
        
    def manaEvenOrOdd(self, string:str):
        
        if string != 'manavalue:even' or string != 'manavalue:odd':
            raise Exception("La string n'est pas de la forme 'manavalue:even' ou 'manavalue:odd'")
        
        reste = -1
        if string[9:] == 'even':
            reste = 0
        elif string[9:] == 'odd':
            reste = 1
        else:
            # HOW DID YOU GET HERE ?
            raise Exception("La string n'est pas de la forme 'manavalue:even' ou 'manavalue:odd'")
            
            
            
    def text(self, string:str):
        if string[0] != 'o':
            raise Exception("La string n'est pas de la forme 'o:TEXT'")
        self.Where.append("c.text LIKE '%" + string[2:] + "%'")
        
        
req = Request("")
req.colors('c=WU')
print(req.full_request())

# if __name__ == '__main__':
#     req = Request()
#     req.input_req()
#     print(req.full_request())