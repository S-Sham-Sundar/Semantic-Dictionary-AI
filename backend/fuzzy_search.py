def levenshtein_distance(word1, word2):
    n = len(word1)
    m = len(word2)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        curr = [0] * (m + 1)
        curr[0] = i
        for j in range(1, m + 1):
            # Characters match
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    prev[j],       # Delete
                    curr[j - 1],   # Insert
                    prev[j - 1]    # Replace
                )
        prev = curr
    return prev[m]

def find_closest_words(query, vocabulary):
    results = []
    for word in vocabulary:
        distance = levenshtein_distance(query, word)
        results.append((word, distance))
    results.sort(key=lambda x: x[1])
    return results[:5]


def load_vocabulary(filename):
    with open(filename, 'r') as f:
        words = [line.strip() for line in f]
    return words
vocabulary = load_vocabulary("datasets/words.txt")

# print(find_closest_words("aplpe", vocabulary))
# print(find_closest_words("banan", vocabulary))
# print(find_closest_words("dor", vocabulary))
# print(find_closest_words("catt", vocabulary))