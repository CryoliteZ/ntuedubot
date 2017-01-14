from django.core.management.base import NoArgsCommand

import sys
import telepot
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from courses.models import Question

SUBSRIBE  = "訂閱課程"
COURSENOTI = "課程通知"
SEARCHFOOD = "查詢美食"
GPAFORECAST = "GPA預測"
USERSETTING = "使用者設定"
USERHELP = "HELP"


class UserState:
    def __init__(self):
        self.sub_state = False
        self.sub_course_state = False

        self.coursenotf_state = False
        self.coursenotf_course_state = False

        self.food_state = False

        self.gpa_state = False
        self.gpa_myGPA_state = False
        self.gpa_getGPA_state = False

        self.setting_state = False
        
        self.general_state = True



class Command(NoArgsCommand):
    def handle_noargs(self, **options):

        user = UserState()

        # should hide
        TOKEN = '242374964:AAE-_ZYNHBGItT6UZZT6chi7gaDsVGmCHA0'
        
        def on_chat_message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            msg = msg['text']
            print(chat_id, msg)   
            if(not bePolite(chat_id, msg)):    
                return


            service_keyboard = ReplyKeyboardMarkup(
                                    keyboard=[
                                        [KeyboardButton(text=SUBSRIBE),KeyboardButton(text=COURSENOTI)], 
                                        [KeyboardButton(text=SEARCHFOOD),KeyboardButton(text=GPAFORECAST)],
                                        [KeyboardButton(text=USERSETTING),KeyboardButton(text=USERHELP)]
                                    ]
                                )

            # state      
            if(user.general_state):
                if(msg == SUBSRIBE):
                    user.sub_state = True
                    user.general_state = False
                elif(msg == COURSENOTI):
                    user.coursenotf_state = True   
                    user.general_state = False                 
                elif(msg == SEARCHFOOD):
                    user.food_state = True
                    user.general_state = False
                elif(msg == GPAFORECAST):
                    user.gpa_state = True 
                    user.general_state = False                   
                elif(msg == USERSETTING):
                    user.setting_state = True
                    user.general_state = False

            # 訂閱課程
            if(user.sub_state):  
                #  決定是否訂閱              
                if(user.sub_course_state):
                    # msg = 課號
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists                                    
                    # display course information 
                    bot.sendMessage(chat_id, "羽球中級")
                    # @DB involves, callback_data = "SUB_" + COURSEID   
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='Yes', callback_data='SUB_COURSEID'), InlineKeyboardButton(text='No', callback_data='SUB_FAIL')],
                    ])
                    bot.sendMessage(chat_id, "確定訂閱？", reply_markup=inline_keyboard)

                    # state release
                    user.sub_course_state = False
                    user.sub_state = False
                    user.general_state = True
                    return


                # 輸入訂閱課號
                bot.sendMessage(chat_id, "請輸入您要訂閱的課號：")
                if(user.sub_course_state == False):
                    user.sub_course_state = True
                    return



            # 課程通知
            if(user.coursenotf_state):   
                # 決定通知項目               
                if(user.coursenotf_course_state):
                    # msg = 課號
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text="點名", callback_data='NOTF_ROLL_COURSEID'), InlineKeyboardButton(text="作業", callback_data='NOTF_HW_COURSEID')],
                    ])
                    bot.sendMessage(chat_id, "請問是課程還是作業通知呢？", reply_markup=inline_keyboard)

                    # state release
                    user.coursenotf_state = False
                    user.coursenotf_course_state = False
                    user.general_state = True
                    return
                # 輸入通知課號
                bot.sendMessage(chat_id, "請輸入要通知的課號：")
                user.coursenotf_course_state = True

            # 美食


            # GPA 預測
            if(user.gpa_state):
                forecastCourseID  = ""
                UserSelfPr = 50

                # Forecasrt result
                if(user.gpa_getGPA_state):   
                    UserSelfPr = msg                 
                    ResultGrade = forecastUserGrade(forecastCourseID, UserSelfPr)
                    bot.sendMessage(chat_id, "預測的等第：" + ResultGrade,reply_markup=service_keyboard)

                    # state release
                    user.gpa_getGPA_state = False
                    user.gpa_myGPA_state = False
                    user.gpa_state = False
                    user.general_state = True
                    return


                # 輸入PR值
                if(user.gpa_myGPA_state):
                    # save the courseID
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists     
                    forecastCourseID = msg
                    # input user PR level
                    bot.sendMessage(chat_id, "請輸入您的PR值：")
                    user.gpa_getGPA_state = True
                    return
                 
                # 輸入通知課號
                bot.sendMessage(chat_id, "請輸入要預測的課號：",reply_markup=ReplyKeyboardRemove())
                user.gpa_myGPA_state = True

               
            #使用者設定



            if user.general_state == True:
                bot.sendMessage(chat_id, '您好，請問您需要什麼服務？', reply_markup=service_keyboard)

        def on_callback_query(msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

            # For subsribe course callback
            if "SUB_" in query_data:                
                if(query_data == "SUB_FAIL"):
                    bot.answerCallbackQuery(query_id, text="取消訂閱，請問您還需要什麼服務？")
                else:
                    # subsricbe to course (get courseid by splitting query_data)
                    # @DB involves user and course subsribe relation
                    bot.answerCallbackQuery(query_id, text="訂閱成功，課程訊息不再漏接！")

            # For course notification callback  
            if "NOTF_" in query_data:
                # HW notification
                if "NOTF_HW_" in query_data:
                    # event occurs: courseid has HW (get courseid by splitting query_data)
                    # @DB involves: course and HW event relation
                    # @DB involves: find all users who has sub this course and boradcast notification
                    bot.answerCallbackQuery(query_id, text="已幫您通知同學們該交作業了！")
                elif "NOTF_ROLL_" in query_data:
                    # event occurs: courseid has HW (get courseid by splitting query_data)
                    # @DB involves  course and ROLL event relation
                    # @DB involves: find all users who has sub this course and boradcast notification
                    bot.answerCallbackQuery(query_id, text="已幫您通知大家點名了！")



            # print('Callback Query:', query_id, from_id, query_data)
    

        def on_chosen_inline_result(msg):
            result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
            print ('Chosen Inline Result:', result_id, from_id, query_string)


        def forecastUserGrade(courseid, selfpr):
            # compute forecast grade
            # function get DB grade data, do math return the forecast GPA
            # @DB involves, access grade data
            # need code
            Grade = "A"
            return Grade

        def bePolite(chat_id,msg):
            if(("幹" in msg)  and ("幹嘛" or "幹什麼") not in msg):
                bot.sendMessage(chat_id, "請保持應有的禮貌")
                return False
            elif("fuck" in msg.lower()):
                bot.sendMessage(chat_id, "Be polite my friend.")
                return False
            else:
                return True








        bot = telepot.Bot(TOKEN)
        bot.message_loop({'chat': on_chat_message,
                          'chosen_inline_result': on_chosen_inline_result, 'callback_query': on_callback_query},
                         run_forever='Listening ...')

