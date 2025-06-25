from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.tool import get_tool
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from langgraph.prebuilt import ToolNode
from src.langgraphagenticai.nodes.ai_news_node import AiNewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the
        entry and exit points of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanceed chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set as the entry point.
        """
        #Defining tool and tool node

        tools = get_tool()

        tools_node = ToolNode(tools)

        ## Define the LLM
        llm = self.llm

        ## Define the chatbot node
        obj_chatbot_with_tools_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_tools_node.create_chatbot(tools)

        ## Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tools_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition
        )
        self.graph_builder.add_edge("tools", "chatbot")

    
    def ai_news_build_graph(self):
        """
        Builds an AI news graph with tool integration.
        This method creates a chatbot graph that includes a fetch_news node,
        a summarize_news node, and a save_result node. It sets up direct edges
        between nodes. The fetch_news node is set as the entry point.
        """
        ai_news_node = AiNewsNode(self.llm)

        # Add nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        # Add edges
        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)


    def setup_graph(self, usecase:str):
        """
        Sets up the graph for the selected use case
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        if usecase == "Chatbot with Web Search":
            self.chatbot_with_tools_build_graph()

        if usecase == "AI News":
            self.ai_news_build_graph()

        return self.graph_builder.compile()