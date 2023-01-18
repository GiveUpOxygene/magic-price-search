from bs4 import BeautifulSoup as BS

with open("test.html", "r",encoding="UTF8") as f:
    text = f.read()
cards = []
card_n = []
soup = BS(text, "lxml")
cache = False
for card in soup.div.find_all("div"):
    if card.get("title") != None:
        print(card.get("title"))
        cards.append(card.get("title"))
    if card.span != None:
        if cache:
            print(card.span.get_text()[0])
            card_n.append(card.span.get_text()[0])
            cache = False
        else:
            cache = True
print({x:y for x,y in zip(cards, card_n)})
        
