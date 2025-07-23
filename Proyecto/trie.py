class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.definition = None  # Se guarda si es palabra final

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, definition):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.definition = definition

    def search(self, word):
        node = self._traverse(word)
        if node and node.is_end:
            return node.definition
        return None

    def starts_with(self, prefix):
        node = self._traverse(prefix)
        if not node:
            return []
        results = []
        self._collect_words(node, prefix, results)
        return results

    def _traverse(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _collect_words(self, node, prefix, results):
        if node.is_end:
            results.append((prefix, node.definition))
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, results)
