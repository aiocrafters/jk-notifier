import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://jkgad.nic.in"
URL = "https://jkgad.nic.in/En/OrderCirculer.aspx?ordType=O"


def get_hidden_fields(soup):

    data = {}

    for inp in soup.select("input[type=hidden]"):

        name = inp.get("name")
        value = inp.get("value", "")

        if name:
            data[name] = value

    return data


def extract_orders(soup, save_notification):

    rows = soup.select("#ctl00_conPage_dgActRule tr")

    for row in rows:

        title_tag = row.select_one("span.itemLink")

        if not title_tag:
            continue

        title = title_tag.text.strip()

        cols = row.select("td")

        if len(cols) < 3:
            continue

        order_info = cols[1].text.strip()
        department = cols[2].text.strip()

        link_tag = row.select_one("a")

        if not link_tag:
            continue

        onclick = link_tag.get("onclick", "")

        match = re.search(r"window.open\('(.*?)'", onclick)

        if not match:
            continue

        link = urljoin(BASE_URL, match.group(1))

        save_notification(
            "JK GAD Orders",
            f"{title} ({order_info})",
            link
        )


def crawl_gad(save_notification):

    print("Starting JK GAD crawler")

    session = requests.Session()

    res = session.get(URL)

    soup = BeautifulSoup(res.text, "lxml")

    payload = get_hidden_fields(soup)

    page = 1

    while True:

        print(f"Processing page {page}")

        extract_orders(soup, save_notification)

        next_button = soup.find("a", string="| Next")

        if not next_button:
            print("No more pages")
            break

        payload["__EVENTTARGET"] = "ctl00$conPage$dgActRule$ctl14$ctl01"
        payload["__EVENTARGUMENT"] = ""

        res = session.post(URL, data=payload)

        soup = BeautifulSoup(res.text, "lxml")

        payload = get_hidden_fields(soup)

        page += 1

        if page > 50:
            break