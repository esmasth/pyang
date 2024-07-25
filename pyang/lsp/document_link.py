"""LSP Document Link Provider

* `textDocument/documentLink`
  https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_documentLink
"""

from datetime import datetime
import re
from typing import List, Tuple, Union

from lsprotocol import types as lsp
from pygls.server import LanguageServer


def linechar(source: str, offset: int) -> Tuple[int, int]:
    sliced = source[:offset]
    line = sliced.count('\n')
    char = offset - sliced.rfind('\n') - 1
    return (line, char)

_ietf_draft_re = r'I-D: ([a-z-0-9]+)'
_ietf_draft_uri_format = 'https://datatracker.ietf.org/doc/%s/00/'
_ietf_rfc_re = r'[rR][fF][cC][ ]*([0-9]+)(?:[:]?[ ]*Section ([0-9]+(?:\.[0-9]+(?:\.[0-9]+(?:\.[0-9]+)?)?)?))?' #pylint: disable=line-too-long
_ietf_rfc_uri_format = 'https://datatracker.ietf.org/doc/html/rfc%s%s'
def _ietf_links(source: str):
    links = []
    matches = re.finditer(_ietf_rfc_re, source, re.A)
    for match in matches:
        sline, schar = linechar(source, match.start())
        eline, echar = linechar(source, match.end())
        link_range = lsp.Range(
            lsp.Position(sline, schar),
            lsp.Position(eline, echar),
        )
        rfc_num = match.group(1)
        if match.group(2):
            rfc_sec = f'#section-{match.group(2)}'
        else:
            rfc_sec = ''
        target = _ietf_rfc_uri_format % (rfc_num, rfc_sec)
        links.append(
            lsp.DocumentLink(
                range=link_range,
                target=target,
                tooltip=target,
            )
        )
    matches = re.finditer(_ietf_draft_re, source, re.A)
    for match in matches:
        sline, schar = linechar(source, match.start())
        eline, echar = linechar(source, match.end())
        link_range = lsp.Range(
            lsp.Position(sline, schar),
            lsp.Position(eline, echar),
        )
        draft_name = match.group(1)
        target = _ietf_draft_uri_format % (draft_name)
        links.append(
            lsp.DocumentLink(
                range=link_range,
                target=target,
                tooltip=target,
            )
        )
    return links

_ieee_std_re = r'(?:IEEE[ ]?(?:Std )?([0-9]+(?:\.[0-9]+)?(?:\.[0-9]+)?(?:[A-Z]|[a-z])*)(?:-([0-9]{4}))?|([0-9]+(?:\.[0-9]+)?(?:\.[0-9]+)?(?:[A-Z]|[a-z])*)(?:-([0-9]{4}))? - IEEE)' #pylint: disable=line-too-long
_ieee_std_uri_format = 'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%%22Standard%%20Number%%22:%s)&ranges=%s_%s_Year' #pylint: disable=line-too-long
def _ieee_links(source: str):
    links = []
    matches = re.finditer(_ieee_std_re, source, re.A)
    for match in matches:
        sline, schar = linechar(source, match.start())
        eline, echar = linechar(source, match.end())
        link_range = lsp.Range(
            lsp.Position(sline, schar),
            lsp.Position(eline, echar),
        )
        std_num = match.group(1)
        if match.group(2):
            syear = match.group(2)
            eyear = syear
        else:
            syear = 1970
            eyear = datetime.now().year
        target = _ieee_std_uri_format % (std_num, syear, eyear)
        links.append(
            lsp.DocumentLink(
                range=link_range,
                target=target,
                tooltip=target,
            )
        )
    return links

# https://www.itu.int/en/ITU-T/publications/Pages/structure.aspx
_itut_trec_re = r'(?:(?:CCITT[-]?)?(?:ITU)?(?:-T )?(?:Recommendation )?)?([A-Z])\.([0-9][0-9]+(?:\.[0-9]+)?(?:\.[0-9]+)?)' #pylint: disable=line-too-long
_itut_trec_uri_format = 'https://www.itu.int/rec/T-REC-%s.%s'
def _itut_links(source: str):
    links = []
    matches = re.finditer(_itut_trec_re, source, re.A)
    for match in matches:
        sline, schar = linechar(source, match.start())
        eline, echar = linechar(source, match.end())
        link_range = lsp.Range(
            lsp.Position(sline, schar),
            lsp.Position(eline, echar),
        )
        series = match.group(1)
        trec = match.group(2)
        target = _itut_trec_uri_format % (series, trec)
        links.append(
            lsp.DocumentLink(
                range=link_range,
                target=target,
                tooltip=target,
            )
        )
    return links

_3gpp_ts_re = r'3GPP (?:TS )?([0-9]+).([0-9]+)'
_3gpp_ts_uri_format = 'https://www.3gpp.org/dynareport/%s%s.htm'
def _3gpp_links(source: str):
    links = []
    matches = re.finditer(_3gpp_ts_re, source, re.A)
    for match in matches:
        sline, schar = linechar(source, match.start())
        eline, echar = linechar(source, match.end())
        link_range = lsp.Range(
            lsp.Position(sline, schar),
            lsp.Position(eline, echar),
        )
        series = match.group(1)
        ts_num = match.group(2)
        target = _3gpp_ts_uri_format % (series, ts_num)
        links.append(
            lsp.DocumentLink(
                range=link_range,
                target=target,
                tooltip=target,
            )
        )
    return links

def text_document_document_link(
    ls: LanguageServer,
    params: lsp.DocumentLinkParams,
) -> Union[List[lsp.DocumentLink], None]:
    """Handles LSP `textDocument/documentLink` request."""
    links = []
    text_doc = ls.workspace.get_text_document(params.text_document.uri)
    source = text_doc.source

    links.extend(_ietf_links(source))
    links.extend(_ieee_links(source))
    links.extend(_itut_links(source))
    links.extend(_3gpp_links(source))

    return links

def register_callbacks(ls: LanguageServer):
    ls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_LINK)(text_document_document_link)
