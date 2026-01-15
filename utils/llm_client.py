from langchain_groq import ChatGroq
from utils.config import Config

def get_llm(temperature=None, model=None):
    """Get Groq LLM instance"""
    return ChatGroq(
        groq_api_key=Config.GROQ_API_KEY,
        model_name=model or Config.MODEL_NAME,
        temperature=temperature or Config.TEMPERATURE,
        max_tokens=Config.MAX_TOKENS
    )

if __name__ == "__main__":
    llm = get_llm()
    response = llm.invoke("Say 'Hello from Research Paper Analyzer!'")
    print(response.content)