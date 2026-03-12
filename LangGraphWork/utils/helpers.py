from langchain_openai import ChatOpenAI
import os

def get_llm():
    # OPENAI_API_KEY Environment variable is automatically used by ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return llm