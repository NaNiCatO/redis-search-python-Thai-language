import redis
from redisearch import Client, TextField
import pandas as pd
from scripts.ver import thai_subword_tokenize, thai_ngram

# Read the CSV file
df = pd.read_csv('data/full_test.csv')

# Connect to Redis
r = redis.Redis(host='localhost', port=6379)
client = Client('myIndex', conn=r)

# Drop the index if it exists
try:
    client.drop_index()
except:
    pass

# Create the index
schema = (TextField('tokenized', weight=5.0),)
client.create_index(schema)

# Load data into Redis
for index, row in df.iterrows():
    # subword_tokenized = ' '.join(thai_subword_tokenize(row['name']))
    # word_tokenized = ' '.join(syllable_tokenize(row['name'], engine='han_solo'))
    ngram_tokenized = ' '.join(thai_ngram(row['name'], 4, 1))
    tokenized = f"{ngram_tokenized}"
    client.add_document(
        f"doc{index}",
        name=row['name'],
        tokenized=tokenized,  
        location=f"{row['lat']},{row['long']}",
    )

print("Data loaded into Redis")

