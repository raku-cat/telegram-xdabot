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
from getpost import getpost

with open(sys.path[0] + '/keys.json', 'r') as f:
    key = json.load(f)
bot = telepot.Bot(key['telegram'])

if not os.path.exists('xda.txt'):
    with open('xda.txt', 'w') as f:
        f.read
def on_command(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    if content_type == 'text':
        command = msg['text'].lower()
        from_id = msg['from']['id']
        try:
            query = command.split(' ',1)[1]
        except IndexError:
            return
        if command.startswith('/addpost'):
            if from_id == 105301944:
                bot.sendChatAction(chat_id, 'typing')
                posttext = getpost(command)
                if posttext is not None:
                    with open('xda.txt', 'a') as xda:
                        xda.write(posttext + '\n')
                    bot.sendMessage(chat_id, 'Post added to model')
                else:
                    bot.sendMessage(chat_id, 'Invalid url')


def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    with open('xda.txt') as f:
        text = f.read()
    text_model_dumb = markovify.NewlineText(text, state_size=1)
    xda_post_dumb = text_model_dumb.make_short_sentence(430)
    text_model = markovify.NewlineText(text, state_size=2)
    xda_post = text_model.make_short_sentence(430)
    if xda_post is not None:
        def compute():
            listobj = []
            listobj.append(InlineQueryResultArticle(
                id=str(6969), title='Volte pls bro',
                input_message_content=InputTextMessageContent(
                    message_text=xda_post_dumb
                    )
                ))
            listobj.append(InlineQueryResultArticle(
                id=str(6699), title='VoLTE please, brother.',
                input_message_content=InputTextMessageContent(
                    message_text=xda_post
                    )
                ))
            return { 'results' : listobj, 'cache_time' : 1 }
        answerer.answer(msg, compute)

answerer = telepot.helper.Answerer(bot)
MessageLoop(bot,{'chat' : on_command,
                  'inline_query' : on_inline_query}).run_as_thread()
print('Started...')
while 1:
    sleep(10)
