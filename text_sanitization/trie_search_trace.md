# Reasoning Trace: Adversarial Prompt Sanitizer

## 1. Problem Context & Objective
In Large Language Model (LLM) infrastructure, user inputs must be sanitized in real-time to prevent prompt injection attacks or policy violations. We need a system that checks an incoming prompt against a massive database of thousands of banned terms.

**The core constraint:** The check must happen with ultra-low latency before the prompt reaches the expensive inference layer. The lookup time must not degrade as the database of banned words grows.

## 2. Approach 1: The Naive Method (Iterative Search)
The standard approach is storing banned words in a List or Set, and iterating through the prompt, checking if `word in banned_set`.
* **Time Complexity:** $O(M \times L)$ where $M$ is the number of banned words and $L$ is the length of the prompt. 
* **Why it fails at scale:** If the database contains 100,000 banned phrases, checking every word in a 1,000-token prompt against the entire database causes massive CPU spikes and unacceptable latency.

## 3. Approach 2: The Production Method (Trie / Prefix Tree)
We utilize a **Trie** (Prefix Tree) to store the banned words. A Trie restructures the data so that words sharing the same prefix share the same nodes in memory.

1. **Initialization:** Banned words are inserted character by character into the tree structure.
2. **Execution:** When validating a prompt, we traverse the Trie using the characters of the input words.

* **Time Complexity:** $O(W \times L)$ where $W$ is the number of words in the prompt and $L$ is the maximum length of a word. 
* **Space Complexity:** $O(N \times L)$ where $N$ is the number of banned words, heavily optimized by shared prefixes.
* **Why this is the right choice:** The search time is strictly bound by the length of the input prompt, **completely independent** of how massive the banned word database becomes. Searching for a 5-letter banned word takes 5 operations, whether the database has 10 words or 10 million words.

## 4. Edge Cases Handled
* **Empty Prompts:** Returns `True` (safe) instantly, saving compute.
* **Partial Matches:** The `is_end_of_word` flag ensures that a safe word like "classic" doesn't trigger a flag for a shorter banned substring unless explicitly defined.
