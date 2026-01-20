import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

st.set_page_config(page_title="Chat with Dataset", page_icon="📊")
st.title("Chat with Your Dataset")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")

    # API Key input
    api_key = st.text_input("OpenAI API Key", type="password")

    st.divider()

    # File upload
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(st.session_state.df)} rows")

    # Show data preview if loaded
    if st.session_state.df is not None:
        st.subheader("Data Preview")
        st.dataframe(st.session_state.df.head())
        st.caption(f"Shape: {st.session_state.df.shape[0]} rows × {st.session_state.df.shape[1]} columns")


def get_agent_response(df, question, api_key):
    """Get response from LangChain Pandas DataFrame Agent."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key
    )

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        agent_type="tool-calling",
        verbose=True,
        allow_dangerous_code=True
    )

    response = agent.invoke(question)
    return response["output"]


# Main chat area
if st.session_state.df is None:
    st.info("Please upload a CSV file in the sidebar to start chatting.")
elif not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar.")
else:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your data..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from agent
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Clear any existing figures
                    plt.close('all')

                    response = get_agent_response(
                        st.session_state.df,
                        prompt,
                        api_key
                    )
                    st.markdown(response)

                    # Check if a figure was created and display it
                    if plt.get_fignums():
                        st.pyplot(plt.gcf())
                        plt.close('all')

                except Exception as e:
                    response = f"Error: {str(e)}"
                    st.error(response)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
