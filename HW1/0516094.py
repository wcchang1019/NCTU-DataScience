from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import sys
import os
start_time = time.time()


def ptt_one_page_articles(href, index):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    req = requests.get(href, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    article = soup.find_all('div', {'class': 'title'})
    date = soup.find_all('div', {'class': 'date'})
    boo_like = soup.find_all('div', {'class': 'nrec'})
    all_articles = open('all_articles.txt', 'a+')
    all_popular = open('all_popular.txt', 'a+')
    for count in np.arange(0, len(article)):
        if len(article[count]) > 1 and '公告' not in article[count].contents[1].contents[0]:
            try:
                boo_like[count] = int(boo_like[count].contents[0].text)
            except:
                if len(boo_like[count].contents) == 0:
                    boo_like[count] = 0
                elif boo_like[count].contents[0].text == '爆':
                    boo_like[count] = 100
            condition1 = (index == 1992 and date[count].contents[0].replace('/', '').replace(' ', '') == '101')
            condition2 = (index == 2340 and date[count].contents[0].replace('/', '').replace(' ', '') == '1231')
            condition3 = (index != 1992 and index != 2340)
            if condition1 or condition2 or condition3:
                all_articles.write(date[count].contents[0].replace('/', '').replace(' ', '')
                                   + ',' + article[count].contents[1].text
                                   + ',' + 'https://www.ptt.cc' + article[count].find_all('a')[0]['href'] + '\n')
                if boo_like[count] == 100:
                    all_popular.write(date[count].contents[0].replace('/', '').replace(' ', '')
                                      + ',' + article[count].contents[1].text
                                      + ',' + 'https://www.ptt.cc' + article[count].find_all('a')[0]['href'] + '\n')
    all_articles.close()
    all_popular.close()
    return True


def ptt_year_article(year):
    if os.path.exists("all_articles.txt"):
        os.remove("all_articles.txt")
    if os.path.exists("all_popular.txt"):
        os.remove("all_popular.txt")
    if year == 2017:
        for index in np.arange(1992, 2341):
            print(index)
            href = 'https://www.ptt.cc/bbs/Beauty/index' + str(index) + '.html'
            ptt_one_page_articles(href, index)
            time.sleep(0.5)
    return True


def ptt_article_boo_like(href):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    req = requests.get(href, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    push = soup.find_all('div', {'class': 'push'})
    df = pd.DataFrame(columns=['type', 'name'])
    for index in np.arange(0, len(push)):
        try:
            df.loc[len(df)] = [push[index].find_all('span', {'class': 'push-tag'})[0].text.replace(' ', ''),
                               push[index].find_all('span', {'class': 'push-userid'})[0].text]
        except:
            pass
    print(href, 'OK')
    return df


def ptt_time_interval_boo_like(df, start_date, end_date):
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    total = pd.DataFrame()
    for index in np.arange(0, len(df)):
        tmp = ptt_article_boo_like(df.iloc[index]['href'])
        total = total.append(tmp, ignore_index=True)
        time.sleep(0.5)
    file_name = 'push' + '[' + str(start_date) + '-' + str(end_date) + '].txt'
    if os.path.exists(file_name):
        os.remove(file_name)
    f = open(file_name, 'a+')
    f.write('all like: ' + str(total['type'].value_counts()['推']) + '\n')
    f.write('all boo: ' + str(total['type'].value_counts()['噓']) + '\n')
    push = total[(total['type'] == '推')]['name'].value_counts()
    push = push.reset_index(drop=False)
    push.columns = [0, 1]
    push = push.sort_values([1, 0], ascending=[False, True])
    boo = total[(total['type'] == '噓')]['name'].value_counts()
    boo = boo.reset_index(drop=False)
    boo.columns = [0, 1]
    boo = boo.sort_values([1, 0], ascending=[False, True])
    for index in np.arange(0, 10):
        f.write('like #' + str(index+1) + ': ' + str(push.iloc[index][0]) + ' ' + str(push.iloc[index][1]) + '\n')
    for index in np.arange(0, 10):
        f.write('boo #' + str(index+1) + ': ' + str(boo.iloc[index][0]) + ' ' + str(boo.iloc[index][1]) + '\n')
    f.close()
    return total


def read_file(file_name):
    try:
        all_articles = open(file_name, 'r')
    except OSError:
        print('please run crawl first')
    contents = all_articles.read()
    contents = contents.split('\n')
    df = pd.DataFrame(columns=['date', 'href'])
    for content in contents:
        if len(content) > 0:
            content = content.split(',')
            df.loc[len(df)] = [int(content[0]), content[-1]]
    return df


def ptt_get_img(href):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    req = requests.get(href, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    total = soup.find_all('a')
    lis = list()
    for test in total:
        if test['href'].endswith(('.jpg', '.jpeg', '.png', '.gif')):
            lis.append(test['href'])
    print(href, 'OK')
    return lis


def ptt_get_popular_img(df, start_date, end_date):
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    total = list()
    for index in np.arange(0, len(df)):
        total += (ptt_get_img(df.iloc[index]['href']))
        time.sleep(0.5)
    file_name = 'popular' + '[' + str(start_date) + '-' + str(end_date) + '].txt'
    if os.path.exists(file_name):
        os.remove(file_name)
    f = open(file_name, 'a+')
    f.write('number of popular articles:' + str(len(df)) + '\n')
    for index in np.arange(0, len(total)):
        f.write(str(total[index]) + '\n')
    f.close()
    return True


def keyword_judgment(keyword, href):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    req = requests.get(href, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    total = soup.find_all('div', {'id': 'main-container'})
    total = str(total).split('--')[0]
    if keyword in total:
        return True
    else:
        return False


def ptt_get_keyword_img(df, keyword, start_date, end_date):
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    total = list()
    for index in np.arange(0, len(df)):
        if keyword_judgment(keyword, df.iloc[index]['href']):
            total += (ptt_get_img(df.iloc[index]['href']))
            time.sleep(0.5)
    file_name = 'keyword(' + keyword + ')' + '[' + str(start_date) + '-' + str(end_date) + '].txt'
    if os.path.exists(file_name):
        os.remove(file_name)
    f = open(file_name, 'a+')
    for index in np.arange(0, len(total)):
        f.write(str(total[index]) + '\n')
    f.close()
    return True


def main():
    # index1992 2017 first post
    # index2340 2017 last post
    input_len = len(sys.argv)
    condition = input_len == 2 or input_len == 4 or input_len == 5
    if condition:
        if input_len == 2:
            if sys.argv[1] == 'crawl':
                ptt_year_article(2017)
        elif input_len == 4:
            if sys.argv[1] == 'push':
                start_date = int(sys.argv[2])
                end_date = int(sys.argv[3])
                df = read_file('all_articles.txt')
                ptt_time_interval_boo_like(df, start_date, end_date)
            elif sys.argv[1] == 'popular':
                start_date = int(sys.argv[2])
                end_date = int(sys.argv[3])
                df = read_file('all_popular.txt')
                ptt_get_popular_img(df, start_date, end_date)
        elif input_len == 5:
            if sys.argv[1] == 'keyword':
                keyword = str(sys.argv[2])
                start_date = int(sys.argv[3])
                end_date = int(sys.argv[4])
                df = read_file('all_articles.txt')
                ptt_get_keyword_img(df, keyword, start_date, end_date)
        else:
            print('incorrect input')
    else:
        print('incorrect input')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
