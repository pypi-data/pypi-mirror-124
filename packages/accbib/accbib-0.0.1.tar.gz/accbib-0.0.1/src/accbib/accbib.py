import urllib.request
from urllib.error import HTTPError
from pybtex.database import BibliographyData,Entry,Person
import json
import os
from . import ioxml
from . import iobib
from . import translator

def authors2person(authors):
    new_authors = []
    for author in authors:
        pers = Person()
        given_name = author.get('given')
        if given_name is not None:
            strs = given_name.split(' ')
            pers.first_names = [strs[0]]
            if len(strs)>1:
                pers.middle_names = strs[1:]
        last_name = author.get('family')
        if last_name is not None:
            pers.last_names = [last_name]
        new_authors.append(pers)
    return new_authors

def json2entry(jstr):
    fields = {}
    keymaps = dict(
        doi='DOI',
        journal='container-title',
        number='issue',
        pages='page',
        publisher='publisher',
        title='title',
        url='URL',
        volume='volume',
        city='city',
        edition='edition-number'  
        )
    for key,value in keymaps.items():
        data = jstr.get(value)
        if data is not None:
            data = str(data)
            data = data.strip().strip(r'{}[]')
            if data!='':
                fields[key] = data
    
    if fields.get('pages') is None:
        pages = jstr.get('article-number')
        if pages is not None:
            fields['pages'] = pages

    try:
        fields['year'] = str(jstr['created']['date-parts'][0][0])
    except:
        pass
    
    type_ = jstr.get('type','journal-article')
    type_ = translator.jtypeTranslator(type_,itype='json',otype='bib')

    ety = Entry(type_,fields=fields)
    authors = jstr.get('author')
    if authors is not None:
        pers = authors2person(authors)
        ety.persons['author'] = pers
    editors = jstr.get('editor')
    if editors is not None:
        pers = authors2person(editors)
        ety.persons['editor'] = pers
    
    return ety

def entries2bib(entries,tags=[]):
    etyDict = {}
    N1 = len(entries) - len(tags)
    tags = tags+ [None]*N1
    for ii, ety in enumerate(entries):
        if tags[ii] is None:
            try:
                tag = ety.persons['author'][0].last_names[0]+ety.fields['year']
            except:
                tag = 'reftag'
        else:
            tag = tags[ii]
        # check if tag already exists in previous tags
        if tag in tags[0:ii]:
            ii=1
            while (tag+f'_{ii:d}') in tags[0:ii]:
                ii += 1
            tag = tag+f'_{ii:d}'
        # add ety to dict
        tags[ii] = tag
        etyDict[tag] = ety
    return BibliographyData(entries=etyDict)

def fetchadoi(doi,default='default',userlib=None):
    # look up doi on website
    BASE_URL = 'http://dx.doi.org/'
    url = BASE_URL + doi
    req = urllib.request.Request(url)
    req.add_header('Accept', 'application/vnd.citationstyles.csl+json')
    try:
        with urllib.request.urlopen(req) as f:
            jstr = f.read().decode()
            jobj = json.loads(jstr)
            print(f'{doi} was successfully looked up!')
    except HTTPError as e:
        # look up doi in user lib
        if userlib is not None:
            try:
                for entag in userlib.entries:
                    ety = userlib.entries[entag]
                    if ety.fields['doi'] == doi:
                        print(f'{doi} was found in userlib!')
                        return ety
            except:
                pass
        # use default value if provided
        if default == 'default':
            if e.code == 404:
                mesg = 'DOI not found.'
            else:
                mesg = 'Service unavailable.'
            jdict = dict(title=mesg,DOI=doi,author=[{'family':'Anom','given':'Anom'}])
            jstr = json.dumps(jdict)
            jobj = json.loads(jstr)
            print(f'{doi} was not found, a program generated value was used.')
        else:
            print(f'{doi} was not found, used provided default value was used.')
            return default
    
    return json2entry(jobj)

def fetchdois(dois,default='default',userlib=None):
    # dois: list of doi
    if isinstance(dois,str):
        dois = [dois]

    entries = []
    for ii, doi in enumerate(dois):
        # get rid of duplicate dois
        if doi in dois[0:ii]:
            continue
        ety = fetchadoi(doi,default=default,userlib=userlib)
        entries.append(ety)
    
    # add tags for each ref
    bibdata = entries2bib(entries)
    return bibdata

def checkbib(bibdata):
    for ent in bibdata.entries:
        ety = bibdata.entries[ent]
        doi = ety.fields['doi'].strip().strip(r'{}[]')

        ety2 = fetchadoi(doi,default=None)
        if ety2 is not None:
            # type
            newtype = ety2.type
            if newtype!='':
                ety.type = newtype
            # fields
            for key, value in ety2.fields.items():
                ety.fields[key]= value
            # person
            ety.persons = ety2.persons
    return bibdata

def export(filename,bibdata,jnStyle='full'):
    exts = ['.bib','.xml']
    extension = os.path.splitext(filename)[1]
    if extension.lower() not in exts:
        extension = exts[0]
        filename = filename+extension
    
    if extension == '.bib':
        iobib.export2bib(filename,bibdata)
    
    if extension == '.xml':
        ioxml.export2xml(filename,bibdata,jnStyle=jnStyle)

def doi2db(dois,outfile):
    bibdata = fetchdois(dois)
    export(outfile,bibdata)

def loadbib(filename,checkdoi=True):
    bibdata = iobib.importbib(filename)
    if checkdoi:
        bibdata = checkbib(bibdata)
    return bibdata

def loadxml(filename,checkdoi=True):
    entries,tags = ioxml.importxml(filename)
    bibdata = entries2bib(entries,tags=tags)
    if checkdoi:
        bibdata = checkbib(bibdata)
    return bibdata

def loadois(filename,userlib=None):
    dois = []
    with open(filename, "r") as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            else:
                doi = line.strip()
                doi = line.strip(',.;"').strip()
                dois.append(doi)
    if userlib is not None:
        userlib = loaddb(userlib,checkdoi=False)
    bibdata = fetchdois(dois,userlib=userlib)
    return bibdata

def loaddb(filename,format=None,checkdoi=True):
    if format is None:
        extension = os.path.splitext(filename)[1]
        if extension=='.bib':
            return loadbib(filename,checkdoi=checkdoi)
        elif extension=='.xml':
            return loadxml(filename,checkdoi=checkdoi)
        else:
            return None
    elif format == 'bib':
         return loadbib(filename,checkdoi=checkdoi)
    elif format == 'xml':
         return loadbib(filename,checkdoi=checkdoi)
    else:
        return None

def bib2db(infile,outfile,checkdoi=True):
    bibdata = iobib.importbib(infile)
    if checkdoi:
        bibdata = checkbib(bibdata)
    export(outfile,bibdata)

def xml2db(infile,outfile,checkdoi=True):
    bibdata = ioxml.importxml(infile)
    if checkdoi:
        bibdata = checkbib(bibdata)
    export(outfile,bibdata)