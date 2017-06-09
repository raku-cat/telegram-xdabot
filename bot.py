#!/usr/bin/env python3
import time
import sys
import markovify
import telepot
import json
import random
import os
from time import sleep
from telepot.loop import MessageLoop
from telepot.helper import InlineUserHandler, AnswererMixin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

with open(sys.path[0] + '/keys.json', 'r') as f:
    key = json.load(f)
bot = telepot.Bot(key['telegram'])

if not os.path.exists('xda.txt'):
    with open('xda.txt', 'w') as f:
        f.read

def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    with open('xda.txt') as f:
        text = f.read()
    text_model = markovify.NewlineText(text, state_size=1)
    xda_post = text_model.make_sentence()
    if xda_post is not None:
        def compute():
            listobj = []
            listobj.append(InlineQueryResultArticle(
                id=str(6969), title='Volte pls bro',
                input_message_content=InputTextMessageContent(
                    message_text=xda_post
                    )
                ))
            return { 'results' : listobj, 'cache_time' : 30 }
        answerer.answer(msg, compute)

answerer = telepot.helper.Answerer(bot)
MessageLoop(bot, on_inline_query).run_as_thread()
print('Started...')
while 1:
    sleep(10)