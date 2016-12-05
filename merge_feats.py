import pymongo

db = pymongo.MongoClient().yelp_data
businesses = db.businesses
geo_feats = db.geo_feats
formatted_data = db.formatted_data

def main():
    bulk_updater = formatted_data.initialize_unordered_bulk_op()
    for geo_feat in geo_feats.find():
        _id = geo_feat.pop("business_id")
        geo_feat.pop("_id")
        bulk_updater.find({"business_id": _id}).update_one({"$set": geo_feat})

    try:
        result = bulk_updater.execute()
        print result
    except Exception as e:
        print e

main()
