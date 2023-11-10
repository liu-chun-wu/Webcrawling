from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    StickerMessage,
    LocationMessage,
    QuickReply,
    MessageAction,
    QuickReplyItem
)

from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

configuration = Configuration(access_token="uXah+5gMETXEDN9Gnbo0rJY0Fvtq5ZEzhEvujVWeI5aOtCxpaAT+QI9uM/EeLFP3A+lXqQxaINwDWLAnXBxQKSgkLApI4jpyITnyYZYLXC668g7EfS64j4meI2uYMOt6FW5w4Jg4mtH+DNlSuVns9gdB04t89/1O/w1cDnyilFU=")
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
        ####################################
        if event.message.text == "@傳送文字":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="111502522")]
                )
            )
        elif event.message.text == "@傳送圖片":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(
                        original_content_url="https://i.imgur.com/TA2Rpt0.jpg",
                        preview_image_url="https://i.imgur.com/TA2Rpt0.jpg"
                        )
                    ]
                )
            )
        elif event.message.text == "@傳送貼圖":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        StickerMessage(
                            package_id = "446",
                            sticker_id = "1988"
                        )
                    ]
                )
            )
        elif event.message.text == "@多項傳送":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        TextMessage(text="嗨!你好嗎"),
                        ImageMessage(
                            original_content_url="https://i.imgur.com/TA2Rpt0.jpg",
                            preview_image_url="https://i.imgur.com/TA2Rpt0.jpg"
                        ),
                        StickerMessage(
                            package_id = "446",
                            sticker_id = "1988"
                        )
                    ]
                )
            )
        elif event.message.text == "@傳送位置":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(
                            title = "National Central University",
                            address = "桃園市中壢區中大路300號",
                            latitude = 24.968972,
                            longitude = 121.1946
                        )
                    ]
                )
            )
        elif event.message.text == "@快速選單":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(
                        text="Your student Info",
                        quick_reply = QuickReply(
                            items=[
                                QuickReplyItem(action = MessageAction(label = "Name",text="Name")),
                                QuickReplyItem(action = MessageAction(label = "StudentID",text="StudentID")),
                                QuickReplyItem(action = MessageAction(label = "banana",text="banana"))
                                ]
                            )
                        )
                    ]
                )
            )
        elif event.message.text == "Name":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="劉俊吾")]
                )
            )
        elif event.message.text == "StudentID":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="111502522")]
                )
            )
        elif event.message.text == "banana":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(
                            original_content_url="https://i.imgur.com/sfb4sOT.jpg",
                            preview_image_url="https://i.imgur.com/sfb4sOT.jpg"
                        )
                    ]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )


if __name__ == "__main__":
    app.run()
