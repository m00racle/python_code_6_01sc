"""  
Problem Wk.1.4.9: Extract tags [Optional]
Write a procedure, called extractTags, that takes a string as input and returns a list of
strings corresponding to the names of the bracketed tags in the string. Bracketed tags
start with [ and end with ]. You can assume that the brackets are properly matched in
the input. 
"""

def extractTags(inp : str) -> list:
    """  
    given inp a string 
    returns list of strings that was extracted from inp which tagged with []
    """
    result = []
    # pick = False
    # tagged = ''
    # for s in inp:
    #     if s == '[' and not pick: 
    #         pick = True
    #         continue
    #     if s == ']' :
    #         if not pick : raise IndexError("invalid tag detected: no enclosure")
    #         pick = False
    #         result.append(tagged)
    #         tagged = ''
        
    #     if pick : tagged += s
    
    # if pick : raise IndexError("invalid tag detected: no enclosure")

    # : use alternative algoithm str[:] to pass the same tests:
    start = None
    end = None
    for i in range(len(inp)):
        if inp[i] == '[' and start == None : start = i + 1
        if inp[i] == ']' :
            if start == None : raise IndexError("invalid tag detected: no enclosure")
            end = i
            result.append(inp[start : end])
            start = None
            end = None
    
    if start != None or end != None : raise IndexError("invalid tag detected: no enclosure")

    return result

def run():
    # run the code above
    try:
        print(extractTags('test [the run [] in except] [cond]'))
    except IndexError:
        print("Index error happen")
    except :
        print("other error happen")
    else:
        print("Nothing happen")
    finally:
        print("run complete")
        

if __name__ == '__main__':
    run()