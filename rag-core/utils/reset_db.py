import weaviate
from config.settings import WEAVIATE_URL, WEAVIATE_INDEX_NAME

def reset_knowledge_base():
    print(f"Connecting to Weaviate at {WEAVIATE_URL}...")
    client = weaviate.connect_to_local(port=8080, grpc_port=50051)

    try:
        # Check if the collection (index) exists
        if client.collections.exists(WEAVIATE_INDEX_NAME):
            print(f"Deleting existing index: '{WEAVIATE_INDEX_NAME}'...")
            client.collections.delete(WEAVIATE_INDEX_NAME)
            print("Database wiped clean.")
        else:
            print(f"Index '{WEAVIATE_INDEX_NAME}' did not exist. Nothing to delete.")
            
    except Exception as e:
        print(f"Error resetting DB: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    confirm = input("Are you sure you want to DELETE all data? (yes/no): ")
    if confirm.lower() == "yes":
        reset_knowledge_base()
    else:
        print("Operation cancelled.")