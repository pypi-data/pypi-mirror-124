from pybtex.database.input import bibtex

def export2bib(filename,bibdata):
    bibdata.to_file(filename,bib_format='bibtex')
    print(f'saved as {filename}')

def importbib(filename):
    parser = bibtex.Parser()
    bibdata = parser.parse_file(filename)
    return bibdata