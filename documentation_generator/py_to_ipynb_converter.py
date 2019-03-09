#!/usr/bin/env python
from documentation_generator.process_ipynb import prep_line_for_jupyter

def get_file_as_text(template):
    g = open(template, "r")
    lines = g.readlines()
    g.close()
    return ''.join(lines)

def write_text_as_file(txt, fname):
    g = open(fname, "w")
    g.write(txt)
    g.close()
    return g.name

fmt = """ {
   "cell_type": "code",
   "execution_count": %(execution_count)d,
   "metadata": {},
   "outputs": [],
   "source": [
    "%(cell_text)s"
    ]
   }
"""

code_fmt=""" {
   "cell_type": "code",
   "execution_count": %(execution_count)d,
   "metadata": {},
   "outputs": [],
   "source": [
    %(code_text)s
    ]
   }
"""

markdown_fmt=""" {
   "cell_type":"markdown",
   "metadata":{},
   "source":[
%(markdown_text)s
    ]
   }
"""

def add_markdown_block(full_text, kk, lines):
    markdown_text = ""
    markdown_active = 1
    kk += 1
    l = lines[kk].strip().replace("\n", "")
    while kk < len(lines):
        l = lines[kk]
        if l.strip() == "#endmarkdown":
            kk += 1
            break
        if l == "":
            kk += 1
            continue
        if l[0] != "#":
            kk += 1
            continue

        l1 = l[1:]
        markdown_text += prep_line_for_jupyter(l1)
        kk += 1

    contrib = markdown_fmt % dict(markdown_text = markdown_text.strip()[:-1])
    full_text += contrib + ",\n"
    return full_text, kk


def add_code_block(full_text, kk, lines):
    markdown_text = ""
    markdown_active = 1
    kk += 1
    l = lines[kk].strip().replace("\n", "")
    while kk < len(lines):
        l = lines[kk]
        if l.strip() == "#endcode":
            kk += 1
            break
        if l == "":
            kk += 1
            continue
        l1 = l 
        markdown_text += prep_line_for_jupyter(l1)
        kk += 1

    contrib = code_fmt % dict(execution_count=kk + 1,
                              code_text = markdown_text.strip()[:-1])
    full_text += contrib + ",\n"
    return full_text, kk

def py_to_ipynb_converter(source, template, output):
    assert template != output, "template must be different than output"
    g = open(source, "r")
    lines = g.readlines()
    full_text = ""
    max_index = len(lines) - 1
    kk = 0
    markdown_active = 0
    while kk < len(lines):
        l = lines[kk]
        line_text = l.strip().replace("\n","")

        # read for keywords 
        if line_text == "#markdown":
            full_text, kk = add_markdown_block(full_text, kk, lines)
            continue
        
        if line_text == "#code":
            full_text, kk = add_code_block(full_text, kk, lines)
            continue

        contrib = fmt % dict(execution_count=kk + 1,
                             cell_text=line_text)
        
        if l.strip().replace("\n","") == "":
            kk += 1
            continue
        
        full_text += contrib
        if kk != max_index:
            full_text += ",\n"

        if kk == max_index:
            break
        kk += 1

    template_text = get_file_as_text(template)
    write_text_as_file(template_text % dict(cells=full_text), output)
    print("%s wrote:%s" % (__file__, output))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('Convert custom language files to jupyter notebooks')
    parser.add_argument('source')
    parser.add_argument('--template',
                        dest='template',
                        default='documentation_generator/templates/template.ipynb')
    parser.add_argument('--output',
                        dest='output',
                        default=None,
                        required=False)
    
    args = parser.parse_args()
    template = args.template
    if args.output is None:
        output = "%s_ipynb_compiler.ipynb" % template[:-6]
    else:
        output = args.output
        
    py_to_ipynb_converter(source=args.source, template=template, output=output)

