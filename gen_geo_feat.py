import pymongo
import json
import collections

yelp_db = pymongo.MongoClient().yelp_data
businesses = yelp_db.businesses
geo_feats = yelp_db.geo_feats
radius = 0.5/3963.2 # walking distance.
min_rating = 3.5
parent_categories = collections.defaultdict(set)

def get_parent_categories():
    with open('./categories.json') as all_category_file:
        for i, category in enumerate(json.loads(all_category_file.read())):
            if 'country_whitelist' in category and \
               'US' not in category['country_whitelist']:
                continue

            if 'country_blacklist' in category and \
               'US' in category['country_blacklist']:
                continue

            parent_categories[category['title']] |= set(category['parents'])
            parent_categories[category['alias']] |= set(category['parents'])

def count_category(nearby_biz, target):
    count = 0
    for biz in nearby_biz:
        for c in biz['categories']:
            if c in parent_categories and target in parent_categories[c]: count += 1
    return count

def count_high_rating_biz(nearby_biz):
    count = 0
    for biz in nearby_biz:
        if biz['stars'] >= min_rating:
            count += 1
    return count

def main():
    get_parent_categories()
    count = 0
    geo_feat_docs = []
    for biz in businesses.find():
        coordinates = biz["loc"]["coordinates"]
        cond = {"$and": [{"loc": {"$geoWithin": {"$centerSphere":[coordinates, radius]}}}]}
        nearby_biz = list(businesses.find(cond))
        feat_doc = {
                "business_id": biz["business_id"],
                "num_nearby_biz": len(nearby_biz),
                "num_shopping": count_category(nearby_biz, "shopping"),
                "num_restaurants": count_category(nearby_biz, "restaurants"),
                "num_food": count_category(nearby_biz, "food"),
                "num_nightlife": count_category(nearby_biz, "nightlife"),
                "num_high_rating_biz": count_high_rating_biz(nearby_biz)}
        geo_feat_docs.append(feat_doc)
        count += 1
        print count
    geo_feats.insert_many(geo_feat_docs)

main()


