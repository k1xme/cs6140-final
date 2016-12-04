import collections
import json


def main():
    all_attributes = collections.defaultdict(int)
    attribute_values = collections.defaultdict(set)

    with open('./yelp_academic_dataset_business.json', 'r') as data_file:
        for i, line in enumerate(data_file):
            business = json.loads(line)
            #  if business['city'] not in ('Pittsburgh', 'Charlotte', 'Phoenix', 'Las Vegas', 'Madison'):
                #  continue

            for attribute, value in business['attributes'].iteritems():
                if not isinstance(value, dict):
                    if isinstance(value, bool) and value == False:
                        continue

                    all_attributes[attribute] += 1
                    attribute_values[attribute].add(value)
                else:
                    attribute_name = {'Good For': 'Good for',
                                      'Ambience': 'Ambience',
                                      'Music': 'Music',
                                      'Parking': 'Parking',
                                      'Hair Types Specialized In': 'Hair Types Specialized In',
                                      'Dietary Restrictions': 'Dietary Restrictions' }

                    for k, v in value.iteritems():
                        if v == False:
                            continue
                        combined_attribute = attribute_name[attribute] + ' ' + k
                        all_attributes[combined_attribute] += 1
                        attribute_values[combined_attribute].add(v)
            #  if i > 5:
                #  break

    attribute_pairs = [(v, k) for k, v in all_attributes.iteritems()]
    attribute_pairs.sort(reverse=True)
    print attribute_pairs
    for p in attribute_pairs:
        print p

    """

    (57507, u'Accepts Credit Cards')
    (54303, u'Price Range')
    (26246, u'Good for Kids')
    (25847, u'Take-out')
    (25399, u'Alcohol')
    (25125, u'Attire')
    (24790, u'Good For Groups')
    (23424, u'Wi-Fi')
    (22694, u'Wheelchair Accessible')
    (22679, u'Noise Level')
    (21919, u'Parking lot')
    ...
    ..
    .

    """
    #  for k, v in attribute_values.iteritems():
        #  print k, v

if __name__ == '__main__':
    main()
