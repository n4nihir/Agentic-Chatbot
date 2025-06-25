from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.langgraphagenticai.state.state import State 

class AiNewsNode:
    def __init__(self, llm):
        """
        Initialize the AI News Node with API keys for Tavily and GROQ
        """
        self.tavily = TavilyClient()
        self.llm = llm
        self.state = {}

    def fetch_news(self, state: dict)->dict:
        """
        Fetch AI news based on the specified frequency
        """

        frequency = state['messages'][0].content.lower()
        self.state['freqency'] = frequency
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'yearly': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'yearly': 365}
        time_range = time_range_map[frequency]
        days = days_map[frequency]

        # Fetch news articles from Tavily
        response = self.tavily.search(
            query = "Top Artificial Intelligence (AI) technology news India and globally",
            topic = "news",
            time_range = time_range,
            include_answer = "advanced",
            max_results = 20,
            days = days,
            # include_domains = ["techcrunch.com", "venturebeat.com/ai", ...]
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return self.state

    def summarize_news(self, state: dict)->dict:
        """
        Summarize the fetched news articles using an LLM.

        Args:
            state (State): The state of the graph containg 'news_data'

        Returns:
            State: The state of the graph containing the 'summarized news' key
        """
        news_data = self.state['news_data']
        system_prompt = """
        Summarize AI news articles into markdown format. For each item, include:
        - Date in **DD-MM-YYYY** format in IST timezone
        - Concise sentences summary from latest news
        - Sort news by date-wise (latest first)
        - Source URL as link
        Use format:
        ### [Date]
        - [Summary](URL)
        """

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Articles: \n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_data
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))

        state['summarized_news'] = response.content
        self.state['summarized_news'] = state['summarized_news']
        return self.state

    def save_result(self, state: dict)->dict:
        """
        Save the summarized news to a file.
        """
        frequency = self.state['freqency']
        summary = self.state['summarized_news']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state