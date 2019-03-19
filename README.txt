# =============================================
Python implementation for finding frequent itemsets and making association rules from them

- Modify submission.py file according to the instructions TODO's.
- Submit the same file for tasks: Mining frequent itemsets, Finding association rules

- To test your implementation locally run: python3/python2 run.py 

# =============================================
                Basic overview

- For taks: mining frequent itemsets, you should complete test_apriori_gen(..) and large_itemsets(..)
- For task: finding association rules, you should complete find_association_rules(..)

Intuition for the algorithm is simple: in order to have frequent itemset (a, b, c),
all subsets (a, b), (a, c), (b, c) must be frequent also. Then we can start from N = 1 and 
construct always size (N + 1) subsets from previous level. This way we easily prune out most of the search space.

Hints:
    - Every itemset that we generate is a tuple, so that we can store them in sets
        - makes it faster for example to check if for example a itemset is contained in some set

    - Every itemset that we generate should be sorted
        - when itemset is sorted, we can utilize this to find the itemsets faster
    
    - You should peek at subsetTree.py that is used to find subsets of length N and store current itemsets
        - class Leaf contains always one itemset with support count
        - you can iterate over all itemsets with tree.fetch_candidate_itemsets(..)


- Data for the exercise is extracted from instacart grocery orders, available at: https://www.instacart.com/datasets/grocery-shopping-2017

# =============================================
