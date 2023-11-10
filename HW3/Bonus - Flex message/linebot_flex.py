from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
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
import xml.etree.cElementTree as ET
import json

app = Flask(__name__)

configuration = Configuration(
    access_token="")
handler = WebhookHandler("")


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info
        (
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        mtext = event.message.text
        ####################################

        def monoNum(n):
            content = requests.get(
                'https://invoice.etax.nat.gov.tw/invoice.xml')
            tree = ET.fromstring(content.text)
            items = list(tree.iter(tag='item'))
            title = items[n][0].text
            ptext = items[n][3].text
            ptext = ptext.replace('<p>', '').replace('</p>', '\n')
            return title + '\n' + ptext[:-1]

        def InvoiceToFlex(x):
            content = requests.get(
                'https://invoice.etax.nat.gov.tw/invoice.xml')
            tree = ET.fromstring(content.text)
            items = list(tree.iter(tag='item'))
            title = items[x][0].text
            ptext = items[x][3].text
            ptext = ptext.replace('<p>', '').replace('</p>', ':')
            ptext = ptext.replace('、', ':').replace('：', ':')
            ptext = ptext.split(':')
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
            contents = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Invoice",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "xl"
                        },
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": templist[0],
                            "size": "lg",
                            "color": "#FF0000",
                            "wrap": True,
                            "weight": "bold"
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "margin": "none",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": templist[1],
                                            "size": "md",
                                            "color": "#555555",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": templist[2],
                                            "size": "md",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": templist[3],
                                            "size": "md",
                                            "color": "#555555",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": templist[4],
                                            "size": "md",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": templist[5],
                                            "size": "md",
                                            "color": "#555555",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": templist[6],
                                            "size": "md",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": templist[7],
                                            "size": "md",
                                            "color": "#555555",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": templist[8],
                                            "size": "md",
                                            "color": "#111111",
                                            "align": "end",
                                            "weight": "bold"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
            return contents
        ####################################
        if mtext == "@對獎":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請輸入發票最後三碼進行兌獎!")]
                )
            )
        elif mtext == "@前期中獎號碼":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(
                        alt_text="hello", contents=FlexContainer.from_json(json.dumps(
                            {"type": "carousel", "contents": [InvoiceToFlex(1), InvoiceToFlex(2)]}))
                    )]
                )
            )
        elif mtext == "@本期中獎號碼":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[FlexMessage(
                        alt_text="hello", contents=FlexContainer.from_json(json.dumps(InvoiceToFlex(0))))]
                )
            )
        elif len(mtext) == 3 and mtext.isdigit():
            content = requests.get(
                'https://invoice.etax.nat.gov.tw/invoice.xml')
            tree = ET.fromstring(content.text)
            items = list(tree.iter(tag='item'))
            title = items[0][0].text
            ptext = items[0][3].text
            ptext = ptext.replace('<p>', '').replace('</p>', ':')
            ptext = ptext.replace('、', ':').replace('：', ':')
            temlist = ptext.split(':')
            prizelist = []
            prizelist.append(temlist[1][5:8])
            prizelist.append(temlist[3][5:8])
            prizelist.append(temlist[5][5:8])
            prizelist.append(temlist[6][5:8])
            prizelist.append(temlist[7][5:8])
            if mtext in prizelist:
                message = '符合某獎項後三碼，請自行核對發票前五碼!\n\n'
                message += monoNum(0)
            else:
                message = '很可惜，未中獎。請輸入下一張發票最後三碼。'
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=message)]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請輸入發票最後三碼進行兌獎!")]
                )
            )


if __name__ == "__main__":
    app.run()
