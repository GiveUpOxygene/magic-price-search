from bs4 import BeautifulSoup as bs
import bs4

with open("test2.html","r", encoding="utf-8") as f:
    soup = bs(f.read(), "html.parser", parse_only=bs4.SoupStrainer("h1"))
    # print(soup.prettify())
    print(soup.h1.get_text())