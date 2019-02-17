"""

"""

def detect_multi_line_assignment(index, lines):
    """
    get multi line assignment e.g. if this string is 
    split on multiple lines
    xs = np.array([[1, 2, 3],
                   [5, 6, 8]])
    becomes in the line listing
    ["xs = np.array([[1, 2, 3],\n",[5, 6, 8]])]
    this function will return the entire continuous output e.g. 
    "xs = np.array([[1, 2, 3],
                   [5, 6, 8]])"

    @index: integer index of a list (line number)
    @lines: list of strings (lines from a file)
    """
    l = lines[index]
    if l.count('=') == 0:
        return {'index':index + 1, 'continue':1, 'output':None}

    initial_index = index
    startline = ""
    l = lines[initial_index]
    # lines ending in comma are continuations
    # pd.DataFrame.from_dict({'x':[1, 2],
    #                         'y':[2, 3]})
    while l.strip()[-1] == ',' and index < len(lines):
        l = lines[index]
        startline += l
        index += 1
        pass
    
    if index == initial_index:
        startline = lines[initial_index]
        index = index + 1
        
    return {'index':index, 'continue':0, 'output':startline}
    
