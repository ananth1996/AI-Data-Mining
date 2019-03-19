# Dont modify the import statements!
import itertools 
from helpers import all_but_one, make_large_one_item_sets
from subsetTree import SubsetTree


# APRIORI-GEN: Generate itemset candidates of length (N + 1)
def apriori_gen(L_prev, N=1):
    # INPUT:
    #   - L_prev    :   (set()) large itemsets of length N
    #   - N         :   (int) Size of the large itemsets in L_prev
    # OUTPUT:
    #   - L_next    :   (set()) Large itemsets of length (N + 1), itemsets should be sorted

    # We want to use sets for itemsets, because containment can be checked in time O(1) on average
    prev_itemset_list = list(L_prev)
    L_next = set()

    # 1 - Go over all items in previous itemset
    for i in range(len(prev_itemset_list)):
        # Notice that itemsets that we output should be sorted
        # Then: to make all possible pairs we only need to consider pairs (i,j) where j > i
        query = prev_itemset_list[i]
        extension_candidates = prev_itemset_list[i + 1:]
        # ============= TODO: ========================
        # See chapter 9.2 for AprioriGen() details
        #   
        # Your implementation should:
        # 
        # 1. Go over all itemsets in L_prev and join 
        # them together if they share all but 1 item. 
        #   - Combined itemsets should be sorted
        #
        # 2. If two lists can be combined, make sure that 
        # all possible subsets of length N are found in L_prev.
        # if all subsets are contained in L_prev, add the combined 
        # item to L_next
        #   
        # 3. As L_next is a set, we cannot use lists. Instead use a tuple() 
        #   - if you use all_but_one() it already returns sorted tuples that can be used for itemset candidates
        # 
        # Hints:
        #   - use all_but_one(A, B) to combine two lists A, B
        #       - all_but_one returns combined tuple if A, B share all but 1 item, else it returns None
        #       - output itemset is already sorted
        #
        #   - You can use: list(itertools.combinations(itemset, N)) to get all subsets of length N 
        #       - itemset is iteraple: this can be output of all_but_one(..)
    return L_next


# LARGE_ITEMSETS: Generate large itemsets
def large_itemsets(transactions, min_support=0.001):
    # INPUT:
    #   - transactions      :   list of all transactions
    #   - min_support       :   treshold to store a large-itemset
    # OUTPUT:
    #   - itemsets          :   dictionary with Leaf-class items that have support over min_support

    # Make dictionary where we store lengh l itemset under key l
    level = 1
    itemsets = {}
    d = len(transactions)
    
    # Start with itemsets where each item is it's own itemset
    # make_large_one_item_sets returns:
    #   - L_prev : set of length one itemsets
    #   - itemsets : class with itemset and support parameters
    L_prev, itemsets[level] = make_large_one_item_sets(transactions, d * min_support)

    # Generate itemsets of length (N+1) until no itemsets are discovered
    while len(L_prev) != 0:
        print("Solving itemsets of length {}".format(level + 1))
        # Generate candidates of length (level + 1)
        C_K = apriori_gen(L_prev, N=level)

        # A tree-kind structure that helps us checking subsets faster
        tree = SubsetTree(C_K)

        # ============= TODO: ========================
        # See chapter 9.2 for Apriori() algorithm details
        #   
        # Your implementation should:
        # 
        # 1. Go over all the transactions and for each single transaction
        # find all itemsets in C_K that are subset of the transaction. increment 
        # count for all such subsets. 
        # 
        # Hints:
        #   - You want to use: subsetTree - class to find subsets more efficient
        #       - Tree is constructed above
        #       - tree.subset(transaction) returns a iterable over all subsets that you can for loop over
        #       - Tree leafs contain support-count and itemset parameters
        #
        #   - if you are looping over the found subsets you can use 
        #       - itemset.increment_support() to raise count of a itemset
        #    
        # ============================================

        # Pass only valid item(sets)
        level += 1
        L_prev = set()
        itemsets[level] = set()
        for large_item_candidate in tree.fetch_candidate_itemsets():
            # ============= TODO: ========================
            # See chapter 9.2 for Apriori() algorithm details
            #
            # Your implementation should:
            # 
            # 1. Go over all generated subsets of C_K and pass only itemsets to next level
            # where itemset has count over (d * min_support).
            # 
            # 2. If a itemset is approved as frequent, you should
            #       - Add only the itemset tuple to L_prev as we make the new itemset based on these
            #       - Add the leaf-itemlarge_item_candidate to dictionary itemsets[level] 
            #         as we want to store the itemset and the support count
            #   
            #  Hints:
            #   - All generated itemsets are stored in tree and are iterated over with tree.fetch_candidate_itemsets
            #   - large_item_candidate is a Leaf item with attributes
            #       - itemset : itemset candidate as a tuple
            #       - support : total count of support for the candidate
            pass # Remove this line!
            # ============================================
            
    return itemsets

# Recommendation class to store association rules
class recommendation:
    def __init__(self, body, head, confidence):
        self.head = head
        self.body = body
        self.confidence = confidence


# FIND_ASSOCIATION_RULES: find head -> body rules
def find_association_rules(itemsets, support_count_dictionary, min_confidence_ratio=0.5):
    # INPUT:
    #   - itemsets                      : list containing Leaf class items with itemset - tuples
    #   - support_count_dictionary      : dictionary that maps itemset (tuple) to support-count
    #   - min_support_ratio             : Min ratio of support(l) / support(a) to accept rule a -> (l - a)
    # OUTPUT:
    #   - recommendations               :   all recommendations a -> (l - a) that have min_support

    recommendations = []
    for leafitem in itemsets:
        # Extract itemset from the Leaf item
        itemset = leafitem.itemset
        support_l = support_count_dictionary[itemset]

        for i in range(1, len(itemset)):
            # Get all subsets with length i of itemset. 
            # Remember that as the itemset is frequent, also all subsets of it are frequent
            iter_combinations = list(itertools.combinations(itemset, i))
            # ============= TODO: ========================
            # See chapter 9.3 for details on mining association rules
            # 
            # After finding all frequent itemsets, we want to find association rules for recommending individual items
            #   
            # Your implementation should:
            #   
            #  let I be the frequent itemset and S be some non-empty subset
            #
            #  1. Go over all possible subsets of frequent itemset
            #  2. If support(I) / support(S) >= min_confidence_ratio
            #       - Make new item instance of recommendation(..) class
            #           - takes inputs: body, head, confidence
            #       - Append the recommendation to recommendations list 
            #
            #  Hints:
            #       - support_count_dictionary contains mapping from frequent itemset-tuple to its support count
            #           - support_count_dictionary[itemset] : itemset should be sorted
            #
            # ============================================
    return recommendations


