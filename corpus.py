from enum import Enum
import httpx

USER_AGENT = "Mozilla/5.0"  # "compliance-app/1.0"


class LawCode(str, Enum):
    civil = "civil"
    forest = "forest"


# TODO: replace hard-coded URLs with dynamic navigation to find the compiled versions
# TODO: replace this function with a an API which returns the page contents. This way, it can
# fallback to a default page containing the last version, whenever the URLs change
# TODO: the API call should return not only law codes, but jurisprudence, norms, court decisions
def get_law_code_url(code: LawCode) -> str:
    if LawCode.forest:
        return "https://www.planalto.gov.br/ccivil_03/_Ato2011-2014/2012/Lei/L12651compilado.htm"
    elif LawCode.civil:
        return "https://www.planalto.gov.br/ccivil_03/Leis/2002/L10406compilada.htm"


async def get_html_content(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=(1, 30))
        response.raise_for_status()
        return response.text


async def get_law_code_raw_content(code: LawCode):
    url = get_law_code_url(code)
    html_content = await get_html_content(url)
    return html_content
