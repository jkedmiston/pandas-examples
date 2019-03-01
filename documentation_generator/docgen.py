"""
generate text based documentation from a working standalone script
useful for generating doc strings which update from a working python script. 
"""
import argparse
import pandas as pd
from documentation_generator.file_sniffer import detect_multi_line_assignment
from documentation_generator.file_sniffer import detect_multi_line_function, detect_multi_line_markdown_block
from documentation_generator.generate_ipynb import generate_ipynb
from documentation_generator.file_sniffer import get_text_from_file, write_text_to_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser('')
    parser.add_argument('source', default="pandas_examples/flattening.py")
    parser.add_argument('--output_file', default='stdout', dest='output_file')
    parser.add_argument('--no_jupyter', default=False, action='store_true')
    args = parser.parse_args()

    source = args.source
    output_file = args.output_file
    execution_text = ""
    if args.output_file != 'stdout':
        output_file_obj = open(output_file, 'w')
        printfunc = output_file_obj.write
    else:
        printfunc = print

    source_text = get_text_from_file(source, remove_blocks=[['"""#docgenstart', '#docgenend\n"""']])
    lines = source_text.split("\n")
    lines = list(map(lambda x: x + "\n", lines))
    
    # execute underlying source to bring in any packages, etc. 
    exec(open(source).read())

    file_line_index = 0
    sequence = []
    jupyters = ""
    while file_line_index < len(lines):
        l = lines[file_line_index]
        file_line_index0 = file_line_index
        sequence.append(file_line_index)

        outval = detect_multi_line_assignment(file_line_index, lines)
        outval2 = detect_multi_line_function(file_line_index, lines)
        outval3 = detect_multi_line_markdown_block(file_line_index, lines)
        
        # TODO: wrap this in function
        # a function was detected
        if outval2["continue"] == 0:
            output = outval2["output"]
            file_line_index = outval2["index"]
            printfunc(output)
            jupyters += "#code\n%s\n#endcode\n" % (output)
            continue

        if outval3["continue"] == 0:
            output = outval3["output"]
            file_line_index = outval3["index"]
            printfunc(output)
            jupyters += "%s\n" % output
            continue
        
        file_line_index = outval["index"] # increment forward
        if outval['continue']:
            if len(l.strip()) > 1:
                jupyters += "#code\n%s\n#endcode\n" % l
                pass
            pass
        else:
            output = outval["output"].strip()
            start, end = output.split("=", 1)
            varname = start.strip()
            end = end.strip()
            if varname.count('.') == 0:
                locals()[varname] = eval(end)
            else:
                # execute the member function e.g. df.apply(), then print out
                exec(output)
                varname = varname.split('.')[0]

            outstr = ">>> %s\n>>> %s\n%s\n" % (output, varname, locals()[varname])
            printfunc(outstr)
            execution_text += outstr + "\n"
            jupyters += "#code\n%s\n%s\n#endcode\n" % (output, varname)
            continue

    # write output at the top of the input file
    source_text = get_text_from_file(source, remove_blocks=[['"""#docgenstart', '#docgenend\n"""']])
    
    source_text = '"""#docgenstart\nFile output (%s): \n%s\n#docgenend\n"""%s' % (source, execution_text, source_text)
    write_text_to_file(source_text, source)
    if args.no_jupyter:
        pass
    else:
        # set up a pre-jupyter document by encolsing blocks in #code/#endcode blocks
        source_jupyter_file = args.source.replace('.py', '_tmp.py')
        tmp = open(source_jupyter_file, 'w')


        tmp.write(jupyters.replace('\n\n','\n'))
        # code needs to end in # (TODO)
        tmp.write("\n#\n")
        tmp.close()
        #
        generate_ipynb(source=source_jupyter_file, final_output=args.source.replace('.py', '.ipynb'))
