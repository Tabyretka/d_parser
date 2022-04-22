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


def main(url: str) -> None:
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
            }
    rs = requests.get(url=url, headers=headers)
    if rs.ok:
        soup = Bs(rs.text, "lxml")
        images = soup.find_all("img")
        images_sp = []
        comix_name = soup.find("div", id="left_column").find("div", id="comix_description").find("div", class_="right_box").find("div", class_="info_box").find("a").text
        if not os.path.exists(f"data/{comix_name}"):
            os.mkdir(f"data/{comix_name}")
        for image in images:
            if "uploads_images" in str(image.get("data-src")):
                images_sp.append(image.get("data-src"))
        s = requests.Session()
        for image_url in enumerate(images_sp):
            rs = s.get(url=image_url[1], headers=headers)
            with open(f"data/{comix_name}/{image_url[0]}.jpg", "wb") as image:
                image.write(rs.content)
                progress(count=image_url[0], total=len(images_sp),
                        status="downloading")
    else:
        print(f"err code {rs.status_code}")


if __name__ == '__main__':
    if not os.path.exists("data"):
        os.mkdir("data")
    url = input("Insert url:\n")
    main(url=url)
