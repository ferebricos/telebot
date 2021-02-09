import json
import time
import math
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from telegram_bot_pagination import InlineKeyboardPaginator

#   load json data
FONTS_PATH = "fonts.json"
file = open(FONTS_PATH)
data = json.load(file)

#   consts
TOKEN = ''
ALPHABET = "0123456789АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
FONTS_COUNT = len(data['fonts'])
PAGINATOR_FONTSONPAGE = 4
PAGINTATOR_PAGES = math.ceil(FONTS_COUNT/PAGINATOR_FONTSONPAGE)

#   return fonted text
def get_fontedtext(text,fontid):
    newtext = ''
    for character in text:
        pos = ALPHABET.find(character)
        if pos != -1:
            newtext += data['fonts'][fontid]['characters'][character]
        else:
            newtext += character
    return newtext
#   return paginator markup
def get_paginator(page):
    paginator = InlineKeyboardPaginator(
        PAGINTATOR_PAGES,
        current_page=page,
        data_pattern='paginator#{page}'
    )
    return paginator.markup
#   return on_chat_message page for pagiantor
def get_page(page_number, text):
    if PAGINATOR_FONTSONPAGE*page_number > FONTS_COUNT:
        lastpage = FONTS_COUNT
    else:
        lastpage = PAGINATOR_FONTSONPAGE*page_number
    page = text + "\n"
    for i in range(page_number*PAGINATOR_FONTSONPAGE-PAGINATOR_FONTSONPAGE, lastpage):
        page += "\n" + data["fonts"][i]["title"]+": "+get_fontedtext(text,i)
    return page

#   BOT ACTIVITES

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type=="text":
        if msg["text"] == "/start":
            bot.sendMessage(chat_id,"Информация о боте....")
        elif msg["text"] == "/about":
            bot.sendMessage(chat_id,"Community K&K, idea @karoza, realization @ferebrico, technology https://coolsymbol.com/cool-fancy-text-generator.html")
        else:
            bot.sendMessage(chat_id,get_page(1,msg["text"]),reply_markup=get_paginator(1))
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    if query_data.split('#')[0] == "paginator":
        page_choosen = int(query_data.split('#')[1])
        # Ответ, чтобы не висел таймер около кнопки
        bot.answerCallbackQuery(query_id, text='')
        if msg['message']['reply_markup']['inline_keyboard'][0][page_choosen-1]['text'][0] != '·':
            bot.editMessageText(
                (msg['message']['chat']['id'],msg['message']['message_id']),
                get_page(page_choosen,msg['message']['text'].split("\n")[0]),
                reply_markup=get_paginator(page_choosen))

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)
        articles = []
        out = []
        for i in range(FONTS_COUNT):
            out.append(get_fontedtext(query_string,i))
            articles.append(InlineQueryResultArticle(
                        id=f"font_{i}",
                        title=f"{data['fonts'][i]['title']}: "+out[i],
                        input_message_content=InputTextMessageContent(
                            message_text=out[i]
                        )
                   ))
        return articles
    def getdefault():
        articles = []
        out = []
        for i in range(FONTS_COUNT):
            out.append(get_fontedtext("Пример текста (example)",i))
            articles.append(InlineQueryResultArticle(
                        id=f"font_{i}",
                        title=f"{data['fonts'][i]['title']}: "+out[i],
                        input_message_content=InputTextMessageContent(
                            message_text=out[i]
                        )
                   ))
        return articles
    if msg['query'] != '':
        answerer.answer(msg, compute)
    else:
        answerer.answer(msg, getdefault)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)




#   set bot
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10) 