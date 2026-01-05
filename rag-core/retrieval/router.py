from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config.settings import OLLAMA_BASE_URL, LLM_MODEL

def route_query(query):
    """
    Uses the LLM to semantically classify the user's intent.
    """
    print("Analyzing intent...")
    
    llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    
    # Engineering Prompt: Few-Shot Prompting
    # We give it examples so it learns the pattern instantly.
    router_template = """You are a routing system. Classify the following user query into one of two categories:
    
    [WEB]: For questions about current events, companies, stock prices, weather, news, or general world knowledge not in a resume.
    [LOCAL]: For questions about "Jinish", "Resumes", "Skills", "Contact Info", "Projects", "Experience", or "Internships".
    
    Examples:
    Q: "Who is Jinish?" -> [LOCAL]
    Q: "Latest news on Apple" -> [WEB]
    Q: "Tell me about his python skills" -> [LOCAL]
    Q: "What is the stock price of Tesla?" -> [WEB]
    
    Query: {question}
    
    Classification (Respond ONLY with [WEB] or [LOCAL]):"""

    prompt = ChatPromptTemplate.from_template(router_template)
    chain = prompt | llm
    
    response = chain.invoke({"question": query})
    
    # Cleaning the response (LLMs sometimes add extra spaces)
    decision = response.strip().upper()
    
    if "[WEB]" in decision:
        return "WEB"
    else:
        return "LOCAL"