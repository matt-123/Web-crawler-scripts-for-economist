#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Authoer: Matt Chen
Last-modified:2012-1-11
"""
import httplib2
from BeautifulSoup import BeautifulSoup
from re import compile,sub
import os
import chardet

BASE_URL="http://www.economist.com"

def getList():
    h=httplib2.Http('.cache')
    reponse,content=h.request(BASE_URL)
    article_list=[]
    if (reponse.status==200):
        soup=BeautifulSoup(content.decode('utf-8'))
        tab=soup.findAll('section',{'class':compile('^ec-news-package')})
        for l in tab:
            article_dict={}
            l=l('a')[0]
            article_dict['title']=l.string
            article_dict['url']=l['href']
            article_list.append(article_dict)
    return article_list

def get_article(url):
    h=httplib2.Http('.cache')
    reponse,content=h.request(url)
    if(reponse.status==200):
        soup=BeautifulSoup(content.decode('utf-8'))
        ss=url.find('blog')
        if(ss!=-1):
            article=soup.find('div',{'class':'ec-blog-body'}).contents
        else:
            article=soup.find('div',{'class':compile('^ec-article-content')}).contents
    content=''
    for sc in article:
        sc=str(sc)
        sc=sc.replace('<p>','').replace('</p>','')
        sc=sc.replace('&mdash;','-')
        html_tag=compile(r'<[^>]+>')
        sc=sub(html_tag,'',sc)
        sc=sc.strip()
        sc+='\r\n'
        content+=sc
    return content

def write_article(path,content):
    #print path
    file=open(path,'w+')
    title=os.path.splitext(os.path.split(path)[1])[0]
    file.write(title+'\r\n\r\n')
    file.write(content)
    file.close()

def main():
    article_list=getList()
    for article in article_list:
        article_title=article['title']
        #article_title=str(article['title'])
        #print type(article_title),article_title.__class__
        #print article['title'].str()
        #print chardet.detect(article_title),'1'
        #article_title=article_title.decode('ISO-8859-2').encode('ascii')
        path=os.path.join(os.path.dirname(__file__),article_title+'.doc')
        path=path.replace('?','')
        print path
        #path=path.decode('ISO-8859-2').encode('utf-8')
        #print chardet.detect(path),'2'
        if os.access(path,os.F_OK):
            print "File [ %s ] have exit,skipping." %path
            continue
        article_url=BASE_URL+article['url']
        content=get_article(article_url)
        write_article(path,content)

if __name__=='__main__':
    main()





