from bs4 import BeautifulSoup as bs
import bs4

index_list = ["nad","nv","lowest","avg"]
value_list = []

with open("test.html","r", encoding="utf-8") as f:
    soup = bs(f.read(), "html.parser", parse_only=bs4.SoupStrainer("dl"))
    for c in soup.dl.findChildren(recursive=False):
        if c.name == "dd":
            value_list.append(c.get_text())
    dico = {x:y for x,y in zip(index_list, value_list)}
    
print(dico)