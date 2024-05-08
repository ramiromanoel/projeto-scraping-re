# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,pt;q=0.8,ko;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': '_gid=GA1.2.331339392.1711779955; _ga_D6NF5QC4QT=GS1.1.1711779955.1.1.1711779998.17.0.0; _ga=GA1.2.1385083095.1711779955; FCNEC=%5B%5B%22AKsRol__YvRyHqz3ey_PN5DnuIa59K8ryCpMOfNz2rgFg-qGKebEHZQSaInyPTYMgLDbpUzdOHbR4M-leD9IJBV1OJWjdR6rUTI7ePIsnNZjUIpZlUapJtTQZjHv7Wnzxkyx9L-kpwQ9Mle4rELD_QrXNhDhKJyoIw%3D%3D%22%5D%5D; __gads=ID=85c8b9a27469f2dc:T=1711779997:RT=1711779997:S=ALNI_MYloXJvksd81YVkRWSw4g-4wyCp-w; __gpi=UID=00000dd706d9408b:T=1711779997:RT=1711779997:S=ALNI_Man2boXSjxOxmeCy2hX3Gkgfk5vzQ; __eoi=ID=c4d227722bb8a8dc:T=1711779997:RT=1711779997:S=AA-AfjZdAQQ7j2DLys3lV1GMYeX7; _ga_DJLCSW50SC=GS1.1.1711779954.1.1.1711780002.12.0.0',
        'pragma': 'no-cache',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
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
        print("Não foi possível obter os dados!")
        return{}

    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        data

def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_ = "td-page-content")
                               .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_infos(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

# %%
