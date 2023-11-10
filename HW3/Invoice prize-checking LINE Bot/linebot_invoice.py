from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import requests
import xml.etree.cElementTree as ET
app = Flask(__name__)

configuration = Configuration(
    access_token="3HekGAAKBbw0qtZqkTIf+NxHPo4QwTGt5q9k1pNLozIoaaw/MXwgNH2bjbXaEOmrA+lXqQxaINwDWLAnXBxQKSgkLApI4jpyITnyYZYLXC4zR0PjTI+Q2ybluF/5poF8xAhLB0Q5X+3kuwAX/czfNwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("8baf788747ba0562b3e6b9a2312fdc5c")


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
        ####################################
        if mtext == "@對獎":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請輸入發票最後三碼進行兌獎!")]
                )
            )
        elif mtext == "@前期中獎號碼":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=monoNum(1)+"\n\n"+monoNum(2))]
                )
            )
        elif mtext == "@本期中獎號碼":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=monoNum(0))]
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
