import collections
import json
import pymongo
import csv


def main():
    client = pymongo.MongoClient()
    db = client.yelp_data
    original_data = db.businesses
    formatted_data = db.formatted_data

    parent_categories = read_parent_category()

    cursor = original_data.find({})
    formatted_docs = [convert(document, parent_categories) for document in cursor]
    #  formatted_data.insert_many(formatted_docs)

    out_file = open('training_data.csv', 'wb')
    fieldnames = sorted(list(set(k for d in formatted_docs for k in d)))
    writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')

    writer.writeheader() # Assumes Python >= 2.7
    for row in formatted_docs:
        writer.writerow(row)
    out_file.close()

def read_parent_category():
    parent_categories = collections.defaultdict(set)
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
    return parent_categories


def convert(doc, parent_categories):
    new_doc = {
            'restaurants': False,
            'shopping': False,
            'food': False,
            'beautysvc': False,
            'health': False,
            'auto': False,
            'homeservices': False,
            'nightlife': False,
            'fashion': False,
            'localservices': False,
            'other': False,
            'Accepts Credit Cards': False,
            'Price Range': 0,
            'Good for Kids': False,
            'Take-out': False,
            'Alcohol': 'Not specified',
            'Wheelchair Accessible': False,
            'Attire': 'Not specified',
            'Good For Groups': False,
            'Parking lot': False,
            'Wi-Fi': False,
            'Noise Level': 'Not specified',
            'Success': False
        }

    other_category = True
    for category in doc['categories']:
        if category in parent_categories:
            for parent_category in parent_categories[category]:
                if parent_category in new_doc:
                    new_doc[parent_category] = True
                    other_category = False
    new_doc['other'] = other_category

    for attribute, value in doc['attributes'].iteritems():
        if attribute in new_doc:
            new_doc[attribute] = value

    new_doc.pop('_id')
    new_doc['Success'] = (doc['review_count'] >= 40 and doc['stars'] >= 4)
    return new_doc


if __name__ == '__main__':
    main()
