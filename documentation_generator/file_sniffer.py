"""
Fairly random functions for manipulating python files as ascii text collections. 
"""
from documentation_generator.process_ipynb import prep_line_for_jupyter

def detect_multi_line_assignment(index, lines):
    """
    detects if a line is carriage returned across multiple lines and if so
    extracts the entire multiline string and how 

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


def detect_multi_line_function(index, lines):
    """
    detects if a function is carriage returned across multiple lines and if so
    extracts the entire multiline string and how 
    @index: integer index of a list (line number)
    @lines: list of strings (lines from a file)
    """
    l = lines[index]
    if l.count('def ') == 0:
        return {'index':index + 1, 'continue':1, 'output':None}
    elif len(l) < len("def ()"):
        return {'index':index + 1, 'continue':1, 'output':None}
    else:
        if l[0:4] != "def ":
            return {'index':index + 1, 'continue':1, 'output':None}
        else:
            pass
    initial_index = index
    startline = ""
    l = lines[initial_index]
    # lines ending in comma are continuations
    # pd.DataFrame.from_dict({'x':[1, 2],
    #                         'y':[2, 3]})
    while index < len(lines):
        l = lines[index]
        if len(l) > 7:
            if l.count('return'):
    # lines ending in comma are continuations
    # pd.DataFrame.from_dict({'x':[1, 2],
    #                         'y':[2, 3]})
                if l.strip()[-1] == ",":
                    while l.strip()[-1] == "," and index < len(lines):
                        l = lines[index]
                        startline += l
                        index += 1
                        pass
                else:
                    startline += l
                    index += 1
                    pass
                break
        if len(l) > 10:
            if l[0:10] == "    return":
                startline += l
                index += 1
                break
            
        startline += l
        index += 1
        pass
    
    if index == initial_index:
        startline = lines[initial_index]
        index = index + 1
        
    return {'index':index, 'continue':0, 'output':startline}

def detect_multi_line_markdown_block(index, lines):
    """
    """
    l = lines[index]
    if l.count('#markdown') == 0:
        return {'index':index + 1, 'continue':1, 'output':None}
    else:
        pass
    initial_index = index
    startline = ""
    l = lines[initial_index]
    while index < len(lines) and l.count("#endmarkdown") == 0:
        l = lines[index]
        startline += l
        index += 1

    if index == initial_index:
        startline = lines[initial_index]
        index = index + 1
        
    return {'index':index, 'continue':0, 'output':startline}

def get_text_from_file(filename, remove_blocks=[]):
    f = open(filename, "r")
    text = ''.join(f.readlines())
    for start, stop in remove_blocks:
        if text.count(start):
            idx1 = text.index(start)
            try:
                idx2 = text.index(stop)
            except:
                import pdb
                pdb.set_trace()

            remove_text = text[idx1:idx2 + len(stop)]
            text = text.replace(remove_text, '')
        
    return text

def write_text_to_file(text, filename):
    f = open(filename, "w")
    f.write(text)
    f.close()
