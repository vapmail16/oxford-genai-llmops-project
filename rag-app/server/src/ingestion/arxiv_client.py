import requests
import xml.etree.ElementTree as ET

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def fetch_papers(query: str, max_results: int = 10):
    """
    Fetch papers from the arXiv API based on a query.
    
    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to fetch.
        
    Returns:
        list: A list of dictionaries with paper titles and summaries.
    """
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results
    }
    
    response = requests.get(ARXIV_API_URL, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    
    # Parse the XML response
    root = ET.fromstring(response.content)
    papers = []

    # Iterate over each entry in the XML feed
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        papers.append({"title": title.strip(), "summary": summary.strip()})
    
    return papers

if __name__=="__main__":
    papers = fetch_papers(query="ti:perovskite", max_results=10)
    print(papers)