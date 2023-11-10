import requests
from bs4 import BeautifulSoup
url = 'http://www.taiwanlottery.com.tw/'

html = requests.get(url)
html.encoding = 'UTF-8'
sp = BeautifulSoup(html.text, 'lxml')
number = sp.select('.contents_box02')[0]
input = number.text
date = input[1:10]
chi = input[11:22]
order1 = input[38:55]
order2 = input[56:73]
section1 = input[35:38]
section2 = input[74:76]
print('StudentID: 111502522')
print("威力彩期數: "+date+" "+chi)
print("開出順序: "+order1)
print("大小順序: "+order2)
print(section1+": "+section2)
