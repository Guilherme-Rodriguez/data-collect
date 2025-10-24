# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36',
    # 'cookie': '_gid=GA1.2.356645792.1761315075; __gads=ID=03c67021ca64746a:T=1761315069:RT=1761316679:S=ALNI_MaV3WyfzQL8K_Vn8PuvhJvQyChYcA; __gpi=UID=000012a4570536a6:T=1761315069:RT=1761316679:S=ALNI_MbBMLU_97MX505y63GVskoUyncxMA; __eoi=ID=010137e72c610c95:T=1761315069:RT=1761316679:S=AA-AfjbJ4wMA2qZzSgn-0BIJicv-; _gat_gtag_UA_29446588_1=1; _ga=GA1.2.1094606635.1761315074; _ga_DJLCSW50SC=GS2.1.s1761315074$o1$g1$t1761316786$j60$l0$h0; _ga_D6NF5QC4QT=GS2.1.s1761315075$o1$g1$t1761316786$j60$l0$h0; FCNEC=%5B%5B%22AKsRol_wonevWjrvtMGpJuaeHRYq7EJ1BbVYjrv0d9kJkBfhkjLDr7ozLhRTMcktR5LO_P9yC4httKrwWuwagrUWn5pNX8XTK3KpyD1H1kD1xsi3H7g1kWrjErCIZRmXuQ8rUiGqFRTlD05shOYNaS0dMxF_BlY5LA%3D%3D%22%5D%5D',
}

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
            .find("h4")
            .find_next()
            .find_all("li"))

    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagens_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print("Nao foi possivel obter os dados")
        return {}
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data
    
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers = headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_ = "td-page-content")
                    .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links
# %%

url = "https://www.residentevildatabase.com/personagens/alex-wesker/"
get_personagens_infos(url)

# %%

links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_infos(i)
    d['link'] = i
    data.append(d)

# %%
