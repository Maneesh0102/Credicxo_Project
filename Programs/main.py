from bs4 import BeautifulSoup
import requests
import time
import json
import pandas as pd

start = time.time()


df = pd.read_csv(r'C:\Users\MANEESH\Downloads\Amazon Scraping - Sheet1.csv')
d_l = []
for i in range(800,900):
  url = 'https://www.amazon.' + df['country'][i] + '/dp/' + str(df['Asin'][i])

  payload = {}
  headers = {
    'authority': 'www.amazon.de',
    'cache-control': 'max-age=0',
    'rtt': '250',
    'downlink': '1.15',
    'ect': '3g',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'http://localhost:8888/',
    'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8',
    'cookie': 'session-id=259-9049376-4750321; i18n-prefs=EUR; lc-acbde=en_GB; sp-cdn="L5Z9:IN"; ubid-acbde=259-1197239-7423742; session-token=A3TkGMKSLoZL0rtwUKVkdZKouOGHNr+VionER0GUCB6jhw0GT4zh6GGmWKVQikhNhC71vyuWQ+FtFIj8WtOgYQo0fa7YreiwAv0nac1HqT/kaRPk6CNo/1NmUV1UrMxiX75hzmAm5MQDolKWYipQjX5/Ks01aZFsq1BFmDEHunmTxns+g403DnChox1AYlKa; csm-hit=tb:HDYFM3VXRR0B67P0C1BQ+s-HDYFM3VXRR0B67P0C1BQ|1644934521120&t:1644934521121&adb:adblk_no; session-id-time=2082754801l; i18n-prefs=EUR; lc-acbde=en_GB; session-id=259-9049376-4750321; session-id-time=2082787201l; session-token=A3TkGMKSLoZL0rtwUKVkdZKouOGHNr+VionER0GUCB6jhw0GT4zh6GGmWKVQikhNhC71vyuWQ+FtFIj8WtOgYQo0fa7YreiwAv0nac1HqT/kaRPk6CNo/1NmUV1UrMxiX75hzmAm5MQDolKWYipQjX5/Ks01aZFsq1BFmDEHunmTxns+g403DnChox1AYlKa; ubid-acbde=259-1197239-7423742'
  }

  response = requests.request("GET", url, headers=headers, data=payload).text

  soup = BeautifulSoup(response, 'lxml')
  name = soup.select_one('#productTitle')
  d = {'link': url}
  if name:
    d['Product Title'] = name.text.strip()

    image_url = soup.select_one('#landingImage')
    if image_url:
      d['Product Image URL'] = image_url['src']

    else:
      image_url1 = soup.select_one('#imgBlkFront')
      d['Product Image URL'] = image_url1['src']

    price = soup.select_one('#mbc-price-1')
    price2 = soup.select_one('#a-autoid-0-announce .a-color-base')
    price3=soup.select_one('#price')
    if price:
      d['Price of the Product'] = price.text.strip()
    else:
      if price2:
        d['Price of the Product'] = price2.text.strip()
      elif price3:
        d['Price of the Product'] = price3.text
      else:
        d['Price of the Product'] = 'NOT AVAILABLE'

    des = soup.select_one("#productDescription_feature_div")
    des2 = soup.select_one('#detailBulletsWrapper_feature_div')
    if des:
      d["Product Details"] = des.text.strip()
    elif des2:
      d["Product Details"] = des2.text.strip().replace(' ','')


    else:
      d["Product Details"] = "NOT AVAILABLE"
  else:
    d['result'] = '404 Error'
  d_l.append(d)
  d = {}
  print(i)
print(d_l)
with open("800-899.json", "w" , encoding="utf-8") as writeJSON:

  json.dump(d_l,writeJSON, ensure_ascii=False)
end = time.time()
print(end - start)
