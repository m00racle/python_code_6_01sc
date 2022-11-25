"""  
Problem Wk.1.4.7: Palindrome [Optional]
Write a procedure, called isPalindrome, that takes a string as an argument and returns
True if the string is a palindrome, that is, if the string is identical to the reversed string.
It should return False otherwise.
"""

def isPalindrome(s : str) -> bool:
    """  
    given s a string
    returns true if s is palindrome and false otherwise
    """
    i = 0
    k = -1

    while (i - k) <= len(s):
        if s[i] != s[k]: return False
        i += 1
        k -= 1
    
    return True