from langchain_openai import ChatOpenAI

def get_llm():
    # OPENAI_API_KEY Environment variable is automatically used by ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0,
        max_tokens=2048,
    )
    return llm