from redisearch import Client, Query
import redis
from scripts.ver import thai_subword_tokenize, thai_ngram, search_tokenize


# Connect to Redis
r = redis.Redis(host='localhost', port=6379)
client = Client('myIndex', conn=r)

# Function to search by name with advanced querying and prefix boost
def search_name(name, client=client, page=0, limit=10):
    # Tokenize the query for Thai

    subword_tokenized = thai_subword_tokenize(name)
    ngram_tokenized = thai_ngram(name, 4, 1)

    query = f"{name}*"
    ngram_query = f"{' '.join([f"{ngram}" for ngram in ngram_tokenized])}" # {' '.join([f"{word}" for word in syllable_tokenized])}

     
    
    # Create a query with advanced features
    query_obj = Query(query).limit_fields('tokenized').paging(page*limit, limit).verbatim()
    ngram_query_obj = Query(ngram_query).limit_fields('tokenized').verbatim().in_order()


    # Perform the search
    if len(subword_tokenized) > 3:
        print(f"Fuzzy Query: {ngram_query}")
        result = client.search(ngram_query_obj)
    else:
        print(f"Query: {query}")
        result = client.search(query_obj)
    
    return result.docs, result.total

# # Example searches
if __name__ == "__main__":
    print("Search results :")
    result, total = search_name('โรงเรียน', page=0, limit=10)
    print(f"Total hits: {total}")
    for doc in result:
        print(f"Document name: {doc.name}, location: {doc.location}")

