import json
import collections


def main():
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

    all_categories = collections.defaultdict(int)
    with open('./yelp_academic_dataset_business.json', 'r') as data_file:
        for i, line in enumerate(data_file):
            business = json.loads(line)
            if business['city'] not in ('Pittsburgh', 'Charlotte', 'Phoenix', 'Las Vegas', 'Madison'):
                continue

            #  if i > 5:
            #      break
            #
            for category in business['categories']:
                if category in parent_categories:
                    for parent_category in parent_categories[category]:
                        all_categories[parent_category] += 1
                else:
                    all_categories['other'] += 1

    category_counts = [(v, k) for k, v in all_categories.iteritems()]
    category_counts.sort(reverse=True)
    print len(category_counts)  # 75 vs 71 in 5 cities
    for category_count in category_counts:
        print category_count

    """
    All data points
    (40019, u'restaurants')
    (15937, u'shopping')
    (12254, u'food')
    (10864, u'beautysvc')
    (7276, u'health')
    (7206, u'auto')
    (7114, u'homeservices')
    (6008, u'nightlife')
    (5020, u'fashion')
    (4738, u'localservices')
    ...
    ..
    .

    In 5 cities
    (19049, u'restaurants')
    (8088, u'shopping')
    (5792, u'food')
    (5538, u'beautysvc')
    (3761, u'auto')
    (3686, u'homeservices')
    (3538, u'health')
    (3072, u'nightlife')
    (2673, u'fashion')
    (2527, u'localservices')
    ...
    ..
    .
    """


if __name__ == '__main__':
    main()
