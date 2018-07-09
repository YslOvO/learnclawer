import requests
import time
import re
from bs4 import BeautifulSoup
from time import sleep
main_url = "https://www.amazon.com"
headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
s = requests.session()
s.keep_alive = False

#获取一个page下的urls
def GET_URL(url):
    L = []
    new_L=[]
    try:
        while len(L) == 0:
            response = requests.get(url,headers=headers)
            Soup = BeautifulSoup(response.text,'lxml')
            Soup2 = Soup.select('div["id=zg-center-div"]')
            center_div=BeautifulSoup(str(Soup2),'lxml')
            soup=center_div.select("a['class=a-link-normal']")
            sleep(2)
            for s in soup:
                L.append(main_url + s['href'])
        for i in range(int(len(L)/2)):
            new_L.append(L[2*i])
        return new_L
    except:
        print('cannot GET URLS')
        return None

#商品名称
def GET_TITTLE(Soup):
    title = (Soup.select('span["id=productTitle"]')[0].text.strip())
    return title

#商品描述
def GET_DESCRIPT(Soup):
    descript=Soup.find_all("ul","a-unordered-list a-vertical a-spacing-none")[0].get_text().strip().replace('\n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\n \n\t\t\t\t\t\t\t', ';')
    descript=descript.replace('\t','').replace('\n',' ')
    return descript

#获取商品的评分
def GET_SCORE(Soup):
    score = Soup.select('i["class=a-icon a-icon-star a-star-4-5"]')[0].text 
    if score =='':
        score = Soup.select('i["class=a-icon a-icon-star a-star-4"]')[0].text
        if score == '':
            score = Soup.select('i["class=a-icon a-icon-star a-star-3-5"]')[0].text 
    return score

#获取商品REVIEW数量
def GET_REVIEW_NUM(Soup):
    review_num = Soup.select('span["id=acrCustomerReviewText"]')[0].text
    return review_num

#获取商品ANSWERED QUESTIONS数量
def GET_ANSWER_NUM(Soup):
    answer_num = Soup.select('a["class=a-link-normal askATFLink"]')[0].text.strip()
    return answer_num

#获取商品价格
def GET_PRICE(Soup):
    price = Soup.select('span["id=priceblock_ourprice"]')[0].text.strip()
    return price

#获取商品颜色种类
def GET_COLOR(Soup):
    color_list = []
    Color = ''
    for ul in Soup.select('ul["class=a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches"]'):
        for li in ul.find_all('li'):
            color_list.append(li.attrs['title'])
    for i in range(len(color_list)):
        Color=Color+color_list[i]+';'
    return Color

#获取商品detail
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

#获取商品rank
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
    response = requests.get(url,headers = headers)
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

#url为排名page第一页的前面部分，依据需要修改
def main(pg):
    url = 'https://www.amazon.com/Best-Sellers-Electronics-Wearable-Technology/zgbs/electronics/10048700011/&pg=' + str(pg)
    urls = GET_URL(url)
    file=open('result.txt', 'a', encoding='utf-8')
    for i in range(len(urls)):
        content=GET_INFO(urls[i])
        file.write('\n'.join([content]))
        file.write('\n')
        sleep(2)
    file.close()

if __name__ == '__main__':
    time_begin=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    begin =time.time()
    for i in range(2):
        pg=i+1
        main(pg)
    time_end=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end = time.time()
    print('\n','begin from:',time_begin)
    print('\n','end at:',time_end)
    print('\n','Running time: %s Seconds'%(end-begin))