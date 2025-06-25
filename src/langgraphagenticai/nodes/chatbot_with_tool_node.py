from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self, llm):
        self.llm = llm

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response
            """
            return {"messages": [llm_with_tools.invoke(state['messages'])]}

        return chatbot_node