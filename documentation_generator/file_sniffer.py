def detect_multi_line_assignment(kk, lines):
    l = lines[kk]
    if l.count('=') == 0:
        return {'kk':kk + 1, 'continue':1, 'output':None}

    kk0 = kk
    startline = ""
    l = lines[kk0]
    while l.strip()[-1] == ',' and kk < len(lines):
        l = lines[kk]
        startline += l
        kk += 1
        pass
    if kk == kk0:
        startline = lines[kk0]
    return {'kk':kk + 1, 'continue':0, 'output':startline}
    
