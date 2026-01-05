from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config.settings import OLLAMA_BASE_URL, LLM_MODEL
from retrieval.retriever import retrieve_context

def format_docs(docs):
    """
    Takes a list of documents and joins their content into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def generate_answer(query):
    """
    The Full RAG Chain:
    1. Retrieve docs
    2. Format docs
    3. Send to LLM -> Return Answer
    """
    print(f"thinking... (Asking {LLM_MODEL})")
    
    # 1. Setup the LLM (Phi3)
    llm = OllamaLLM(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL
    )

    # 2. Create the Prompt Template
    # We tell the AI exactly how to behave
    template = """You are a helpful assistant. Use the following context to answer the question.
    If you don't know the answer, just say that you don't know.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    # 3. Retrieve context manually first (so we can print it if we want)
    relevant_docs = retrieve_context(query)
    formatted_context = format_docs(relevant_docs)

    # 4. Run the Chain
    # We feed the context and question into the prompt, then to the LLM
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "context": formatted_context,
        "question": query
    })

    return response

if __name__ == "__main__":
    test_query = "What did Jinish do at Abrossit?"
    answer = generate_answer(test_query)
    
    print("\n=== FINAL ANSWER ===")
    print(answer)