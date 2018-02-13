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
import regex
import bbcode

bbparse = bbcode.Parser()

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
        if from_id == 105301944:
            if command.startswith('/addpost'):
                    bot.sendChatAction(chat_id, 'typing')
                    posttext = getpost(query)
                    if posttext is not None:
                        posttext = regex.sub('\[QUOTE((.*?)!?\])(.*?)\[\/QUOTE\]', '', posttext, flags=regex.IGNORECASE)
                        posttext = bbparse.strip(posttext)
                        if posttext is not None:
                            with open('xda.txt', 'a') as xda:
                                xda.write(posttext + '\n')
                            bot.sendMessage(chat_id, 'Post added to model')
                        else:
                            bot.sendMessage(chat_id, 'Post ended up being empty')
                    else:
                        bot.sendMessage(chat_id, 'Invalid url')
            elif command.startswith('/addtext'):
                bot.sendChatAction(chat_id, 'typing')
                if command is not None:
                    modeltext = query.replace('\n', ' ').replace('\r', '')
                    with open('xda.txt', 'a') as xda:
                        xda.write(modeltext + '\n')
                    bot.sendMessage(chat_id, 'Post added to model')
                else:
                    bot.sendMessage(chat_id, 'Post cant be an empty string')



def on_inline_query(msg):
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    thanks = 0
    with open('xda.txt') as f:
        for i,l in enumerate(f):
            thanks += 1
        print(thanks)
    with open('xda.txt') as f:
        text = f.read()
    text_model = markovify.NewlineText(text, state_size=2)
    xda_post = text_model.make_short_sentence(430)
    if xda_post is not None:
        def compute():
            listobj = []
            listobj.append(InlineQueryResultArticle(
                id=str(6969), title='Enable VoLTE',
                input_message_content=InputTextMessageContent(
                    message_text=xda_post + '\n\nThe Following ' + str(thanks) + ' Users Say Thanks For This Useful Post'
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
