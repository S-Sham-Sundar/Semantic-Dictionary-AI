class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True

    def search(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_end_of_word

    def starts_with(self, prefix):
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True
    
    def delete(self, word):
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete_child = _delete(node.children[char], word, depth + 1)
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        _delete(self.root, word, 0)
    
    def autocomplete(self, prefix):
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return []
            current_node = current_node.children[char]

        results = []
        def dfs(node, current_word):
            if node.is_end_of_word:
                results.append(current_word)

            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)

        dfs(current_node, prefix)
        
        return results
    
    def load_words_from_file(self, filename):
        with open(filename, 'r') as f:
            words = [line.strip() for line in f]
        for word in words:
            self.insert(word)



trie = Trie()
# Load dataset
trie.load_words_from_file("datasets/words.txt~")


# print("----- SEARCH TESTS -----")

# print(trie.search("apple"))        
# print(trie.search("application"))  
# print(trie.search("banana"))       
# print(trie.search("door"))         
# print(trie.search("zebra"))        


# print("\n----- PREFIX TESTS -----")

# print(trie.starts_with("ap"))      
# print(trie.starts_with("bat"))     
# print(trie.starts_with("cat"))     
# print(trie.starts_with("do"))      
# print(trie.starts_with("xyz"))     


# print("\n----- AUTOCOMPLETE TESTS -----")

# print(trie.autocomplete("ap"))
# print(trie.autocomplete("ba"))
# print(trie.autocomplete("cat"))
# print(trie.autocomplete("do"))
# print(trie.autocomplete("z"))

