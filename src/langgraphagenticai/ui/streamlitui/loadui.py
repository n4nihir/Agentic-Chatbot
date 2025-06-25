import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}
        st.session_state.IsFetchButtonClicked = False
        st.session_state.time_frame = None

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖" + self.config.get_page_title(), layout="wide")
        st.header("🤖" + self.config.get_page_title())

        with st.sidebar:
            # Get options from config file
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM Selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options, index=0)

            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options, index=0)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("GROQ API Key", type="password", placeholder="Enter your GROQ API Key")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API Key to proceed. Don't have one? Get it from https://console.groq.com/keys")

            #Use Case Selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Use Case", usecase_options, index=0)

            if self.user_controls["selected_usecase"] == "Chatbot with Web Search" or self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API Key", type="password", placeholder="Enter your TAVILY API Key")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("⚠️ Please enter your TAVILY API Key to proceed. Don't have one? Get it from https://app.tavily.com/home")
            if self.user_controls["selected_usecase"] == "AI News":
                with st.sidebar:
                    time_frame = st.selectbox(
                        "Select Time Frame",
                        ["Daily", "Weekly", "Monthly"],
                        index=0
                    )

                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.time_frame = time_frame


        return self.user_controls