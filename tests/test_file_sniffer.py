from documentation_generator.file_sniffer import detect_multi_line_assignment
from documentation_generator.file_sniffer import detect_multi_line_function
from documentation_generator.process_ipynb import replace_exec_line_if_detected

def test_replace_exec_line_if_detected():
    """
    Tests the execfile replacement capability in creating jupyter notebook
    from primitives. 
    """
    test_line = "exec(open('tests/test_file_sniffer.py').read())"
    l = replace_exec_line_if_detected(test_line)

    # someone cannabilistic to self test this file. 
    test_lines = open("tests/test_file_sniffer.py").readlines()
    exec_lines = l.split("\n")
    for kk, line in enumerate(test_lines):
        if kk == 0:
            continue
        exec_line = exec_lines[kk + 1]
        # excludes \\n", from the end of lines. 
        # the replacement puts in commas at the end of new lines, and
        # newlines are replaced with \\n. If
        # there isn't a comma then just do the \\n exclusion.
        # the selection starts at 1 to avoid the " at the start of the line. 
        if exec_line[-1] == ",":
            exec_line = exec_line[1:-4]
        else:
            exec_line = exec_line[1:-3]
            
        test_line = test_lines[kk][:-1]
        if test_line.count('"') or test_line.count("\\") or test_line.count("'"):
            # TODO... these cases currently too complicated to test
            continue
        assert exec_line == test_line
    
def test_detect_multi_line_assignment():
    text = """
%(core)s
%(nextline)s
lines5
    """
    core = """a = testfunc([43,
                  44,
                  45, 46, 47, 48,
                  50, 51])"""
    nextline = "nextl"
    text = text % dict(core=core, nextline=nextline)
    lines = text.split('\n')
    lines = list(map(lambda x: x+"\n", lines))
    out = detect_multi_line_assignment(0, lines)
    assert out['index'] == 1
    assert out['continue'] == 1

    out = detect_multi_line_assignment(1, lines)
    assert out["output"] == core + "\n"
    assert out["index"] == 1 + 4
    assert lines[out["index"]] == nextline + "\n"

def test_detect_multi_line_function():
    text = """
%(core)s
%(nextline)s
lines5
    """
    core = """def a1(x):
    print(x)
    return"""
    nextline = "nextl"
    text = text % dict(core=core, nextline=nextline)
    lines = text.split('\n')
    lines = list(map(lambda x: x+"\n", lines))
    out = detect_multi_line_function(0, lines)
    assert out['index'] == 1
    assert out['continue'] == 1

    out = detect_multi_line_function(1, lines)
    assert out["output"] == core + "\n"
    assert out["index"] == 1 + 3
    assert lines[out["index"]] == nextline + "\n"

if __name__ == "__main__":
    test_detect_multi_line_assignment()
    test_detect_multi_line_function()
    test_replace_exec_line_if_detected()
    
