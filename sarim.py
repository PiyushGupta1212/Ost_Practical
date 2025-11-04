from itertools import combinations

# Transactions (from your image)
transactions = [
    ['I1', 'I2', 'I3', 'I4'],
    ['I2', 'I3', 'I5'],
    ['I1', 'I2', 'I3', 'I5'],
    ['I2', 'I5']
]

# Minimum support count
min_support = 2

def get_support(itemset, transactions):
    """Count support of itemset in transactions"""
    return sum(1 for t in transactions if set(itemset).issubset(set(t)))

def apriori(transactions, min_support):
    # Step 1: Generate candidate 1-itemsets
    items = sorted(set(i for t in transactions for i in t))
    c1 = [[i] for i in items]

    # Frequent itemsets dictionary
    freq_itemsets = {}
    k = 1
    current_l = []

    # Step 2: Loop until no more frequent itemsets
    while True:
        # Calculate support for candidates
        candidates = []
        for itemset in c1:
            support = get_support(itemset, transactions)
            if support >= min_support:
                candidates.append(itemset)
                freq_itemsets[tuple(itemset)] = support

        if not candidates:
            break

        current_l = candidates

        # Generate new candidates (join step)
        next_c = []
        for i in range(len(current_l)):
            for j in range(i+1, len(current_l)):
                union = sorted(set(current_l[i]) | set(current_l[j]))
                if len(union) == k+1 and union not in next_c:
                    next_c.append(union)
        c1 = next_c
        k += 1

    return freq_itemsets

# Run Apriori
frequent_itemsets = apriori(transactions, min_support)

print("Frequent Itemsets (with support counts):")
for itemset, support in frequent_itemsets.items():
    print(itemset, "=>", support)

# Generate association rules
def generate_rules(freq_itemsets, min_conf=0.5):
    rules = []
    for itemset in freq_itemsets:
        if len(itemset) > 1:
            support_itemset = freq_itemsets[itemset]
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    consequent = tuple(set(itemset) - set(antecedent))
                    if consequent:
                        conf = support_itemset / freq_itemsets[tuple(sorted(antecedent))]
                        if conf >= min_conf:
                            rules.append((antecedent, consequent, conf))
    return rules

rules = generate_rules(frequent_itemsets)

print("\nAssociation Rules:")
for antecedent, consequent, conf in rules:
    print(antecedent, "=>", consequent, f"(conf: {conf:.2f})")
