from itertools import chain
import pickle
from tqdm import *
import os.path
import operator
import ast
from math import sqrt
from prediction_testing import fscore, mean_avg_p


def build_dictionaries(training_file):
    item_purchase_dict = {}
    customer_purchase_dict = {}
    item_category_dict = {}
    with open(training_file) as training_data:
        for line in training_data.readlines():
            cust_ID, item_ID, rating = line[:22].split()
            categories = ast.literal_eval(line[22:])[0]
            if customer_purchase_dict.get(cust_ID):
                customer_purchase_dict[cust_ID].append((item_ID, rating))
            else:
                customer_purchase_dict[cust_ID] = [(item_ID, rating)]
            if item_purchase_dict.get(item_ID):
                item_purchase_dict[item_ID].append(cust_ID)
            else:
                item_purchase_dict[item_ID] = [cust_ID]

            if item_category_dict.get(item_ID):
                item_category_dict[item_ID].update(categories)
            else:
                item_category_dict[item_ID] = set(categories)

    return item_purchase_dict, customer_purchase_dict, item_category_dict


def item_rating_dict(training_file):
    item_avg_rating = {}
    with open(training_file) as training_data:
        for line in training_data.readlines():
            cust_ID, item_ID, rating = line[:22].split()
            if item_avg_rating.get(item_ID):
                item_avg_rating[item_ID].append(int(rating))
            else:
                item_avg_rating[item_ID] = [int(rating)]
    item_avg_rating = {item: sum(ratings)/len(ratings) for item, ratings in item_avg_rating.items()}
    return item_avg_rating

"""
def weight_similar(items_to_customers, customers_to_items):
    customer_weighted_similar = {}
    for customer, purchases in tqdm(customers_to_items.items()):
        similar_customers = {cust: 0 for cust in set(chain(*[items_to_customers[item] for item[0] in purchases]))}
        for similar_customer in similar_customers:
            for purchase in purchases:
                if similar_customer in items_to_customers[purchase[0]]:
                    similar_customers[similar_customer] += 1

        customer_weighted_similar[customer] = similar_customers
    return customer_weighted_similar
"""

def load_data(datafile):
    if datafile == "cust_similar.p":
        if os.path.isfile("cust_similar.p"):
            print("loading <cust_similar> from datastore")
            customer_to_similar_customers = pickle.load(open("cust_similar.p", "rb"))
            print("data loaded")
            return customer_to_similar_customers
        else:
            print("generating <cust similar>")
            items_to_customers = load_data("items_to_cust.p")
            customers_to_items = load_data("cust_to_items.p")
            customer_to_similar_customers = weight_similar(items_to_customers, customers_to_items)
            print("dumping data to store")
            pickle.dump(customer_to_similar_customers, open("cust_similar.p", "wb"))
            print("data dumped")

    elif datafile == "items_to_cust.p":
        if os.path.isfile("items_to_cust.p"):
            print("loading <items_to_cust> from datastore")
            items_to_customers = pickle.load(open("items_to_cust.p", "rb"))
            print("data loaded")
            return items_to_customers
        else:
            print("generating <items to cust>")
            items_to_customers, _, _ = build_dictionaries("training_data_simple.txt")
            print("dumping to data store")
            pickle.dump(items_to_customers, open("items_to_cust.p", "wb"))
            print("data dumped")

    elif datafile == "cust_to_items.p":
        if os.path.isfile("cust_to_items.p"):
            print("loading <cust_to_items> from datastore")
            customers_to_items = pickle.load(open("cust_to_items.p", "rb"))
            print("data loaded")
            return customers_to_items
        else:
            print("generating <cust_to_items>")
            _, customers_to_items, _ = build_dictionaries("training_data_simple.txt")
            print("dumping to data store")
            pickle.dump(customers_to_items, open("cust_to_items.p", "wb"))
            print("data dumped")
    elif datafile == "items_to_cata.p":
            if os.path.isfile("items_to_cata.p"):
                print("loading <items to cata> from datastore")
                items_to_cata = pickle.load(open("items_to_cata.p", "rb"))
                print("data loaded")
                return items_to_cata
            else:
                print("generating <items to cata>")
                _, _, items_to_cata = build_dictionaries("training_data_simple.txt")
                print("dumping to data store")
                pickle.dump(items_to_cata, open("items_to_cata.p", "wb"))
                print("data dumped")


def compute_customer_similarity_vector(cust_ID, item_ID, customer_to_similar_customers, cust_to_items, overlap):
    purchase_vector = []
    top_similar_customers = [customer for customer in sorted(customer_to_similar_customers[cust_ID].items(), key=operator.itemgetter(1), reverse=True) if customer[1] > overlap][1:]
    for customer in top_similar_customers:
        for ID_rating_pair in cust_to_items[customer[0]]:
            if item_ID == ID_rating_pair[0]:
                purchase_vector.append(customer[1])
    return purchase_vector


def generate_lookup(cust_to_items):
    rating_lookup_table = {customer: {item: int(rating) for item, rating in customer_items} for customer, customer_items in cust_to_items.items()}
    average_lookup_table = {customer: (sum(rating_lookup_table[customer].values())/len(items)) for customer, items in cust_to_items.items()}
    return rating_lookup_table, average_lookup_table


def pearson_correlation(cust_to_items):
    print("generating lookup tables")
    rating_lookup_table, avg_lookup_table = generate_lookup(cust_to_items)
    print("building cor-vectorspace")
    cust_to_correlationvector = {customer: {} for customer in cust_to_items.keys()}
    print("constructs created")
    for customer_i, customer_i_items in tqdm(cust_to_items.items()):
        customer_i_item_set = set(rating_lookup_table[customer_i].keys())
        for customer_j, customer_j_items in cust_to_items.items():
            if (customer_j == customer_i) or (rating_lookup_table[customer_j] is None):
                continue
            numerator = 0
            denominator_i = 0
            denominator_j = 0
            for item in customer_i_item_set.intersection(rating_lookup_table[customer_j].keys()):
                cust_i_item_rating = rating_lookup_table[customer_i][item]
                cust_j_item_rating = rating_lookup_table[customer_j][item]
                cust_i_avg = avg_lookup_table[customer_i]
                cust_j_avg = avg_lookup_table[customer_j]

                numerator += (cust_i_item_rating - cust_i_avg)*(cust_j_item_rating - cust_j_avg)
                denominator_i += (cust_i_item_rating - cust_i_avg)**2
                denominator_j += (cust_j_item_rating - cust_j_avg)**2
            if numerator == 0:
                cust_to_correlationvector[customer_i][customer_j] = 0
                cust_to_correlationvector[customer_j][customer_i] = 0
                continue
            denominator = sqrt(denominator_i) * sqrt(denominator_j)
            cust_to_correlationvector[customer_i][customer_j] = numerator/denominator if denominator != 0 else 0
            cust_to_correlationvector[customer_j][customer_i] = numerator/denominator if denominator != 0 else 0
        rating_lookup_table[customer_i] = None

    return cust_to_correlationvector


def single_pearson(customer_i, rating_lookup_table, avg_lookup_table, cust_to_items):
    customer_i_item_set = set(rating_lookup_table[customer_i].keys())
    correlation_vector = {}
    for customer_j, customer_j_items in tqdm(cust_to_items.items()):
            if (customer_j == customer_i) or (len(customer_j_items) < 2):
                continue
            numerator = 0
            denominator_i = 0
            denominator_j = 0
            for item in customer_i_item_set.intersection(rating_lookup_table[customer_j].keys()):
                cust_i_item_rating = rating_lookup_table[customer_i][item]
                cust_j_item_rating = rating_lookup_table[customer_j][item]
                cust_i_avg = avg_lookup_table[customer_i]
                cust_j_avg = avg_lookup_table[customer_j]

                numerator += (cust_i_item_rating - cust_i_avg)*(cust_j_item_rating - cust_j_avg)
                denominator_i += (cust_i_item_rating - cust_i_avg)**2
                denominator_j += (cust_j_item_rating - cust_j_avg)**2
            if numerator == 0:
                continue
            correlation_vector[customer_j] = numerator/(sqrt(denominator_i) * sqrt(denominator_j))
    return correlation_vector


def prediction_algorithm(customer_to_similar_customers, cust_to_items, items_to_cata, outfile, test_val):
    with open("testing_data.txt", "r") as testing_data:
        for line in tqdm(testing_data.readlines()):
            cust_ID, item_ID, _, _ = line.split()
            score = 0
            avg = 0
            for item in cust_to_items[cust_ID]:
                intersection = set(items_to_cata[item[0]]).intersection(items_to_cata[item_ID])
                avg += len(intersection)
            avg /= len(cust_to_items[cust_ID])
            score += avg
            #score += item_avg[item_ID]
            # ic_avg = 0
            # counter = 0
            # for customer in items_to_cust[item_ID]:
            #     if len(cust_to_items[customer]) > 1:
            #         counter += 1
            #         customer_items = set(map(lambda x: x[0], cust_to_items[customer]))
            #         ic_avg += len(customer_items.intersection(map(lambda x: x[0], cust_to_items[cust_ID])))
            #
            # if counter:
            #     score += ic_avg / counter
            csv = compute_customer_similarity_vector(cust_ID, item_ID, customer_to_similar_customers, cust_to_items, 2)
            if csv:
                score += len(csv)
            if score > test_val:
                outfile.write("{} {} 1 {}\n".format(cust_ID, item_ID, score))
            else:
                outfile.write("{} {} 0 {}\n".format(cust_ID, item_ID, score))


def main():
    customer_to_similar_customers = load_data("cust_similar.p")
    #items_to_cust = load_data("items_to_cust.p")
    cust_to_items = load_data("cust_to_items.p")
    items_to_cata = load_data("items_to_cata.p")
    result_file = open("results.txt", "w+")
    #rating_lookup_table, avg_lookup_table = generate_lookup(cust_to_items)
    outfile = open("outfile.txt", "w+")
    prediction_algorithm(customer_to_similar_customers, cust_to_items, items_to_cata, outfile, 6)
    outfile.close()
    result_file.write(fscore("outfile.txt", "testing_data.txt"))
    result_file.write(mean_avg_p("outfile.txt", "testing_data.txt"))
    #os.remove("outfile.txt")
    result_file.close()

if __name__ == '__main__':
    main()
