from langchain_community.tools.tavily_search import TavilySearchResults

def get_tool():
    """
    Return the list of tools to be used in the chatbot
    """
    tool = TavilySearchResults(max_results=2)
    return [tool]