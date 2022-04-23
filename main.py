import requests
import os
import sys
from bs4 import BeautifulSoup as Bs


def progress(count, total, status='', bar_len=60):
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    fmt = '[%s] %s%s ...%s' % (bar, percents, '%', status)
    print('\b' * len(fmt), end='')
    sys.stdout.write(fmt)
    sys.stdout.flush()


def get_url(url: str) -> list:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
    }
    res = []
    try:
        rs = requests.get(url=url, headers=headers)
        if rs.ok:
            soup = Bs(rs.text, "lxml")
            ul_sp = soup.find_all("ul", id="comix_pages_ul")
            for ul in ul_sp:
                li_sp = ul.find_all("li")
                for li in li_sp:
                    res.append(li.find("img").get("data-src"))
            comix_name = soup.find("div", id="left_column").find("div", id="comix_description").find("div",
                                                                                                     class_="right_box").find(
                "div", class_="info_box").find("a").text
            res.append(comix_name)
            return res
    except Exception as e:
        print(e)
        os.abort()


def save_url(pic_sp: list) -> None:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
    }
    session = requests.Session()
    comix_name = pic_sp.pop()
    if not os.path.exists(f'data/{comix_name}'):
        os.mkdir(f'data/{comix_name}')
    for pic_url in enumerate(pic_sp):
        rs = session.get(url=pic_url[1], headers=headers)
        if rs.ok:
            with open(f'data/{comix_name}/{pic_url[0]}.jpg', 'wb') as p:
                p.write(rs.content)
                progress(pic_url[0], len(pic_sp), status='downloading')


if __name__ == '__main__':
    if not os.path.exists("data"):
        os.mkdir("data")
    url = input("Insert url:\n")
    pic_sp = get_url(url=url)
    save_url(pic_sp)
