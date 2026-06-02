import json

class DictionaryEngine:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.words = {}
        for entry in data:
            self.words[entry["word"]] = entry

    def get_word_data(self, word):
        return self.words.get(word)
    
dictionary = DictionaryEngine("datasets/dictionary.json")

print(dictionary.get_word_data("apple"))

print(dictionary.get_word_data("dog"))

print(dictionary.get_word_data("banana"))
