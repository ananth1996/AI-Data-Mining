from subsetTree import Leaf

# return a combined list if two lists share (N-1) items
def all_but_one(A, B):
    assert len(A) == len(B)
    N = len(A)
    A = list(A)
    # We want to keep the items sorted, so that we can search the list more efficiently
    combined_list = tuple(sorted(A + [item for item in B if item not in A]))
    # Combined length can be (N+1) only when two lists have 1 different elements
    if len(combined_list) == (N+1):
        return combined_list
    else:
        return None


# Read all transactions to a list
def read_transactions(path="data/transactions.csv"):
    transactions = []
    with open(path, 'r') as f:
        for line in f:
            # Transactions are separated by spaces
            tmp = [int(i) for i in line.split()]
            transactions.append(tmp)
    return transactions


# Make dictionary mapping from item -> description
def get_item_dictionary(path="data/items.csv"):
    item_dictionary = {}
    with open(path, 'r') as f:
        for line in f:
            # All items are contained in items.csv with (id, description)
            tmp = line.split(",")
            item_dictionary[int(tmp[0])] = tmp[1].strip()
    return item_dictionary


# Make dictionary as large itemset as key mapped to its support count
def make_support_dictionary(large_itemsets):
    support_dictionary = {}
    for level in large_itemsets.keys():
        for itemset in large_itemsets[level]:
            support_dictionary[itemset.itemset] = itemset.support

    return support_dictionary


# make set L_1 that contains items and their counts
def make_large_one_item_sets(transactions, min_support):
    L_1 = set()
    one_item_sets = set()
    all_items = set([item for transaction in transactions for item in transaction])
    for item in all_items:
        support = sum(x.count(item) for x in transactions)
        if support >= min_support:
            one_item_sets.add(Leaf((item, ), support=support))
            L_1.add((item, ))

    return L_1, one_item_sets
