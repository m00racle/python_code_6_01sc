"""  
Problem Wk.1.4.8: Substring
Write a procedure, called isSubstring, that takes two strings as inputs and returns True
when the first string is a substring of the second one, that is, when all of the characters
in the first string occur contiguously in the second string. 
"""

def isSubstring(word: str, subs: str)-> bool:
    """  
    Given word and subs
    Returns True if subs is substring of word and return false otherwise
    """
    if len(subs) > len(word) : return False
    for i in range(len(word)-len(subs) + 1):
        test = ''
        for k in range(len(subs)):
            test += word[i + k]
        if test == subs : return True
    return False