import requests
import re
import argparse


borsa_italiana = 'https://www.borsaitaliana.it'
get_list = ['/borsa/azioni/listino-a-z.html?initial=', '&page=']
get_pages_pattern = ['\/borsa\/azioni\/listino-a-z.html\?initial=', '&page=([0-9])']
get_name_pattern = '<title>Azioni ([A-Za-z0-9\'\-& ]+)\:'
get_code_pattern = 'Codice Alfanumerico<\/strong></span></td><td><span class="t-text -right">(\S+)<\/span>'
get_ISIN_pattern = {'MIB': '/borsa/azioni/scheda/(\S+).html',
                    'GEM': '/borsa/azioni/global-equity-market/scheda/(\S+).html',
                    'AIM': '/borsa/azioni/aim-italia/scheda/(\S+).html'}


def get_stock_info(r_text, filename, index):
    regex = re.compile(r'[\n\r\t]')
    txt = regex.sub('', r_text)
    name = re.findall(get_name_pattern, txt)
    name = name[0] if len(name) > 0 else ''
    symbol = re.findall(get_code_pattern, txt)
    if len(symbol) == 1:
        with open(filename, 'a+') as f:
            f.write('%s,%s,%s,%s\n' % (isin, symbol[0], name, index))
        print('\t%s, %s, %s, %s' % (isin, symbol[0], name, index))
    else:
        print('ERR: %s -> %s' % (isin, symbol))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='output file', required=True)
    args = parser.parse_args()

    outputfile = args.o

    with open(outputfile, 'w') as f:
        f.write('ISIN,SYMBOL,NAME\n')

    for i in range(ord('A'), ord('Z')+1):
        print('Processing %s...' % chr(i))
        r = requests.get(borsa_italiana + get_list[0] + chr(i))
        isin_list = {
            'MIB': list(set(re.findall(get_ISIN_pattern['MIB'], r.text))),
            'GEM': list(set(re.findall(get_ISIN_pattern['GEM'], r.text))),
            'AIM': list(set(re.findall(get_ISIN_pattern['AIM'], r.text)))
        }

        pages = list(set(re.findall(get_pages_pattern[0] + chr(i) + get_pages_pattern[1], r.text)))
        if len(pages) > 1:
            for p in pages:
                r = requests.get(borsa_italiana + get_list[0] + chr(i) + get_list[1] + p)
                isin_list['MIB'] += list(set(re.findall(get_ISIN_pattern['MIB'], r.text)))
                isin_list['GEM'] += list(set(re.findall(get_ISIN_pattern['GEM'], r.text)))
                isin_list['AIM'] += list(set(re.findall(get_ISIN_pattern['AIM'], r.text)))

        for el in isin_list:
            for isin in isin_list[el]:
                r = requests.get(borsa_italiana + get_ISIN_pattern[el].replace('(\S+)', isin))
                get_stock_info(r.text, outputfile, el)

    print('Done')
