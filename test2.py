from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.models import FlexSendMessage
from linebot.models.flex_message import BubbleContainer
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer
)

from linebot.v3.webhooks import MessageEvent, TextMessageContent
import requests
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import json
content = requests.get(
    'https://invoice.etax.nat.gov.tw/invoice.xml')
tree = ET.fromstring(content.text)
items = list(tree.iter(tag='item'))
title = items[0][0].text
ptext = items[0][3].text
ptext = ptext.replace('<p>', '').replace('</p>', ':')
ptext = ptext.replace('、', ':').replace('：', ':')
ptext = ptext.split(':')
special_1 = ptext[0] + " : " + ptext[1]
special_2_name = ptext[2]

s3 = ptext[4] + ptext[5]
s4 = ptext[4] + ptext[6]
s5 = ptext[4] + ptext[7]
templist = []
templist.append(ptext[0] + " : " + ptext[1])
templist.append(ptext[2])
templist.append(ptext[3])
templist.append(ptext[4])
templist.append(ptext[5])
templist.append(ptext[4])
templist.append(ptext[6])
templist.append(ptext[4])
templist.append(ptext[7])
print(templist)
