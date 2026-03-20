from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class PromptSanitizer:
    """
    Uses a Trie (Prefix Tree) to efficiently store and search for 
    banned adversarial substrings in O(L) time.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert_banned_word(self, word: str) -> None:
        """Inserts a banned word into the Trie. Time: O(L)"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def is_prompt_safe(self, prompt: str) -> bool:
        """
        Checks if any word in the prompt is in the banned list.
        Complexity: O(W * L) where W is words, L is max word length.
        Independent of the size of the banned word database.
        """
        if not prompt:
            return True

        words = prompt.split()
        for word in words:
            node = self.root
            found = True
            for char in word:
                if char not in node.children:
                    found = False
                    break
                node = node.children[char]
            
            # If we successfully traversed the word and it's marked as a banned ending
            if found and node.is_end_of_word:
                return False 
                
        return True
