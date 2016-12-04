import json
import pymongo

def main():
    client = pymongo.MongoClient()
    db = client.yelp_data
    biz = db.businesses
    cities = ['Pittsburgh', 'Charlotte', 'Phoenix', 'Las Vegas', 'Madison']
    with open('/home/kexi/yelp_data/yelp_academic_dataset_business.json') as f:
        for line in f:
            b = json.loads(line)
            if b['city'] in cities:
                loc = {'type': 'Point', 'coordinates': [b['longitude'], b['latitude']]}
                b['loc'] = loc
                biz.insert(b)

main()

