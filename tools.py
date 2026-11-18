from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=tavily_api_key)

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic. Returns Titles, URLS, and Snippets of the top results. If no results are found, returns a message indicating that. 
    """
    results = tavily.search(query, max_results=5)

    out = []

    for r in results['results']:
        title = r.get('title', 'No title found')
        url = r.get('url', 'No URL found')
        snippet = r.get('content', 'No snippet found')[:300]
        out.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")

    return "\n----\n".join(out)
    # try:
    #     results = tavily.search(query, max_results=5)
    #     if results and len(results) > 0:
    #         return results[0].get("url", "No URL found")
    #     else:
    #         return "No results found"
    # except Exception as e:
    #     return f"An error occurred during the search: {str(e)}"

print(web_search.invoke("Latest advancements in AI technology"))

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text from a given URL for deeper reading.
    """
    try:
        response = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            tag.decompose()  # Remove elements
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content[:1000]  # Return first 1000 characters for brevity
    except Exception as e:
        return f"An error occurred while scraping the URL: {str(e)}"

