from helpers import read_transactions, get_item_dictionary, make_support_dictionary
from submission import large_itemsets, find_association_rules, apriori_gen

# Apriori gen should work correctly to find itemsets correctly
def test_apriori_gen():
    # Test if we generate items correctly, N = 1
    test_input = set([(1,), (5, ), (7, )])
    test_output = apriori_gen(test_input, N=1)
    assert len(test_output) == 3, "Apriori didn't generate candidates"
    assert all(len(item) == 2 for item in test_output), "Apriori generated incorrect length itemset(s)"
    # Test if we generate items correctly, N = 2
    test_input = set([(1, 2 ), (1, 3 ), (2, 3 ), (2, 7 ), (3, 7 ), (7, 9 ), (3, 9 )])
    test_output = apriori_gen(test_input, N=2)    
    assert all(len(item) == 3 for item in test_output), "Apriori generated incorrect length itemset(s)"
    # Generated items should be sorted
    assert all(sorted(item) == list(item) for item in test_output), "Apriori generated output is not sorted"
    # Itemsets should be tuples
    assert all(isinstance(item, tuple) for item in test_output), "Apriori generated itemset should be tuples"


# See what kind of itemsets data had
def print_large_itemsets(itemsets, item_mapping):
    print("\n===========================\nMost frequent itemset for each length:\n===========================")
    for key in itemsets.keys():
        if len(itemsets[key]) != 0:
            print("\nmost frequent combination of length {}".format(key))
            most_popular = max([(itemset.itemset, itemset.support) for itemset in itemsets[key]], key = lambda item: item[1])
            print(", ".join([item_mapping[item_id] for item_id in most_popular[0]]))

# See what kind of association rules were found
def print_most_confident_rules(recommendations, item_mapping):
    print("\nMost confident association rules:")
    recommendations = sorted(recommendations, key = lambda item : (item.confidence), reverse = True)
    for item in recommendations[:3]:
        body = ", ".join([item_mapping[item_id] for item_id in item.body])
        head = ", ".join([item_mapping[item_id] for item_id in item.head])
        
        print("with confidence {}: ({}) -> ({})".format(round(item.confidence,2), body, head))

if __name__ == "__main__":
    # To have correct output from frequent itemsets, apriori_gen should work as expected
    test_apriori_gen()

    # Read data
    database_transactions = read_transactions()
    item_mapping = get_item_dictionary()

    # Find all possible frequent itemsets
    itemsets = large_itemsets(database_transactions)
    print_large_itemsets(itemsets, item_mapping)

    # Based on the found itemsets, make a mapping from itemsets -> support count
    support_counts = make_support_dictionary(itemsets)

    print("\n===========================\nfinding association rules from the data\n===========================")
    for key in itemsets.keys():
        # Find association rules based on frequent itemsets and support counts that were discovered
        recommendations = find_association_rules(itemsets[key], support_counts)
        if len(recommendations) > 0:
            print("\nassociation rules from itemsets of length {}".format(key))
            print_most_confident_rules(recommendations, item_mapping)