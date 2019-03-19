"""
A tree kind structure to search for subsets of transactions

We know that transaction is sorted by id's which is why we can search them faster with this structure tree

assume a itemsets candidates of length(3):
C = {(1, 2, 3), (3, 4, 5), (1, 2, 4), (3, 5, 6)}

from which could construct a tree

 {(1)                (3)}               : Root dictionary (possible itemsets of len(1))
   .                  ..........
   .                  .        .
   .                  .        .
 {(1,2)             (3,4)    (3,5)}     : Bucket(s) dictionary (possible len(2) sets with respects to known itemsets)
   ...........        .        .
   .         .        .        .
   .         .        .        .
{(1,2,3), (1,2,4), (3,4,5), (3,5,6)}    : Leafs (all itemsets in C)

Because itemsets are sorted, we know that there cant be a itemset of length(3) where first item is one of (2,4,5,6)

Now given some transaction t = (t_1, t_2 ..... t_3) we can easily check which subsets of t are in C as if we take some
item t_i as item, we know that we cannot extend the itemset with item t_j, where j < i.
"""


class SubsetTree:

    def __init__(self, itemsets):
        self.root = Bucket(parent=None)
        self.large_itemsets = []

        # Construct the tree given a set of itemsets
        for itemset in itemsets:
            tmp = self.root.children
            tmp_key = str(itemset[0]) + ":"
            # Iterate a frequent itemset, until we traverced all items in the set
            for i in range(1, len(itemset)):
                if tmp_key not in tmp.keys():
                    tmp[tmp_key] = Bucket(parent=tmp)
                tmp = tmp[tmp_key].children
                tmp_key += str(itemset[i]) + ":"

            # Once we have all items in the set, make a new leaf node
            new_leaf = Leaf(itemset)
            self.large_itemsets.append(new_leaf)
            tmp[tmp_key] = new_leaf

    # Return all itemsets, so they can be iterated
    def fetch_candidate_itemsets(self):
        return self.large_itemsets[:]

    # Find all subsets with respect to some transaction
    def subset(self, transaction):
        C = set()
        # Make sure the transaction is sorted and iterate over it's items
        transaction = sorted(transaction)
        for i in range(len(transaction)):
            # Start the search from each index and consider all upcoming indices
            subsets = self.has_subset(self.root, "", transaction[i], transaction[i + 1:])
            # Append all found subsets to set C
            for item in subsets:
                C.add(item)
        return C

    # Recursive function that finds all subsets
    def has_subset(self, b, tmp_hash, item, others):
        tmp_hash += str(item) + ":"
        if tmp_hash not in b.children.keys():
            return
        if isinstance(b.children[tmp_hash], Leaf):
            yield b.children[tmp_hash]
            return
        for i in range(len(others)):
            solution = self.has_subset(b.children[tmp_hash], tmp_hash, others[i], others[i + 1:])
            for sol in solution:
                yield sol


# Intermediate node in the tree, where we map a set of intermediate length to (length + 1) based on child-dictionary
class Bucket:
    def __init__(self, parent):
        self.children = {}
        self.parent = parent


# Found itemsets of some given transactions and their support score
class Leaf:
    def __init__(self, items, support=0):
        self.itemset = items
        self.support = support

    def increment_support(self):
        self.support += 1

    def get_support_count(self):
        return self.support

