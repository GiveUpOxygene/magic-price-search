import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as BS

# with open("test.html", 'r', encoding="utf8") as f:
#     text = f.read()
#     occurs = re.compile('images/magic/editions/sigles/(?P<edition>.+)/').findall(text)
#     occurs2 = re.compile('[0-9]+[\.][0-9]+ €').findall(text)
    
#     dico = {x:y for x,y in zip(occurs, occurs2)}
#     print (dico)
#     print (float(occurs2[0].replace(' €', '')))

with open("card.html", 'r', encoding="utf8") as f:
    text = f.read()
    
    
edition = []
quantity = []
condition = []
price = []

soup = BS(text,"lxml")
for p in soup.find_all('div'):
    if p.get('class') == ['dispo']:
        for p3 in p.find_all('td'):
            if p3.get_text() != "" :
                if p3.find('select') != None:
                    # print("Quantité : " + p3.get_text()[-1])
                    quantity.append(p3.get_text()[-1])
                elif p3.get('style') == None:
                    if p3.find('img') != None:
                        # print("Edition : " + p3.get_text())
                        edition.append(p3.get_text())
                    else:
                        # print("Condition : " + p3.get_text())
                        condition.append(p3.get_text())
                else:
                    # print("Prix : " + p3.get_text())
                    price.append(p3.get_text())
                    
dico = {x:y for x,y in zip(edition, zip(price, quantity, condition))}

print (dico)