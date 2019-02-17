from pandas_examples.file_sniffer import detect_multi_line_assignment

def test_multi_line_assignment():
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

if __name__ == "__main__":
    test_multi_line_assignment()
