import sys
import os
from pathlib import Path
import logging

from proai.cmdline import run
import xmltodict

log = logging.getLogger(__name__)


def adoc2xml(manuscript_dir='/home/hobs/code/tangibleai/nlpia-manuscript/manuscript'):
    cmd = f'asciidoctor -d book -b docbook5 -D {manuscript_dir}/xml {manuscript_dir}/adoc/*.adoc'
    results = run(cmd.split(' '))
    return results


def parse_xml_files(xmlpath, ext='.xml'):
    """ Read an xml file or directory of files (non-recursively) and return a nested dict

    >>> parse_xml_files(Path(DATA_DIR) / 'xml').keys()
    """
    bookdict = {}
    xmlpath = Path(xmlpath)
    if dirpath.is_dir():
        filepaths = sorted(xmlpath.listdir())
    else:
        filepaths = [dirpath]
    for f in filepaths:
        filepath = Path(dirpath) / f
        if not str(filepath).endswith(ext):
            continue
        # print(filepath)
        xmlstring = open(filepath).read()
        xmldict = {}
        try:
            xmldict = xmltodict.parse(xmlstring)
        except Exception as e:
            log.warning(f'**ParseError** -- Unable to parse "{f}":')
            log.warning(f'    {e}')
        bookdict[f] = xmldict
    return bookdict


if __name__ == "__main__":
    xmlpath = os.path.curdir
    if len(sys.argv) > 1:
        xmlpath = sys.argv[1]
    bookdict = parse_xml_files(xmlpath)
    print(bookdict.keys())
    # print(json.dumps(bookdict, indent=2))
