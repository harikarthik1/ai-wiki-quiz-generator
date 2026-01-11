import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch Wikipedia page")

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()
    paragraphs = soup.find_all("p")

    summary = paragraphs[0].text.strip() if paragraphs else ""
    content = " ".join(p.text.strip() for p in paragraphs[:10])
    sections = [s.text for s in soup.select("h2 span.mw-headline")]

    return {
        "title": title,
        "summary": summary,
        "content": content,
        "sections": sections
    }
