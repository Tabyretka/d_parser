from bs4 import BeautifulSoup as Bs


def sexkomix_parse(response_text: str) -> list:
    res = []
    soup = Bs(response_text, "lxml")
    ul_sp = soup.find_all("ul", id="comix_pages_ul")
    for ul in ul_sp:
        li_sp = ul.find_all("li")
        for li in li_sp:
            res.append(li.find("img").get("data-src"))
    comix_name = soup.find("div", id="left_column").find("div", id="comix_description").find("div",
                                                                                             class_="right_box").find(
        "div", class_="info_box").find("a").text
    res.append(comix_name)
    res.append('jpg')
    return res
