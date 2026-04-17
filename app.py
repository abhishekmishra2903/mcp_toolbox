import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic import hub
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from toolbox_langchain import ToolboxClient

# 1. Load environment variables from the .env file (picks up OPENAI_API_KEY)
load_dotenv()

st.set_page_config(page_title="MCP Toolbox Demo", page_icon="🛠️")
st.title("🛠️ OpenAI MCP Toolbox Demo")
st.markdown("This UI securely connects to Google's **GenAI Toolbox** via the `toolbox-langchain` SDK. Watch the agent use the Toolbox to query your database dynamically!")

# 2. The "Magic" - Fetch the secure tools dynamically from the GenAI Toolbox Docker container
@st.cache_resource
def load_toolbox():
    # Instantiate the client directly so it stays alive in the background
    client = ToolboxClient("http://localhost:8080")
    
    # Load and return the tools
    return client.load_toolset()

try:
    toolbox_tools = load_toolbox()
except Exception as e:
    st.error(f"Could not connect to GenAI Toolbox. Is the Docker container running? Error: {e}")
    st.stop()

# 3. Initialize the LLM and the modern Agent setup
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Pull a standard prompt for tool-calling agents
prompt = hub.pull("hwchase17/openai-tools-agent")

# Create the modern agent using ONLY the secure MCP tools
agent = create_tool_calling_agent(llm, toolbox_tools, prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolbox_tools,
    verbose=True,
    handle_parsing_errors=True
)

# 4. The Chat Interface
if user_prompt := st.chat_input("Ask about book genres..."):
    st.chat_message("user").write(user_prompt)
    
    with st.chat_message("assistant"):
        # Create a status container for a cleaner "thinking" experience
        with st.status("Solving your request...", expanded=True) as status:
            # Pass this specific container to the handler
            st_callback = StreamlitCallbackHandler(st.container())
            
            response = agent_executor.invoke(
                {"input": user_prompt},
                config={"callbacks": [st_callback]}
            )
            # Once done, change the status to 'complete'
            status.update(label="Analysis Complete!", state="complete", expanded=False)
        
        # Display the final answer outside the status box
        st.write(response["output"])