import json
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost/')
db = client.hw_web10

if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for author in data:
            db.authors.insert_one({
                'fullname': author['fullname'].replace('-', ''),
                'born_date': author['born_date'],
                'born_location': author['born_location'],
                'description': author['description']
            })

    with open('quotes.json', 'r', encoding='utf8') as fd:
        quotes = json.load(fd)

    for quote in quotes:
        author = db.authors.find_one({'fullname': quote['author']})
        if author:
            db.quotes.insert_one({
                'quote': quote['quote'],
                'tags': quote['tags'],
                'author': ObjectId(author['_id'])
            })
