"""
Minimal ReAct agent template for the AI Agents workshop.
You'll extend this in later labs.
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
# from langchain.agents import Tool
from langgraph.prebuilt import create_react_agent

# from tools.add import add_function
from tools.search import exa_search

# Load environment variables from .env file
load_dotenv()

def create_agent():
    llm = ChatOpenAI(model_name="qwen/qwen3-coder:free", temperature=0, base_url="https://openrouter.ai/api/v1")

    checkpointer = MemorySaver()

    tools = [exa_search]  # You'll register a search tool in Lab 2
    
    # Create ReAct agent with LangGraph (eliminates deprecation warnings)
    agent = create_react_agent(llm, tools, checkpointer=checkpointer, verbose=True, prompt="Always use the tools provided to you. If you don't have the information, say you don't know. If you have the information, use the tools to get the information.")
    return agent

if __name__ == "__main__":
    agent = create_agent()
    print("Welcome to your ReAct agent. Type 'quit' to exit.")
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.lower() in {'quit', 'exit'}:
            print("Goodbye!")
            break
        try:
            config = {"configurable": {"thread_id": "first_thread"}}
            
            # LangGraph uses invoke with messages format
            response = agent.invoke({"messages": [("human", user_input)]}, config=config, print_mode="tree")
            # Extract the final AI message from the response
            final_message = response["messages"][-1].content
            print("Agent:", final_message)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
