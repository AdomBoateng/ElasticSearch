import os
import json
from elasticsearch_functions import connect_elasticsearch, index_documents, respond_to_intent

def load_documents_from_json(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    documents = load_documents_from_json('documents.json')
    es = connect_elasticsearch()
    index_name = "multiple_intents"
    index_documents(es, index_name, documents)

    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "exit":
            print("Goodbye!")
            break
        response = respond_to_intent(es, index_name, user_input)
        print("Bot:", response)
