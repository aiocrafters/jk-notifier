import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl_jkssb(save_notification):

    print("Crawling JKSSB Advertisements")

    url = "https://www.jkssb.nic.in/Advertisement.html"
    base_url = "https://www.jkssb.nic.in"

    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")

    links = soup.select("a.linkText")

    for link in links:

        title = link.text.strip()

        href = link.get("href")

        if not href:
            continue

        full_link = urljoin(base_url, href)

        save_notification(
            "JKSSB Advertisements",
            title,
            full_link
        )