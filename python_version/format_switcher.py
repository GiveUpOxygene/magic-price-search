from bs4 import BeautifulSoup as BS

def read_plain_list(filename:str):
    # read the file
    with open(filename, 'r') as f:
        lines = f.readlines()
    # les lignes sont de la forme "number_of_card card_name"
    dico = {}
    for line in lines:
        dico[" ".join(line.split()[1:])] = line.split()[0]
    return dico

def write_plain_list(dico:dict, filename:str):
    # write the file
    with open(filename, 'w') as f:
        for key, value in dico.items():
            f.write(value + " " + key + "\n")

def read_card_list(card_list, debug = False):
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
    
def write_card_list(dico:dict, filename:str):
    '''Ecrit la liste des cartes du deck dans un fichier.cod (format cockatrice)'''
    with open(filename.replace(" ", "_"), 'w', encoding="UTF8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<cockatrice_deck version="1">\n')
        f.write('\t<deckname>' + filename[:-4] + '</deckname>\n')
        f.write('\t<comments>généré automatiquement</comments>\n')
        f.write('\t<zone name="main">\n')
        for card in dico.keys():
            f.write('\t\t<card number="' + str(dico[card]) + '" name="' + card + '"/>\n')
        f.write('\t</zone>\n')
        f.write('</cockatrice_deck>')
        
def main():
    filename = input("Nom du fichier à convertir : ")
    if filename.endswith(".cod"):
        dico = read_card_list(filename)
        write_plain_list(dico, filename[:-4] + ".txt")
    elif filename.endswith(".txt"):
        dico = read_plain_list(filename)
        write_card_list(dico, filename[:-4] + ".cod")
        
if __name__ == "__main__":
    main()