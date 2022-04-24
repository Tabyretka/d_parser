from bs4 import BeautifulSoup as Bs


def pornocomics_parse(response_text: str) -> list:
    soup = Bs(response_text, "lxml")
    comix_name = soup.find("div", class_="fone").find("h1").text
    res = [f'http://pornocomics.icu/{img.get("data-src")}' for img in
           soup.find('div', class_='fdesc full-text clearfix').find_all('img')]
    res.append(comix_name)
    res.append('webp')
    return res
