
def table(headers, data, footer, count):
    out = "\\begin{{longtable}}{{{:s}}}\\toprule \n".format('l'*count)
    for row in headers:
        out += ' & '.join(row) + '\\\\ \n'

    out += '\\midrule \\endhead \n \\bottomrule \\endfoot \n'

    for row in data:
        out += ' & '.join(row) + ' \\\\ \n'

    if (footer is not None):
        out += '\\midrule '
        for row in footer:
            out += ' & '.join(row) + ' \\\\ \n'


    out += '\n\\end{longtable}'

    return out
