from bs4 import BeautifulSoup
import requests


def get_html_content(url: str):
    response = requests.get(
        url,
        timeout=(1, 30),
        headers={"User-Agent": "Mozilla/5.0"},
    )

    response.raise_for_status()

    return response.text


def get_parsed_html(base_url: str) -> BeautifulSoup:
    """
    Fetches the "consolidated" law text from base_url,
    which is expected to be the brazilian
    """
    soup = BeautifulSoup(get_html_content(base_url), features="html.parser")

    with open("page.html", mode="w") as f:
        f.write(soup.prettify())

    compiled_link = soup.find(
        "a", string=lambda text: "Texto compilado" in text, recursive=True
    )
    # page_html = get_html_content(url)
    if not compiled_link and compiled_link.get("href"):
        raise Exception("Missing URL")

    compiled_url = requests.compat.urljoin(base_url, compiled_link["href"])
    return BeautifulSoup(get_html_content(compiled_url), features="html.parser")


def clean_parsed_html(parsed_html: BeautifulSoup) -> dict:
    """Parses an HTML parsed by beatiful soap into a law graph"""
    return {}


def transform_parsed_html_to_law_graph(parsed_html: BeautifulSoup) -> dict:
    """Parses an HTML parsed by beatiful soap into a law graph"""
    return {}


if __name__ == "__main__":
    base_url = "https://www.planalto.gov.br/ccivil_03/_Ato2011-2014/2012/Lei/L12651.htm"
    get_parsed_html(base_url)
