from django.core.management.base import NoArgsCommand

import sys
import telepot
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegramBot.models import *


SUBSRIBE  = "訂閱課程"
COURSENOTI = "課程通知"
SEARCHFOOD = "查詢美食"
GPAFORECAST = "GPA預測"
USERSETTING = "使用者設定"
COUSRESRCH = "課程查詢"
USERHELP = "HELP"


class UserState:
    def __init__(self, chatid):
        self.sub_state = False
        self.sub_course_state = False

        self.coursenotf_state = False
        self.coursenotf_course_state = False

        self.food_state = False

        self.gpa_state = False
        self.gpa_myGPA_state = False
        self.gpa_getGPA_state = False

        self.setting_state = False
        self.setting_confirm_state = False
        self.setting_done = False

        self.general_state = True

        self.search_course_state = False
        self.search_course_list_state = False


        self.chat_id = chatid


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        users = [] 
        userstate = None      

        # should hide
        TOKEN = '242374964:AAE-_ZYNHBGItT6UZZT6chi7gaDsVGmCHA0'
        
        def on_chat_message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if(getUserState(chat_id) is None):
                print("new user", chat_id)
                userstate = UserState(chat_id)
                users.append(userstate)


            userstate = getUserState(chat_id)
            msg = msg['text']
            print(chat_id, msg)   
            if(not bePolite(chat_id, msg)): 
                #initialize state
                userstate.__init__(chat_id)
                return

            student = Student.objects.filter(chat_id = chat_id)
            if(len(student) == 0):
                userstate.setting_done = False
            else:
                userstate.setting_done = True

            service_keyboard = ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text=SUBSRIBE),KeyboardButton(text=COURSENOTI)], 
                                    [KeyboardButton(text=SEARCHFOOD),KeyboardButton(text=GPAFORECAST)],
                                    [KeyboardButton(text=USERSETTING),KeyboardButton(text=COUSRESRCH)]
                                ]
                            )     

            # state      
            if(userstate.general_state):
                if(msg == SUBSRIBE):
                    userstate.sub_state = True
                    userstate.general_state = False
                elif(msg == COURSENOTI):
                    userstate.coursenotf_state = True   
                    userstate.general_state = False                 
                elif(msg == SEARCHFOOD):
                    userstate.food_state = True
                    userstate.general_state = False
                elif(msg == GPAFORECAST):
                    userstate.gpa_state = True 
                    userstate.general_state = False                   
                elif(msg == USERSETTING):
                    userstate.setting_state = True
                    userstate.general_state = False
                elif(msg == COUSRESRCH):
                    userstate.search_course_state = True
                    userstate.general_state = False

             #使用者設定
            if(userstate.setting_state or (not userstate.setting_done)):
                if(userstate.setting_confirm_state):
                    flag = True
                    buff = msg.split("#")
                    # Check input
                    if (len(buff) != 3):
                        flag = False
                    for token in buff:
                        if(len(token) == 0):
                            flag = False
                    print(buff)
                    if(flag):                        
                        # save the user settings
                        # @DB involves, record Student attr.
                        bot.sendMessage(chat_id, "設定成功")
                        if(not userstate.setting_done):
                            newStudent = Student(sid = buff[0], name = buff[1], department = buff[2], chat_id = chat_id)
                            newStudent.save()
                            userstate.setting_done = True                        
                            bot.sendMessage(chat_id, '您好，請問您需要什麼服務？', reply_markup=service_keyboard)
                        else:
                            # 用 sid 找到要更新的人 (目前未擋幫別人更新)
                            updateStudentSet = Student.objects.filter(sid = buff[0])
                            updateStudentSet.update(name = buff[1], department = buff[2])
                        
                    else:
                        bot.sendMessage(chat_id, "設定失敗")
                    # state release
                    userstate.setting_confirm_state = False
                    userstate.setting_state = False
                    userstate.general_state = True
                    return

                    
                if(not userstate.setting_done):
                    bot.sendMessage(chat_id, "您需要設定個人的資料以利我們提供服務！\n 請輸入 '學號#姓名#系所' 設定，中間以#字隔開")                   
                else:
                    bot.sendMessage(chat_id, "請輸入 '學號#姓名#系所' 設定，中間以#字隔開")
                userstate.setting_confirm_state = True
                return

            # 訂閱課程
            if(userstate.sub_state):  
                #  決定是否訂閱              
                if(userstate.sub_course_state):
                    # msg = 課號
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists                                    
                    # display course information 
                    course_set = Course.objects.filter(cid = msg)
                    if(len(course_set) == 0):
                        bot.sendMessage(chat_id, "找不到該課程！")
                    else:
                        target_course = course_set[0]
                        bot.sendMessage(chat_id, target_course.cid + " " + target_course.name + " " + target_course.time)
                        bot.sendMessage(chat_id, "羽球中級")
                        # @DB involves, callback_data = "SUB_" + COURSEID   
                        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                           [InlineKeyboardButton(text='Yes', callback_data='SUB_' + target_course.cid ), InlineKeyboardButton(text='No', callback_data='SUB_FAIL')],
                        ])
                        bot.sendMessage(chat_id, "確定訂閱？", reply_markup=inline_keyboard)

                    # state release
                    userstate.sub_course_state = False
                    userstate.sub_state = False
                    userstate.general_state = True
                    return


                # 輸入訂閱課號
                bot.sendMessage(chat_id, "請輸入您要訂閱的課號：")
                if(userstate.sub_course_state == False):
                    userstate.sub_course_state = True
                    return



            # 課程通知
            if(userstate.coursenotf_state):   
                # 決定通知項目               
                if(userstate.coursenotf_course_state):
                    # msg = 課號
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists
                    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text="點名", callback_data='NOTF_ROLL_COURSEID'), InlineKeyboardButton(text="作業", callback_data='NOTF_HW_COURSEID')],
                    ])
                    bot.sendMessage(chat_id, "請問是課程還是作業通知呢？", reply_markup=inline_keyboard)

                    # state release
                    userstate.coursenotf_state = False
                    userstate.coursenotf_course_state = False
                    userstate.general_state = True
                    return
                # 輸入通知課號
                bot.sendMessage(chat_id, "請輸入要通知的課號：")
                userstate.coursenotf_course_state = True

            # 美食
            if(userstate.food_state):
                userstate.food_state = False
                userstate.general_state = True



            # GPA 預測
            if(userstate.gpa_state):
                forecastCourseID  = ""
                UserSelfPr = 50

                # Forecasrt result
                if(userstate.gpa_getGPA_state):   
                    UserSelfPr = msg                 
                    ResultGrade = forecastUserGrade(forecastCourseID, UserSelfPr)
                    bot.sendMessage(chat_id, "預測的等第：" + ResultGrade,reply_markup=service_keyboard)

                    # state release
                    userstate.gpa_getGPA_state = False
                    userstate.gpa_myGPA_state = False
                    userstate.gpa_state = False
                    userstate.general_state = True
                    return

                # 輸入PR值
                if(userstate.gpa_myGPA_state):
                    # save the courseID
                    # @DB involves, handle and find the course
                    # exception handling if course doesn't exists     
                    forecastCourseID = msg
                    # input user PR level
                    bot.sendMessage(chat_id, "請輸入您的PR值：")
                    userstate.gpa_getGPA_state = True
                    return
                 
                # 輸入通知課號
                bot.sendMessage(chat_id, "請輸入要預測的課號：",reply_markup=ReplyKeyboardRemove())
                userstate.gpa_myGPA_state = True

                   

            #課程查詢
            if(userstate.search_course_state):

                # msg = 課名
                # @DB involves, 用課名找到課號
                if(userstate.search_course_list_state):
                    bot.sendMessage(chat_id, "找到結果如下：")
                    bot.sendLocation(chat_id, 25.014038, 121.538184, disable_notification=None)
                    # state release
                    userstate.search_course_state = False
                    userstate.search_course_list_state = False
                    userstate.general_state = True
                    return



                bot.sendMessage(chat_id, "查詢課程相關資訊的服務！請輸入欲查詢的課名：")
                userstate.search_course_list_state = True
                



            if userstate.general_state == True:
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
                    tc = Take_Course()
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

        def getUserState(chat_id):
            for userstate in users:
                if userstate.chat_id == chat_id:
                    return userstate
            return None








        bot = telepot.Bot(TOKEN)
        bot.message_loop({'chat': on_chat_message,
                          'chosen_inline_result': on_chosen_inline_result, 'callback_query': on_callback_query},
                         run_forever='Listening ...')

