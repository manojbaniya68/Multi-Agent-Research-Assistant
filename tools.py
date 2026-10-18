from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch
from rich import print
from bs4 import BeautifulSoup
import requests

load_dotenv()


@tool
def web_search(topic: str) -> str:
    """Search the web and get relavent titles, urls and content of given search topic"""
    tool = TavilySearch(
        max_results=3,
        topic="general"
    )

    search_result = tool.invoke({"query": topic})
    results = search_result['results']
    search_result_list = []

    for r in results:
        search_result_list.append(
            f"\n title: {r['title']} \n url: {r['url']} \n content: {r['content'][:100]}"
        )

    return "\n\n".join(search_result_list)


@tool
def scrap_url(url: str) -> str:
    """Scrapes the information of provided urls and returns the meaningful content"""
    response = requests.get(url, timeout=15, headers={"User-Agent" : "Mozilla/5.0"})
    soup = BeautifulSoup(response.text,"html.parser")

    # Remove unnecessary elements
    for element in soup(["script", "style", "nav", "footer","header", "aside", "noscript"]):
        element.decompose()

    # Extract the page title
    title = soup.title.get_text(strip=True) if soup.title else "No title"
    content = soup.get_text(" ", strip=True)

    if not content:
        return "No readable content found on this webpage."

    # Limit content to avoid overwhelming the LLM
    content = content[:3000]

    return f"Page title: {title}\n\nContent:\n{content}"







