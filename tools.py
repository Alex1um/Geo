from collections import Counter

def make_columns_unique(columns: list):
    from collections import Counter
    counter = Counter(columns)
    for i in range(len(columns) - 1, -1, -1):
        count = counter[columns[i]]
        if count > 1:
            counter[columns[i]] -= 1
            columns[i] = f"{columns[i]}_{count - 1}"
    return columns