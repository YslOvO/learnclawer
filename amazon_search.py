import requests
import time
import re
from bs4 import BeautifulSoup
from time import sleep
main_url = "https://www.amazon.com"
headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
headers2 = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36","Connection": "close"}

#获取一个page下的urls
def GET_URL(url):
    L = []
    new_L=[]
    try:
        while len(L) == 0:
            response = requests.get(url,headers=headers)
            Soup = BeautifulSoup(response.text,'lxml')
            soup=Soup.select("a['class=a-link-normal a-text-normal']")
            sleep(2)
            for s in soup:
                L.append(main_url + s['href'].replace('https://www.amazon.com',''))
        for i in range(int(len(L)/2)):
            new_L.append(L[2*i+1])
        return new_L
    except:
        print('cannot GET URLS')
        return None

def GET_TITTLE(Soup):
    #商品名称
    title = (Soup.select('span["id=productTitle"]')[0].text.strip())
    return title

def GET_DESCRIPT(Soup):
    #商品描述
    descript=Soup.find_all("ul","a-unordered-list a-vertical a-spacing-none")[0].get_text().strip().replace('\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n \n\t\t\t\t\t\t\t', ';')
    descript=descript.replace('\t','').replace('\n',' ')
    return descript

def GET_SCORE(Soup):
    #获取商品的评分
    score = Soup.select('i["class=a-icon a-icon-star a-star-4-5"]')[0].text 
    if score =='':
        score = Soup.select('i["class=a-icon a-icon-star a-star-4"]')[0].text
        if score == '':
            score = Soup.select('i["class=a-icon a-icon-star a-star-3-5"]')[0].text 
    return score

def GET_REVIEW_NUM(Soup):
    #获取商品REVIEW数量
    review_num = Soup.select('span["id=acrCustomerReviewText"]')[0].text
    return review_num

def GET_ANSWER_NUM(Soup):
    #获取商品ANSWERED QUESTIONS数量
    answer_num = Soup.select('a["class=a-link-normal askATFLink"]')[0].text.strip()
    return answer_num

def GET_PRICE(Soup):
    #获取商品价格
    price = Soup.select('span["id=priceblock_ourprice"]')[0].text.strip()
    return price

def GET_COLOR(Soup):
    #获取商品颜色种类
    color_list = []
    Color = ''
    for ul in Soup.select('ul["class=a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches"]'):
        for li in ul.find_all('li'):
            color_list.append(li.attrs['title'])
    for i in range(len(color_list)):
        Color=Color+color_list[i]+';'
    return Color

def GET_DETAIL(Soup):
    try:
        ASIN,Date_listed='',''
        #在detail内
        product_detail=Soup.select('td["class=bucket"]')
        Soup2=BeautifulSoup(str(product_detail[0]),'lxml')
        div_content=Soup2.select('div["class=content"]')
        soup=BeautifulSoup(str(div_content[0]),'lxml').text
        print('detail in Product Detail')
        print('no date listed')
        #Shipping_Weight
        #pattern = re.compile('Shipping Weight: (.*?) \(View shipping rates and policies\)',re.S)
        #Shipping_Weight = re.findall(pattern, soup)[0]
        
        #ASIN
        try:
            pattern = re.compile('ASIN: (.*?)\n',re.S)
            ASIN = re.findall(pattern, soup)[0]
        except:
            print('no asin')
    except:
        try:
            #在information内
            product_info=Soup.select('div["id=productDetails_feature_div"]')
            Soup2=BeautifulSoup(str(product_info[0]),'lxml')
            div_content=Soup2.select('div["class=a-section table-padding"]')
            soup=BeautifulSoup(str(div_content[0]),'lxml').text
            print('detail in Product Information')
            #Product Dimensions 
            #pattern = re.compile('Product Dimensions\s*(.*?)\n',re.S)
            #Product_Dimensions  = re.findall(pattern, soup)[0]
            
            #Item Weight
            #pattern = re.compile('Item Weight\s*(.*?)\n',re.S)
            #Item_Weight = re.findall(pattern, soup)[0]
            #Shipping Weight
            #pattern = re.compile('Shipping Weight\s*(.*?) \(View shipping rates and policies\)',re.S)
            #Shipping_Weight = re.findall(pattern, soup)[0]
            
            #ASIN
            try:
                pattern = re.compile('ASIN\s*(.*?)\n',re.S)
                ASIN = re.findall(pattern, soup)[0]
            except:
                print('no asin')
            #Item model number
            #pattern = re.compile('Item model number\s*(.*?)\n',re.S)
            #Item_model_number = re.findall(pattern, soup)[0]
            
            #Date first listed on Amazon
            try:
                pattern = re.compile('Date first listed on Amazon\s*(.*?)\n',re.S)
                Date_listed = re.findall(pattern, soup)[0]
            except:
                print('no date listed')
        except:
            try:
                #在description内
                div_content=Soup.select('div["class=a-section a-spacing-none feature"]')
                soup=BeautifulSoup(str(div_content[0]),'lxml').text
                print('detail in Product Description')
                #ASIN
                try:
                    pattern = re.compile('ASIN:\s*(.*?)\n',re.S)
                    ASIN = re.findall(pattern, soup)[0]
                except:
                    print('no asin')
                #Date first listed on Amazon
                try:
                    pattern = re.compile('Date first listed on Amazon:\s*(.*?)\n',re.S)
                    Date_listed = re.findall(pattern, soup)[0]
                except:
                    print('no date listed')
            except:
                print('cannot read detail')
    detail=ASIN+';'+Date_listed
    return detail

def GET_RANK(Soup):
    try:
        #在detail内
        product_detail=Soup.select('td["class=bucket"]')
        Soup2=BeautifulSoup(str(product_detail[0]),'lxml')
        SalesRank=Soup2.select('li["id=SalesRank"]')
        soup=BeautifulSoup(str(SalesRank[0]),'lxml').text
        #Rank
        pattern = re.compile('#(.*?)\n\n\n',re.S)
        ALLRank = re.findall(pattern, soup)
        Rank=''
        for i in range(len(ALLRank)):
            rank=str(ALLRank[i]).replace('\\n',' ').replace('\\xa0',' ')
            Rank=Rank+';'+rank
        Rank=Rank.replace('\n',' ').replace('\xa0',' ').strip(';')
        print('rank in Product Detail')
    except:
        try:
            #在information内
            product_info=Soup.select('div["id=productDetails_feature_div"]')
            Soup2=BeautifulSoup(str(product_info[0]),'lxml')
            SalesRank=Soup2.find('td',{'class':False,'colspan':False,'id':False})
            L=''
            for i in SalesRank.strings:
                L=L+str(i)
            Rank=L.replace('\n\n#',';').strip(';\n')
            print('rank in Product Information')
        except:
            try:
                #在description内
                SalesRank=Soup.find('li',{'id':'SalesRank'})
                L=''
                len(SalesRank)
                for i in SalesRank.strings:
                    L=L+str(i)
                soup=re.sub('\.zg.*? } ',' ',L).replace('\n','  ').replace('\xa0',' ')
                pattern = re.compile('#(.*?)   ',re.S)
                ALLRank = re.findall(pattern, soup)
                Rank=''
                for i in range(len(ALLRank)):
                    Rank=Rank+';'+ALLRank[i]
                Rank=Rank.strip(';')
                print('rank in Product Description')
            except:
                print('url cannot read RANK')
    return Rank

#汇总
def GET_INFO(url):
    #解析
    response = requests.get(url,headers = headers2)
    Soup = BeautifulSoup(response.text,'lxml')
    
    #商品名称
    try:
        title = GET_TITTLE(Soup)
    except:
        print('no title  ',url)
        title = "none"
    
    #商品描述
    try:
        descript=GET_DESCRIPT(Soup)
    except:
        print('no descript  ',url)
        descript = "none"
    
    #获取商品的评分
    try:
        score = GET_SCORE(Soup)
    except:
        print('no score  ',url)
        score = "none"
    
    #获取商品REVIEW数量
    try:
        review_num = GET_REVIEW_NUM(Soup)
    except:
        print('no review_num  ',url)
        review_num = "none"
    
    #获取商品ANSWERED QUESTIONS数量
    try:
        answer_num = GET_ANSWER_NUM(Soup)
    except:
        print('no answer_num  ',url)
        answer_num = 'none'
    
    #获取商品价格
    try:
        price = GET_PRICE(Soup)
    except:
        print('no price  ' ,url)
        price = 'none'
        
    #获取商品颜色种类
    try:
        color = GET_COLOR(Soup)
    except:
        print('no color',url)
        color = 'none'
    
    #获取细节
    try:
        detail = GET_DETAIL(Soup)
    except:
        print('no detail',url)
        detail = 'none'
    
    #获取排名
    try:
        rank = GET_RANK(Soup)
    except:
        print('no rank',url)
        rank ='none'
    
    content='###product count:' + '\t' + title + '\t' + descript + '\t' + score + '\t' + review_num + '\t' + answer_num + '\t' + price + '\t' + color + '\t' + detail + '\t' + rank 
    #print('Title:',title, '\n \n', 'Dedescript:',descript,'\n \n','Score:',score,'\n \n','Review number:',review_num,'\n \n','Answer questions number:',answer_num,'\n \n','Price:',price,'\n \n','Color:',color,'\n \n','Detail:',detail,'\n \n''Rank:',rank,'\n \n')
    print(title,'\n')
    return content

def Get_pages_urls(pg):
    s = requests.session()
    s.keep_alive = True
    URLS = []
    for i in range(pg):
        urls = []
        page = i+1
        url = 'https://www.amazon.com/s/ref=sr_pg_' + str(page) + '?&page=' + str(page) + '&keywords=rice+cooker&ie=UTF8'
        urls = GET_URL(url)
        URLS.extend(urls)
        sleep(2)
    return URLS

def main(URLS):
    filename='search_result' + str(pg) + '.txt'
    file=open(filename, 'a', encoding='utf-8')
    s.keep_alive = False
    for i in range(len(URLS)):
        content=GET_INFO(URLS[i])
        file.write('\n'.join([content]))
        file.write('\n')
        sleep(2)
    file.close()

#只获取所有商品的url
if __name__ == '__main__':
    time_begin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    begin =time.time()
    
    pg=15
    URLS=Get_pages_urls(pg)
    #main(URLS)
    
    time_end=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end = time.time()
    print('\n','begin from:',time_begin)
    print('\n','end at:',time_end)
    print('\n','Running time: %s Seconds'%(end-begin))

#根据url爬取商品信息
s = requests.session()
s.keep_alive = False
time_begin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
begin =time.time()

pg=15
main(URLS)

end = time.time()
time_end=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print('\n','begin from:',time_begin)
print('\n','end at:',time_end)
print('\n','Running time: %s Seconds'%(end-begin))


