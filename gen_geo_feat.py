import pymongo
import pandas

yelp_db = pymongo.MongoClient().yelp_data
businesses = yelp_db.businesses
geo_feats = yelp_db.geo_feats
radius = 0.5/3963.2 # walking distance.
min_rating = 3.5

def count_category(nearby_biz, category):
    count = 0
    for biz in nearby_biz:
        if category in biz['categories']:
            count += 1
    return count

def count_high_rating_biz(nearby_biz):
    count = 0
    for biz in nearby_biz:
        if biz['stars'] >= min_rating:
            count += 1
    return count

def main():
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


