import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Initialize session state history if not present
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Stream the graph response
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ("user", user_message)}):
                for value in event.values():
                    assistant_message = value["messages"].content

                    # Add messages to session history
                    st.session_state.chat_history.append(("user", user_message))
                    st.session_state.chat_history.append(("assistant", assistant_message))

        elif usecase == "Chatbot with Web Search":
            #Prepare state and invoke the graph
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            response = graph.invoke(initial_state)
            for msg in response["messages"]:
                if isinstance(msg, HumanMessage):
                    st.session_state.chat_history.append(("user", msg.content))
                elif isinstance(msg, ToolMessage):
                    st.session_state.chat_history.append(("ai", f"Tool call start \n {msg.content} \n Tool call end"))
                elif isinstance(msg, AIMessage) and msg.content:
                    st.session_state.chat_history.append(("assistant", msg.content))

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing AI news..."):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Add to chat history
                    st.session_state.chat_history.append(("user", frequency))
                    st.session_state.chat_history.append(("assistant", markdown_content))
                except FileNotFoundError:
                    st.error(f"Error: AI news summary file not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"Error: {e}")


        # Show chat history in a Streamlit container
        with st.container():
            for role, message in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(message)
