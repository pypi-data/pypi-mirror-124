import numpy as np
import logging

def jnameTranslator(jname,jnStyle='abbr'):
    jabbrs = np.array([ [r'Acta Physica Sinica',r'Acta Phys. Sin.'],
                        [r'Analytical Chemistry',r'Anal. Chem.'],
                        [r'Applied Optics',r'Appl. Opt.'],
                        [r'Applied Physics B',r'Appl. Phys. B'],
                        [r'Applied Physics B: Lasers and Optics',r'Appl. Phys. B Lasers Opt.'],
                        [r'Applied Physics Letters',r'Appl. Phys. Lett.'],
                        [r'Applied Sciences',r'Appl. Sci.'],
                        [r'Atomic Data',r'At. Data'],
                        [r'Chemical Physics',r'Chem. Phys.'],
                        [r'Chemical Phyics Letters',r'Chem. Phys. Lett.'],
                        [r'Chemical Reviews',r'Chem. Rev.'],
                        [r'Chinese Physics Letters',r'Chin. Phys. Lett.'],
                        [r'European Physical Journal B',r'Eur. Phys. J. B'],
                        [r'European Physical Journal D',r'Eur. Phys. J. D'],
                        [r'IEEE Journal of Quantum Electronics',r'IEEE J. Quantum Electron.'],
                        [r'IEEE Journal of Selected Topics in Quantum Electronics',r'IEEE J. Sel. Top. Quantum Electron.'],
                        [r'Journal of Applied Physics',r'J. Appl. Phys.'],
                        [r'Journal of Modern Optics',r'J. Mod. Phys.'],
                        [r'Journal of National University of Defense Technology',r'J. Natl. Univ. Def. Technol.'],
                        [r'Journal of Optics',r'J. Opt.'],
                        [r'Journal of Physics B: Atomic, Molecular and Optical Physics',r'J. Phys. B At Mol. Opt. Phys.'],
                        [r'Journal of Physics B','J. Phys. B'],
                        [r'Journal of the Optical Society of America A',r'J. Opt. Soc. Am. A'],
                        [r'Journal of the Optical Society of America B',r'J. Opt. Soc. Am. B'],
                        [r'Laser Physics',r'Laser Phys.'],
                        [r'Light: Science & Applications',r'Light Sci. Appl.'],
                        [r'Nature Communications',r'Nat. Commun.'],
                        [r'Nature Photonics',r'Nat. Photonics'],
                        [r'Nature Physics',r'Nat. Physics'],
                        [r'New Journal of Physics',r'New J. Phys.'],
                        [r'Optics & Laser Technology',r'Opt. Laser Technol.'],
                        [r'Optics Communications',r'Opt. Commun.'],
                        [r'Optics Express',r'Opt. Express'],
                        [r'Optics Letters',r'Opt. Lett.'],
                        [r'Physical Review',r'Phys. Rev.'],
                        [r'Physical Review A',r'Phys. Rev. A'],
                        [r'Physical Review B',r'Phys. Rev. B'],
                        [r'Physical Review C',r'Phys. Rev. C'],
                        [r'Physical Review D',r'Phys. Rev. D'],
                        [r'Physical Review E',r'Phys. Rev. E'],
                        [r'Physical Review Letters',r'Phys. Rev. Lett.'],
                        [r'Physical Review Research',r'Phys. Rev. Res.'],
                        [r'Physical Review X',r'Phys. Rev. X'],
                        [r'Physics of Plasmas',r'Phys. Plasmas'],
                        [r'Physics Today',r'Phys. Today'],
                        [r'Reports on Progress in Physics',r'Reports Prog. Phys.'],
                        [r'Review of Scientific Instruments',r'Rev. Sci. Instrum.'],
                        [r'Reviews of Modern Physics',r'Rev. Mod. Phys.'],
                        [r'Science Advances',r'Sci. Adv.'],
                        [r'Scientific Reports',r'Sci. Rep.'],
                        [r'Soviet Journal of Experimental and Theoretical Physics',r'Sov. J. Exp. Theor. Phys.'] ])

    if jnStyle=='abbr':
        ind0 = 0
        ind1 = 1
    else:
        # if not 'abbr', 'full' will be assumed
        ind0 = 1
        ind1 = 0
    
    res = jname
    ind = np.where(np.char.lower(jabbrs[:,ind0])==jname.lower())
    try:
        ind = ind[0][0]
        res = jabbrs[ind][ind1]
        return res
    except:
        return res

def jtypeTranslator(jtype, itype='bib',otype='xml'):
    typetbl = np.array([['article','JournalArticle','journal-article'],
                        ['book','Book','book'],
                        ['inproceedings','ConferenceProceedings','proceedings-article']
                      ])

    if itype == 'xml':
        indi = 1
    elif itype == 'json':
        indi = 2
    else:
    # take as 'bib'
        indi = 0

    if otype == 'xml':
        indo = 1
    elif otype == 'json':
        indo = 2
    else:
    # take as 'bib'
        indo = 0
    # if input type equals to output type
    if itype == otype:
        return jtype
    
    ind = np.where(np.char.lower(typetbl[:,indi])==jtype.lower())
    try:
        ind = ind[0][0]
        res = typetbl[ind][indo]
        return res
    except:
        return jtype
    
def fieldsTranslator(fields,dst='bib'):
    xmlfields = ['URL','Issue', 'JournalName','City',   'DOI']
    bibfields = ['url','number','journal',    'address','doi']
    if dst.lower()=='bib':
        lut = xmlfields
        out = bibfields
        convertor = str.lower
    elif dst.lower()=='xml':
        lut = bibfields
        out=xmlfields
        convertor = str.capitalize
    else:
        logging.warn(f'undefined dst paramters: {dst}')
        return fields
    
    outfields = {}
    for key,value in fields.items():
        try:
            ind = lut.index(key)
            key2 = out[ind]
        except:
            key2 = convertor(key)
        outfields[key2] = value
    
    return outfields