import sys
from retrieval.qa import generate_answer
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
# ... rest of your imports

def start_chat():
    print("--- Local RAG System Initialized ---")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            # 1. Get user input
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            # 2. Generate Answer
            response = generate_answer(user_input)

            # 3. Print Output
            print(f"\nAI: {response}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_chat()