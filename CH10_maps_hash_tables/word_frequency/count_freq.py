

def max_word(filename):
    """Return the most frequent word in the file filename."""
    freq = {}
    for piece in open(filename, encoding = 'UTF-8').read().lower().split(): # is "piece" a line?
        # only consider alphabetic characters within this piece
        word = ''.join(c for c in piece if c.isalpha())
        if word:
            freq[word] = 1 + freq.get(word, 0) # word goes in as the key,
                                                # value is freq which is incremented
                                                # if word was already in dict.
                                                # Else 0 is the default freq
    max_word = ''
    max_count = 0
    for (w, c) in freq.items(): # (key, value) tuples represent (word, count)
         if c > max_count:
             max_word = w
             max_count = c
    print(f"The most frequent word is '{max_word}'")
    print(f"{max_word} occurs '{max_count}' times")
    return (max_word, max_count)

filename = 'sherlock_holmes.txt'
max_word(filename)
