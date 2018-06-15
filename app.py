import requests
import urllib.parse
import re
import random
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbModel import Images, DB_connect

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('uLkoN0+ed2cqEaU+kH0EWoKdgBl1hXA/95EaQ8WZEQyBRrR28Dkwbsgdfb/Xq7g4hQLzYD0fAZHgFtXSBqmDe6K5QpTUv42G9MjuvZs7spCxcM6sww2AJ/wLE13LbWd0UbNJLos4wdO5Y8Mwi+eb0QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8219a79f77e4a30b9f14ca52cdccdf6e')

token = '2013603382218265|Bn5X5MRhythURJ865FebY_kM53A'
fanpage = {"162599767271235":"艦隊Collection"}

client_id = '5a165b840d4337f'
client_secret = '4f6565aa49229f9515d026aee90de66300bebc0a'
album_id = 'vz4kB'

'''
@app.route("/")
def hello():
    return "Hello World!"
'''

def pattern_NTOU_Eat(text):
    patterns = [
        '想吃',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def pattern_No18(text):
    patterns = [
        '%%', '舔腿', '摳', '胸', '乳', '之空','緣之',
        '打槍', '尻槍', '掏槍', '濕','想%','想舔','嘿嘿嘿',
        '打飛', '射' , '色色的' ,'阿斯','開車',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def pattern_Nomurmur(text):
    patterns = [
        '恩','嗯', '喔', '哈哈', '呵','所以呢'
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def pattern_about(text):
    patterns = [
        'about', 'About', 'ABOUT', 'ABout', 'ABOut', 'ABOUt',
        'ABOUT', 'aBout', 'aBOut', 'aBOUt', 'aBOUT', 'abOut',
        'abOUt', 'abOUT', 'aboUt', 'aboUT', 'abouT', 'aBoUt',
        'aBoUT', 'AbOut', 'AbOUt', 'AbOUT', 'abOuT', 'AbOuT',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def pattern_help(text):
    patterns = [
        'help', 'Help', 'HElp', 'HELP', 'hElp', 'hELp',
        'hELP', 'heLp', 'heLP', 'helP', 'HeLp', 'HeLP',
        'HelP', 'hElP',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def pattern_hello(text):
    patterns = [
        '安安', '安', 'hi', 'HI', 'hello', '你好',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def pattern_mei(text):
    patterns = [
        'mei', 'Mei', 'MEi', 'MeI', 'MEI', 'mEi', 'mEI' ,'meI',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def pattern_NololiC(text):
    patterns = [
        '蘿莉', 'loli', '幼女','貝瑞',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

def pattern_KCI(text):
    patterns = [
        'KCI', 'kci', 'kancollectimage','KanCollectImage','KanCollect',
        'kancollect', 'kc', 'KC',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        
def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 200


def FE():
    ele = '1309707529076258'
    res = requests.get('https://graph.facebook.com/v2.10/{}/?fields=posts{{full_picture}}&access_token={}'.format(ele, token))
    content = []
    count = 0
    for information in res.json().get('posts').get('data'):
        if count == 5:
            break
        if 'full_picture' in information:
            count += 1
            content.append(information['full_picture'])
    return content


def driver():
    ele = '119133272075216'
    res = requests.get('https://graph.facebook.com/v2.10/{}/?fields=posts{{full_picture}}&access_token={}'.format(ele, token))
    content = []
    count = 0
    for information in res.json().get('posts').get('data'):
        if count == 5:
            break
        if 'full_picture' in information:
            count += 1
            content.append(information['full_picture'])
    return content


def Dcard():
    target_url = 'https://www.dcard.tw/f/ntou'
    head = 'https://www.dcard.tw/f/ntou/p/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for i, text in enumerate(soup.select('.PostEntry_root_V6g0r'),0):
        if i == 15:
            return content
        for index, txt in enumerate(re.split('[/]',text['href']),0):
            if index == 4:
                link = head + urllib.parse.quote_plus(txt,encoding = 'utf-8')
                content += '{}\n{}\n\n'.format(txt,link)
    return content


def U2():
    target_url = 'https://www.youtube.com/feed/trending?hl=zh-TW&gl=TW'
    head = 'https://www.youtube.com'
    res = requests.get(target_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, text in enumerate(soup.select('.yt-lockup-title a'),0):
        if index == 15:
            return content
        data = '{}\n{}\n\n'.format(text['title'],head + text['href'])
        content += data
    return content


def MEI():
    target_url = 'http://www.mei.ntou.edu.tw/bin/home.php'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, text in enumerate(soup.select('.ptname a'),0):
        if index == 15:
            return content
        data ='{}\n{}\n\n'.format(text['title'],text['href'])
        content += data
    return content


def ptt_beauty():
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
        else:
            article_list = craw_page(res, push_rate)
    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n\n'.format(article.get('rate', None), article.get('title', None),
                                             article.get('url', None))
        content += data
    return content


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq


def crawl_page_gossiping(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    article_gossiping_seq = []
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                url_link = 'https://www.ptt.cc' + link
                article_gossiping_seq.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete', e)
    return article_gossiping_seq


def connect_db(db_string):
    db_session = sessionmaker(bind=create_engine(db_string))
    return db_session()


def get_iu(session):
    nb = random.randint(0, session.query(Images).count()-1)
    img = session.query(Images).filter(Images.id == nb).one()
    session.close()
    return img


@handler.add(MessageEvent, message=TextMessage)


def handle_message(event):
    if pattern_hello(event.message.text):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="安安R~R~R~!!!"))
        return 0

    if event.message.text == "海大Dcard":
        content = Dcard()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == "u2":
        content = U2()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if pattern_mei(event.message.text):
        content = MEI()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if pattern_No18(event.message.text):
        if (random.randint(0,999)%2):
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/zJoNKZ4.jpg',
                preview_image_url='https://i.imgur.com/zJoNKZ4.jpg'
            )
        else:
            image_message = ImageSendMessage(
                original_content_url='https://i.imgur.com/vZYlFw1.jpg',
                preview_image_url='https://i.imgur.com/vZYlFw1.jpg'
            )
        line_bot_api.reply_message(
            event.reply_token,
            image_message)
        return 0
    
    if event.message.text == "隨便來張動漫圖":
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link.replace('http', 'https')
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if pattern_Nomurmur(event.message.text):
        url = "https://i.imgur.com/KSRU5Wo.jpg"
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    
    if event.message.text == 'GPED':
        url = "https://i.imgur.com/tmkhCoQ.png"
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if event.message.text == "轉系":
        content = ""

        chrome_options = Options()
        chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)

        wait = ui.WebDriverWait(browser, 100000)    # 生成等待物件 負責等網頁跑完的相關事項 100000是等待時間的最大值
        browser.get("http://academics.ntou.edu.tw/main-board.aspx")
        wait.until(lambda browser: browser.find_element_by_id('ContentPlaceHolder1_TextBox_search').is_displayed())  # 等網頁跑好
        browser.find_element_by_id('ContentPlaceHolder1_TextBox_search').send_keys('轉系')
        browser.find_element_by_id('ContentPlaceHolder1_iButton_SEARCH').click()
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        flag = 1
        for i in soup.find_all("a", {"class": "link_font"}):
            if re.search('錄取名單', i.get_text(), re.IGNORECASE) and re.search('107', i.get_text(), re.IGNORECASE):
                flag = 0
                print(i.get_text() + ' http://academics.ntou.edu.tw/' + i['href'])
                content = i.get_text() + ' http://academics.ntou.edu.tw/' + i['href']
        if flag:
            print('還沒放榜')
            content = '還沒放榜'
        browser.quit()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if event.message.text == '抽妹子':
        url = get_iu(connect_db(DB_connect))    # ptt_beauty()
        print(type(url.url))
        image_message = ImageSendMessage(
            original_content_url=url.url,
            preview_image_url=url.url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0

    if pattern_NTOU_Eat(event.message.text):
        text = event.message.text
        patterns_B = [
            '早餐','早',
        ]
        patterns_L = [
            '點心','宵夜','消夜'
        ]
        patterns_D = [
            '正餐',
        ]
        patterns_N = [
            '北寧',
        ]
        patterns_Z = [
            '中正',
        ]
        patterns_S = [
            '祥豐',
        ]
        patterns_C = [
            '近',
        ]
        patterns_M = [
            '中距離',
        ]
        patterns_F = [
            '遠',
        ]
        ST = []

        for pattern in patterns_B :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('早餐')
        for pattern in patterns_L :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('宵夜')
        for pattern in patterns_D :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('正餐')
        for pattern in patterns_N :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('北寧路')
        for pattern in patterns_Z :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('中正路')
        for pattern in patterns_S :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('祥豐街')
        for pattern in patterns_C :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('(近)')
        for pattern in patterns_M :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('(中程)')
        for pattern in patterns_F :
            if re.search(pattern, text, re.IGNORECASE):
                ST.append('(遠)')  

        restraunt =['早安美芝城 (祥豐街上) (近) [早餐]',
                    '瑞麟美而美 (祥豐街上) (近) [早餐]',
                    '510早午餐 (祥豐街上) (中程) [早餐]',
                    '富而美早餐店 (祥豐街上) (遠) [早餐]',
                    '祥豐早餐吧 (祥豐街上) (遠) [早餐]',
                    '超羣滷味 鹽酥雞 (祥豐街上) (近) [宵夜]',
                    '10元壽司 (祥豐街上) (近) [宵夜]',
                    '20元麵店 (祥豐街上) (遠) [宵夜]',
                    '切仔麵 (祥豐街上) (近) [正餐]',
                    '家鄉牛肉麵 (祥豐街上) (近) [正餐]',
                    '味美紅燒牛肉麵 (祥豐街上) (近) [正餐]',
                    '吉力串燒鹽酥雞 (祥豐街上) (近) [正餐]',
                    '金園美食館 (祥豐街上) (中程) [正餐]',
                    '鍋燒麵 (祥豐街上) (中程) [正餐]',
                    '丐幫魯味 (祥豐街上) (中程) [正餐]',
                    '普好食麵館 (祥豐街上) (中程) [正餐]',
                    '肥貓秘製酸辣湯 (祥豐街上) (中程) [正餐]',
                    '義起來玩吧 (祥豐街上) (中程) [正餐]',
                    '香米湯湯 (祥豐街上) (遠) [正餐]',
                    '阿MAN早午餐 (中正路上) (近) [早餐]',
                    'APPLE203早餐 (中正路上) (近) [早餐]',
                    '3Q脆皮雞排 (中正路上) (近) [宵夜]',
                    '小蘋果蔥抓餅 (中正路上) (近) [宵夜]',
                    '張家豆漿 (中正路上) (近) [宵夜]',
                    'ComeBuy (中正路上) (近) [宵夜]',
                    '超大杯甜品屋 (中正路上) (中程) [宵夜]',
                    '添好茶 (中正路上) (中程) [宵夜]',
                    '阿山蔬果行 (中正路上) (中程) [宵夜]',
                    '桂發巷小吃 (中正路上) (中程) [宵夜]',
                    '喜歡鹽酥雞 (中正路上) (中程) [宵夜]',
                    '吮指王超級雞車 (中正路上) (中程) [宵夜]',
                    '清心福全 (中正路上) (遠) [宵夜]',
                    '宜蘭包子 (中正路上) (遠) [宵夜]',
                    '佬地方牛排 (中正路上) (遠) [宵夜]',
                    '冰火菠蘿 (中正路上) (遠) [宵夜]',
                    '熊豆咖啡 (中正路上) (遠) [宵夜]',
                    '找到幸福咖啡店 (中正路上) (遠) [宵夜]',
                    '8味超大捲 (中正路上) (遠) [宵夜]',
                    '捌壹捌麵館 (中正路上) (近) [正餐]',
                    '涼麵小舖 (中正路上) (近) [正餐]',
                    '三媽臭臭鍋 (中正路上) (近) [正餐]',
                    '合成便當 (中正路上) (中程) [正餐]',
                    '星翔快餐店 (中正路上) (近) [正餐]',
                    '馬來西亞風味餐 (中正路上) (中程) [正餐]',
                    '八方雲集 (中正路上) (中程) [正餐]',
                    '食神刷刷鍋 (中正路上) (中程) [正餐]',
                    '港式便當 (中正路上) (中程) [正餐]',
                    '陳家麵店 (中正路上) (中程) [正餐]',
                    '河豚很多 (中正路上) (中程) [正餐]',
                    '竇妹泰雲料理 (中正路上) (中程) [正餐]',
                    '涵館 (中正路上) (中程) [正餐]',
                    '海大燒臘店 (中正路上) (中程) [正餐]',
                    '來來快餐 (中正路上) (中程) [正餐]',
                    'Casa Picasso (中正路上) (遠) [正餐]',
                    '和平海岸熱炒 (中正路上) (遠) [正餐]',
                    '牛膳房 (中正路上) (遠) [正餐]',
                    '永和豆漿 (中正路上) (遠) [正餐]',
                    '霸味薑母鴨 (中正路上) (遠) [正餐]',
                    '北寧早餐店 (北寧路上) (近) [早餐]',
                    'C飲料甜品店 (北寧路上) (近) [宵夜]',
                    '中東創意料理 (北寧路上) (近) [正餐]',
                    '豪嘉粥品 (北寧路上) (近) [正餐]',
                    '小山羊碳烤三明治 (北寧路上) (近) [正餐]',
                    '日久阿囉哈 (北寧路上) (近) [正餐]',
                    '美滋客披薩 (北寧路上) (近) [正餐]',
        ]
        content = ""
        
        if len(ST) == 0:
            rnd = random.randint(0,len(restraunt)-1)
            for i,item in enumerate(restraunt,0):
                if i == rnd:
                    content = item
        else:
            for i,temp in enumerate(restraunt,0):
                flag = 0
                for pat in ST:
                    #print(pat)
                    #print(temp)
                    if not re.search(pat, temp, re.IGNORECASE):
                        flag = 1
                        break
                if flag == 0:
                    content += '{}\n'.format(temp)
        print(ST)
        if content == "":
            content = "沒有符合要求的店"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    
    if event.message.text == 'Driver?!':
        images = []
        for url in driver():
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            images.append(image_message)
        line_bot_api.reply_message(
            event.reply_token, images)
        return 0

    if pattern_KCI(event.message.text):
        content = ""
        a = []
        res = requests.get('https://graph.facebook.com/v2.10/{}/?fields=posts{{full_picture}}&access_token={}'.format("162599767271235", token))
        num = 0
        while num < 10:
            num+=1
            if num == 1:
                for information in res.json().get('posts').get('data'):
                    if 'full_picture' in information:
                        a.append(information['full_picture'])
                
                if 'next' in res.json().get('posts')['paging']:
                    res = requests.get(res.json().get('posts').get('paging')['next'])
                else:
                    break
                
            else:
                for information in res.json().get('data'):
                    if 'full_picture' in information:
                        a.append(information['full_picture'])
                    
                if 'next' in res.json()['paging']:
                    res = requests.get(res.json().get('paging')['next'])
                else:
                    break
                
        nb  = random.randint(0,len(a)-1)
        for index, information in enumerate(a,0):
            if index == nb:
                content = information
                url =information
                break
            
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        
        send = [image_message]#,TextSendMessage(text=content)]
        line_bot_api.reply_message(
            event.reply_token, send)
        return 0

    if pattern_NololiC(event.message.text):
        url = "https://i.imgur.com/cWTxA93.png"
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    
    if pattern_help(event.message.text):
        content ="""
海大Dcard
海大行事曆
mei
GPED
u2
靠北工程師
about
(有些隱藏指令請自行探索)
(本Bot無彩虹時段 請注意無色情內容)
        """
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "海大行事曆":
        im = ImageSendMessage(
            original_content_url='https://i.imgur.com/Dok0uGm.jpg',
            preview_image_url='https://i.imgur.com/Dok0uGm.jpg'
        )
        im1 = ImageSendMessage(
            original_content_url='https://i.imgur.com/YMVh1WW.jpg',
            preview_image_url='https://i.imgur.com/YMVh1WW.jpg'
        )
        image_message = [im1,im]
        line_bot_api.reply_message(
            event.reply_token,
            image_message)
        return 0

    if pattern_about(event.message.text):
        buttons_template = TemplateSendMessage(
            alt_text='關於 about',
            template=ButtonsTemplate(
                title='about line bot',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    URITemplateAction(
                        label='如何建立自己的 Line Bot',
                        uri='https://github.com/twtrubiks/line-bot-tutorial'
                    ),
                    URITemplateAction(
                        label='本Bot開發者',
                        uri='https://www.facebook.com/vbscript055246'
                    ),
                    URITemplateAction(
                        label='聯絡教學文作者',
                        uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    
    if event.message.text == 's':
        buttons_template = TemplateSendMessage(
            alt_text='快速服務',
            template=ButtonsTemplate(
                title='請選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='隨便來張動漫圖',
                        text='隨便來張動漫圖'
                    ),
                    MessageTemplateAction(
                        label='海大Dcard',
                        text='海大Dcard'
                    ),
                    MessageTemplateAction(
                        label='靠北工程師',
                        text='靠北工程師'
                    ),
                    MessageTemplateAction(
                        label='KanCollectImage',
                        text='KanCollectImage'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    
    #content = "請輸入help來確認指令或輸入s使用快捷(限手機)"
    #line_bot_api.reply_message(
        #event.reply_token,
        #TextSendMessage(text=content))
    return 0

if __name__ == "__main__":
    app.run()
