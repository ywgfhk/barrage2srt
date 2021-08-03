import os
import re
import html
import pandas as pd
import matplotlib.pyplot as plt

def xml_to_csv(filename):
    response_txt = open(filename+'.txt', mode='r', encoding='utf-8')
    response_str = response_txt.read()
    response_txt.close()

    response_txt = open(filename+"_parsed.txt", mode='w', encoding='utf-8')
    results = re.findall(r"<d\sp=\"(.*?</d>)", response_str, flags=re.DOTALL)
    # convert to CSV
    for r in results:
        # stripping unwanted newlines
        # replacing '">' and '</d>' with double quotes
        # replacing html escape characters
        # write each comment to file in a new line
        r = re.sub(r'\n', '', r)
        r = re.sub(r'\">', ',\"', r)
        r = re.sub(r'</d>', '\"\n', r)
        r = html.unescape(r)
        response_txt.writelines(r)
    response_txt.close()


def filter_csv_by_subs(filename, language='CN'):
    if language == 'CN':
        mode = 4
    elif language == 'EN':
        mode = 5
    else:
        print('language must be CN or EN')
    subs = pd.read_csv(filename+".txt", header=None)
    subs.columns = ['Timestamp', 'Mode', 'Lang', 'Char', '5', '6', 'Userid', '7', 'Text']
    filtered = subs.loc[lambda df: df['Mode'] == mode, :]
    filtered = filtered.sort_values(by=['Timestamp'])
    filtered.to_csv(r''+filename+'csv_filtered'+language+'_subs.csv', index=True)


def csv_to_subs():
    print('foo')


def main():
    #xml_to_csv('第一集')
    filter_csv_by_subs('第一集_parsed', language='CN')


if __name__ == "__main__":
    main()
