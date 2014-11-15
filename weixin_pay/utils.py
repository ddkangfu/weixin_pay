# -*- coding=utf-8 -*-

import hashlib

def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


def calculate_sign(params, auth_key):
    #签名步骤一：按字典序排序参数
    sorted(params)
    #签名步骤二：在string后加入KEY
    url = "&".join(['%s=%s'%(k, v) for (k, v) in params.items])
    url = '%s&key=%s' % (url, auth_key)
    #签名步骤三：MD5加密, 所有字符转为大写
    return hashlib.md5(url).upper()


def dict_to_xml(params):
    xml = ["<xml>",]
    for (k, v) in params.items():
        if (v.isdigit()):
            xml.append('<%s>%s</%s>' % (k, v, k))
        else:
            xml.append('<%s><![DATA[%s]]></%s>' % (k, v, k))
    xml.append('</xml>')
    return ''.join(xml)

if __name__ == '__main__':
    params = {"abc": 'abc123', "123": "123"}
    print dict_to_xml(params)
