# NCTU-DataScience

## HW1-PTT Web Crawler
### Setup
```
$ python3 -m venv venv
$ source test/bin/activate
$ pip install -r readme.txt
```
- Crawl the articles of Beauty in 2017 and create two files `all_articles.txt`
`all_polular.txt`
```
$ python 0516094.py crawl
```
- Calculate the boo and like total count to `push[start_date-end_date].txt`

```
# python 0516094.py push start_date end_date
$ python 0516094.py push 101 102
```
- Output the image url in popular articles to `popular[start_date-end_date].txt`
```
# python 0516094.py popular start_date end_date
$ python 0516094.py popular 101 1231
```
- Output the image url in specific keyword to `keyword(input)[start_date-end_date].txt`
```
# python 0516094.py keyword input start_date end_date
$ python 0516094.py keyword 正妹 101 1231
```
## HW2-Frequent Patterns (Apriori)
- run
```
$ make
$ [main.exe] [min_support] [inputFile] [outputFile]
```