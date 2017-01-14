from django.core.management.base import NoArgsCommand

import sys
import telepot
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from courses.models import Question

class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        TOKEN = '256046468:AAHawEL3u2nPw3zd8_UWs2NCGa0__Xn-p4g'

        def on_chat_message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == 'text':
                bot.sendMessage(chat_id, msg['text'])
                # keyboard=[ [KeyboardButton(text="Yes"), KeyboardButton(text="No")] ]


                           # [InlineKeyboardButton(text='Press me', callback_data='press')],
                           # [InlineKeyboardButton(text='Press me', callback_data='press')]
                       

            bot.sendMessage(chat_id, 'Use custom keyboard', reply_markup=ReplyKeyboardMarkup(
                                        keyboard=[
                                            [KeyboardButton(text="訂閱課程"),KeyboardButton(text="課程通知")], 
                                            [KeyboardButton(text="查詢美食"),KeyboardButton(text="GPA預測")],
                                            [KeyboardButton(text="使用者設定"),KeyboardButton(text="Help")]
                                        ]
                                    ))
            print(msg['text']) 

        def on_inline_query(msg):
            query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
            print ('Inline Query:', query_id, from_id, query_string)

            articles = [InlineQueryResultArticle(
                            id='abc',
                            title='ABC',
                            input_message_content=InputTextMessageContent(
                                message_text='Hello'
                            )
                       )]

            bot.answerInlineQuery(query_id, articles)

        def on_callback_query(msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            print('Callback Query:', query_id, from_id, query_data)

            bot.answerCallbackQuery(query_id, text='Got it')

        def on_chosen_inline_result(msg):
            result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
            print ('Chosen Inline Result:', result_id, from_id, query_string)

        # TOKEN = sys.argv[1]  # get token from command-line

        bot = telepot.Bot(TOKEN)
        bot.message_loop({'chat': on_chat_message,'inline_query': on_inline_query,
                          'chosen_inline_result': on_chosen_inline_result, 'callback_query': on_callback_query},
                         run_forever='Listening ...')
         # Do your processing here
