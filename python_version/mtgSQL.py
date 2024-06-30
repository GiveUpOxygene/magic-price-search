import sqlite3
import sys
import os
import requests as r
from zipfile import ZipFile

class mtgSQL:
    def __init__(self):
        self.SQLITE_DATABASE = './data/AllPrintings.sqlite'
        
    def update(self):
        # TO-DO : tester téléchargement
        # extraction OK
                
        # get file from mtgjson and save it
        response = r.get("http://api.open-notify.org/astros.json")
        print(response)
        
        # req = r.get('https://mtgjson.com/api/v5/AllPrintings.sqlite.zip', allow_redirects=True)
        # open(os.path.dirname(__file__) + "/data/AllPrintings.sqlite", 'wb',encoding="utf8").write(req.content)
        print("Database updated")
        #unzip
        with ZipFile(self.SQLITE_DATABASE + ".zip", "r") as zObject:
            zObject.extractall()
            
print("test")
m = mtgSQL()
m.update()

    # with ZipFile('./data/AllPrintings.sqlite.zip', "r") as zObject:
    #         zObject.extractall()