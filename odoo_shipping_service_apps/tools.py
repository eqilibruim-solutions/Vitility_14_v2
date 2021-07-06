# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
CharTable = [
    (ord(u'ä'), u'ae'),
    (ord(u'ö'), u'oe'),
    (ord(u'ü'), u'ue'),
    (ord(u'Ä'), u'Ae'),
    (ord(u'Ö'), u'Oe'),
    (ord(u'Ü'), u'ue'),
    (ord(u'ß'), u'ss'),
]
DomainVals = lambda domain:dict(map(lambda item :(item[0],item[2]),domain))
def ensure_str(string):
    return string and string or  '';

def get_encoded(text):
    try:
        return text.encode('utf-8')
    except UnicodeDecodeError, e:
        return str(text)
    except Exception, e:
        return str(text)
def wk_ignore(text):
    import unicodedata
    if not (isinstance(text, str) or isinstance(text, unicode)):
        return str(text)
    if isinstance(text, str):
        text = unicode(text, 'utf-8')
    return unicodedata.normalize('NFKD', (text)).encode('ASCII', 'ignore')

def wk_translit(text):
    text = get_encoded(text)
    res = text.decode('utf8').translate(dict(CharTable))
    return  wk_ignore(res)
