import json
import requests
import bs4
import glob
import pandas as pd

session = requests.Session()
def login():
    print('login')
    datas={
        'username': 'user',
        'password':'user12345'
    }
    res = session.post('http://0.0.0.0:5000/login',data=datas)
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    page_item = soup.find_all('li',attrs={'class':'page-item'})
    total_page = len(page_item)-2
    return total_page
def get_urls(page):
    print(f'get urls page {page}')
    params={
        'page':page
    }
    res=session.get('http://0.0.0.0:5000',params=params)
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    titles= soup.find_all('h4',attrs={'class':'card-title'})
    urls=[]
    for title in titles:
        url=title.find('a')['href']
        urls.append(url)
    return urls

def get_detail(url):
    print(f'get detail {url}')
    res=session.get(f'http://0.0.0.0:5000{url}')
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    title=soup.find('title').text.strip()
    price=soup.find('h4',attrs={'class':'card-price'}).text.strip()
    stock=soup.find('span',attrs={'class':'card-stock'}).text.strip().replace('stock','')
    category=soup.find('span',attrs={'class':'card-category'}).text.strip().replace('category','')
    description=soup.find('p',attrs={'class':'card-text'}).text.strip().replace('Description','')

    dict_data={
        'title':title,
        'price':price,
        'stock':stock,
        'category':category,
        'description':description
    }
    with open(f'./results/{url.replace("/","")}.json','w+') as outfile:
        json.dump(dict_data,outfile)

def create_csv():
    files=sorted(glob.glob('./results/*.json'))
    datas=[]
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)
    df = pd.DataFrame(datas)
    df.to_csv('results.csv', index=False)
    print('csv generated')

def run():
    total_page=login()
    options=int(input('Input Option Number:\n1.collecting all url\n2.get detail all product\n3.create csv\n'))
    if options==1:
        total_urls=[]
        for i in range(total_page):
            page=i+1
            urls=get_urls(page)
            total_urls+=urls
        with open('all_urls.json','w+') as outfile:
            json.dump(total_urls,outfile)
    elif options==2:
        with open('all_urls.json') as json_file:
            all_url = json.load(json_file)
        for url in all_url:
            get_detail(url)
    elif options==3:
        create_csv()

if __name__=='__main__':
    run()