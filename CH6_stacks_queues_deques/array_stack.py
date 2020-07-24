"""Stack implementation using a Python list object as unserlying storage."""

class ArrayStack:

    def __init__(self):
        """Create an empty stack."""
        self._data = [] # The list instance is non-public--so there will be no
                        #   way to externally use it as if it were a list.
                        #   We don't want to just inheirit list class's attributes
                        #   and methods wholesale.

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self._data)

    def is_empty(self):
        """Return True if the stack is empty."""
        return len(self._data) == 0

    def push(self, e):
        """Add element e to the top of the stack."""
        self._data.append(e) # External caller can't directly call append, they
                                #  they must use push.

    def top(self):
        """Return (but don't remove) the element at the top of the stack."""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        """Remove and return the element from the top of the stack (last in
        first out). Raise Empty exception if stack is empty."""
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop() # list class's pop method handles it from here

def reverse_file(filename):
    """Overwrite the given file with its contents reversed linewise."""
    S = ArrayStack()
    original = open(filename)
    for line in original:
        S.push(line.rstrip('\n')) # The function will reinsert newlines in the
                                    # write operation phase.
    original.close()

    # Now overwrite the contents in LIFO order
    output = open(filename, 'w') # reopening in write mode will immediately overwrite the original to blank.
    while not S.is_empty():
        output.write(S.pop() + '\n') # reinsert newline characters
    output.close

def is_matched(expr):
    """Check whether delimiter characters in an expression match. Return True
    if matched else False.

    Args:
        expr (str): String with an expression that uses delimters like {[()]}
    """
    # running time O(n) for input sequence of length n.
    #   At most n calls to push and pop, all other helper calls are O(1).
    lefty = '({['
    righty = ')}]'
    S = ArrayStack()
    for c in expr: # iterate over the characters in the expression
        if c in lefty:
            S.push(c)
        elif c in righty:
            if S.is_empty():
                return False # if there was nothing to pop then delimters unmatched
            if righty.index(c) != lefty.index(S.pop()):
                return False
    return S.is_empty() # if all symbols matched, it's empty

def is_matched_html(raw):
    """Return True if all HTML tags properly match openers to closers; else
    False.

    Args:
        raw (str): String of raw html"""
    # can raw have newlines?
    S = ArrayStack()
    j = raw.find('<') # All html tags start with a <
    while j != -1: # string.find() returns -1 for not found
        k = raw.find('>', j+1) # j+1 is optional arg start index
        if k == -1:
            return False # invalid tag
        tag = raw[j+1:k]
        if not tag.startswith('/'): # if it starts with '/' it's a closer tag
            S.push(tag)
        else:
            if S.is_empty(): # nothing to match with
                return False
            if tag[1:] != S.pop():
                return False # delimiter doesn't match
        j = raw.find('<', k+1) # find start of next tag if any
    return S.is_empty()
        

def main():
    reverse_file('reverse_me.txt')
    assert is_matched("((())") == False
    assert is_matched("([{quux([{grault}])}])") == True
    print("is_matched() simple asserts ok")

    html_good = "<body>text outside a tag</body>"
    html_bad1 = "<body an incomplete tag"
    html_bad2 = "<h1>opening tag with no closing tag<h1>"

    assert is_matched_html(html_good) == True
    assert is_matched_html(html_bad1) == False
    assert is_matched_html(html_bad2) == False
    print("is_matched_html() simple asserts ok")

if __name__ == '__main__':
    main()
    
    
