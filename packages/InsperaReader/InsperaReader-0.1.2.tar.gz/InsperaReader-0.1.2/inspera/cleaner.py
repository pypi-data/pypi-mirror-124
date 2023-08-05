from html import unescape
import re

def clean_whitespace(data):
    data = ' '.join(data.split())
    return data.strip()

def clean_tokens(data, remove_nums=False):
    if remove_nums:
        data = re.sub(r'[0-9"]', '', data)
    data = re.sub(r'#[\S]+\b', '', data)
    data = re.sub(r'@[\S]+\b', '', data)
    
    illegal = ['`', '```']
    data = [d for d in data.split() if d not in illegal]
    
    return ' '.join(data)
    

def clean_html(data):
    data = unescape(data)
    tags = re.compile(r'<.*?>')
    data = tags.sub(u' ', data)
    data = re.sub('\==+', ' ', data)
    data = re.sub('\-+', ' ', data)
    data = re.sub('\\+', ' ', data)
    data = re.sub('\/+', ' ', data)
    data = data.replace(u'\xa0', u' ')  # nbsp in latin-1

    return data

def clean_all(data):
    data = clean_html(data)
    data = clean_whitespace(data)
    data = clean_tokens(data)

    return data