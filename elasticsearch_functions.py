from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

def connect_elasticsearch():
    load_dotenv()
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
    es = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.getenv("ca_certs"),
        basic_auth=("elastic", ELASTIC_PASSWORD)
    )
    return es

def index_documents(es, index_name, documents):
    for doc in documents:
        es.index(index=index_name, body=doc)

def respond_to_intent(es, index_name, user_input):
    search_query = {
        "query": {
            "multi_match": {
                "query": user_input,
                "fields": ["intentions"]
            }
        }
    }

    response = es.search(index=index_name, body=search_query)

    if response['hits']['total']['value'] > 0:
        hit = response['hits']['hits'][0]
        response_text = hit['_source']['response']
        return response_text
    else:
        return "Sorry, I didn't understand that. Can you repeat it?"
