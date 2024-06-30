import undetected_chromedriver as uc 
import time
import sys
from bs4 import BeautifulSoup as bs


# Small fix for fucked up library
import chromedriver_autoinstaller

version_main = int(chromedriver_autoinstaller.get_chrome_version().split(".")[0])
this.driver = webdriveruc.Chrome(options=options, seleniumwire_options=seleniumwire_options, version_main=version_main)

# End of fix


# Les urls de cartes sont de la forme : https://www.cardmarket.com/fr/Magic/Cards/English-name-of-the-card

args = sys.argv
# print(args)
card_name = " ".join(args[1:])
print(card_name)

options = uc.ChromeOptions() 
options.headless = True
driver = uc.Chrome(use_subprocess=True, options=options) 
page = driver.get("https://www.cardmarket.com/en/Magic/") 
driver.maximize_window()
print("start sleep")
time.sleep(5)
print("end sleep")

# print(type(page))
driver.save_screenshot("datacamp.png") 
html = driver.page_source
soup = bs(html, "html.parser")
with open("datacamp.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())
driver.close()

