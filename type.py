import requests
from bs4 import BeautifulSoup as bs
import re

def getHtml(mot,sortant, rel=4):
    with requests.Session() as s:
        url = 'http://www.jeuxdemots.org/rezo-dump.php?'

        if sortant:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel': rel, 'relin': 'norelout'}
        else:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel': rel, 'relout': 'norelin'}

        try:
            r = s.get(url, params=payload)
            soup = bs(r.text, 'html.parser')
            prod = soup.find_all('code')

            # Vérifier si le mot recherché est présent dans la page
            if "MOT_NON_TROUVE" in str(prod):
                print("Mot non trouvé dans le dictionnaire.")
            

        except Exception as e:
            print("Une erreur s'est produite :", str(e))
    return r.text
    

def getTypes(mot):
    codesource=getHtml(mot,sortant=True, rel=4)
    # Utilisation d'une expression régulière pour extraire les troisièmes nombres après "r;"
    pattern = r'r;(\d+);(\d+);(\d+);(\d+);(\d+)'
    matches = re.findall(pattern,codesource)

    # Filtrer les matches pour éliminer ceux avec un cinquième nombre négatif
    matches = [match for match in matches if int(match[4]) >= 0]



    # Récupérer le troisième nombre de chaque correspondance
    troisiemes_nombres = [match[2] for match in matches]

    for n in troisiemes_nombres:
        pattern2 = r"e;(\d+);'([^']+)';"

        matches=re.findall(pattern2,codesource)

       # Récupérer la deuxième partie lorsque le deuxième nombre fait partie de troisiemes_nombres
    deuxiemes_parties = [match[1] for match in matches if match[0] in troisiemes_nombres]

    return deuxiemes_parties



    #récupérer 





# Exemple d'utilisation
if __name__ == "__main__":
    mot_recherche = "MOT_A_RECHERCHER"  # Remplacez par le mot que vous souhaitez rechercher
    relation = 4  # Remplacez par la relation spécifique que vous souhaitez



    # Recherche sortante (rel:4) pour le mot donné
    #getHtml('se doucher', sortant=True, rel=relation)
    types=getTypes('pilote')
    print(types)



