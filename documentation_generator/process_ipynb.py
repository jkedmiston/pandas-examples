#!/usr/bin/env python
"""
"""
import os

def prep_line_for_jupyter(l):
    """
    """
    if len(l) > 2:
        if l[0] == "#" and l[1] == "%":
            l = l[1:]
    h = l.replace('"', r'\"').replace("\n", "\\n").replace("'", r'\"')
    out = '"%s"' % h
    out += ",\n"
    return out

def prep_lines_for_jupyter(fname):
    g = open(fname, 'r')
    lines = g.readlines()
    out = ''
    for l in lines:
        out += prep_line_for_jupyter(l)
        pass
    return out

def replace_exec_line_if_detected(l):
    """
    If find a line with exec(open, open the contents of that file and extract those lines and return them. 
    """
    if l.count("exec(open") == 0:
        retval = l
    else:
        # make sure the exec file is a python file. 
        if l.count('.py') == 1:
            idx = l.index('.py')
            suffix = l[idx:idx+3]
            i = l.index('open(') + 6
            while 1:
                test_file_to_inject = l[i:idx] + suffix
                if os.path.isfile(test_file_to_inject):
                    retval = prep_lines_for_jupyter(test_file_to_inject)
                    retval0 = '"# cell source file: %s\\n",\n' % test_file_to_inject
                    if retval[0:2] == '"%':
                        txt1 = retval[:-2].replace('\\n', 'xx').split('\n')[0]
                        txt = retval[:-2][len(txt1) + 1:]
                        retval = txt1 + retval0 + txt + "\n"
                        retval = retval.replace('xx', '\\n')
                    else:
                        retval = retval0 + retval[:-2] + "\n"
                    break
                i += 1
    return retval


def reset_execution_count_in_ipynb(fname):
    lines = open(fname, 'r').readlines()
    all_lines = []
    for kk, line in enumerate(lines):
        if line.count('"execution_count"'):
            line = '"execution_count":null,\n'
        all_lines.append(line)
    g = open(fname, 'w')
    g.write('\n'.join(all_lines))
    g.close()
    print("%s wrote: %s" % (__file__, g.name))

def replace_exec_cells_in_ipynb(fname, fnameout):
    lines = open(fname, 'r').readlines()
    all_lines = []
    for kk, line in enumerate(lines):
        new_line = replace_exec_line_if_detected(line)
        all_lines.append(new_line)
        pass

    g = open(fnameout, "w")
    g.write('\n'.join(all_lines))
    g.close()
    print("%s wrote: %s" % (__file__, g.name))

def process_ipynb(inputfile, output):
    print("processing %s -> %s" % (inputfile, output))
    replace_exec_cells_in_ipynb(inputfile, output)
    reset_execution_count_in_ipynb(output)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser('')
    parser.add_argument('input')
    parser.add_argument('--output', dest='output', required=False, default=None)
    args = parser.parse_args()
    if args.output is None:
        output = args.input.replace('.ipynb', '_out.ipynb')
    else:
        output = args.output
    if args.input.count('.ipynb') == 0:
        raise Exception("expecting ipynb input, you have %s" % args.input)
    
    process_ipynb(args.input, output)
