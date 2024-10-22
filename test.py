# import Token as T
# import telebot
# import json
# from datetime import date, time, datetime, timedelta
# from telebot import types
# import calendar

# user_data={}
# training={}

# bot=telebot.TeleBot(T.TOKEN)

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, 'Привет')


# @bot.message_handler(commands=['add_info'])
# def registration(message):
#     questions=['Введите Ваше ФИО:', 'Введите Ваш вес в кг:', "Введите Ваш рост в см:", "Введите Ваш год рождения:"]
#     keys=['name','weigh', 'growth', 'age']
#     user_data['id']=str(message.chat.id)
#     num=0
#     ask(message,questions,num,keys)

# def ask(message,questions,num, keys):
#     bot.send_message(message.chat.id, text=questions[num])
#     bot.register_next_step_handler_by_chat_id(message.chat.id, get_answer, questions,num,keys)

# def get_answer(message,questions,num,keys):
#     if num==1 or num==2 or num==3:
#         try:
#             int(message.text)
#             user_data[keys[num]]=message.text
#             if num==1 or num ==2:
#                 num+=1
#                 ask(message,questions,num,keys)
#             else:
#                 bot.send_message(message.chat.id, 'Данные успешно сохранены!')
#                 save_to_data(message)
#         except ValueError:
#             bot.send_message(message.chat.id, 'Введите ТОЛЬКО цифры')
#             ask(message,questions,num,keys)
#     elif num==0:
#         user_data[keys[num]]=message.text
#         num+=1
#         ask(message,questions,num,keys)


# def id_check(id,a):
#     b=a['users']
#     for i in b:
#         if i['id']==id:
#             return i
#     return None

# def schedule_check(id, day):
#     x=0
#     with open('data.json', 'r', encoding='UTF-8') as file:
#         a=json.load(file)
#         bobik=id_check(id,a)
#         if bobik!= None:
#             for i in bobik["trainings"]:
#                 print(f'работает {x}')
#                 x+=1
#                 if i["days_of_week"]!=day:
#                     print(i["days_of_week"])
#                     print(day)
#                     flag= True
#                     i["days_of_week"]
#                 else:
#                     return False
#     return flag

# def save_to_data(message):
#     with open('data.json', 'r', encoding='UTF-8') as file:
#         a=json.load(file)
#         b=a['users']
#         m=id_check(str(message.chat.id),a)
#         print(m)
#         if m==None:
#             user_data['trainings']=[]
#         elif m!=None:
#             user_data['trainings']=m['trainings']
#             b.remove(m)
#         print(user_data)
#         b.append(user_data)
#     with open('data.json', 'w', encoding='UTF-8') as file:
#         json.dump(a,file,ensure_ascii=False, indent=4)
#     bot.send_message(message.chat.id, 'Успешно сохранено!')
    

# @bot.message_handler(commands=['add_workout'])
# def start_add_workout(message):
#     questions=['Подробно опишите свою тренировку: упражнения, кол-во походов и длительность:', 'Сколько раз в неделю хотите тренироваться?', 'Выберите дни недели:']
#     keys=['describtion', 'howmany', 'days_of_week', 'exact_time']
#     num=0
#     bot.send_message(message.chat.id, 'Давайте приступим к созданию тренировки!')
#     add_workout(message, questions, keys, num)

# def add_workout(message, questions, keys, num):
#     if num==0 or num==1:
#         bot.send_message(message.chat.id, questions[num])
#         bot.register_next_step_handler_by_chat_id(message.chat.id, check_answers, questions, keys, num)
#     # for i in range(int(trainings['howmany'])):
#     if num==2:
#         for i in training['howmany']:
#             bot.send_message(message.chat.id, text=questions[num], reply_markup=generate_date_schedule(message))
#             num+=1
#     # bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=questions[num], reply_markup=generate_time_schedule())
    

# def check_answers(message, questions, keys, num):
#     if num==0:
#         training[keys[num]]=message.text
#         num+=1
#         add_workout(message, questions, keys, num)
#     elif num==1:
#         try:
#             if int(message.text) <=7 and int(message.text) >0:
#                 training[keys[num]]=message.text
#                 with open('data.json', 'r', encoding='UTF-8') as file:
#                     a=json.load(file)
#                     user=id_check(str(message.chat.id), a)
#                     print(user)
#                     print(message.chat.id)
#                     if user != None:
#                         user['trainings'].append(training)
#                         num+=1
#                         add_workout(message, questions, keys, num)
#                 with open('data.json', 'w', encoding='UTF-8') as file:
#                     json.dump(a,file,ensure_ascii=False, indent=4)
#             else: int('a')
#         except ValueError:
#             bot.send_message(message.chat.id, 'Введите ТОЛЬКО цифры, от 1 до 7')
#             add_workout(message, questions, keys, num)
#         training[keys[num]]=message.text

# @bot.callback_query_handler(func=lambda call: True)
# def handle_button_click(call):
#     if 'day' in call.data:
#         date = call.data.replace('day: ', '')
#         with open('data.json', 'r', encoding='UTF-8') as file:
#             a=json.load(file)
#             user=id_check(str(call.message.chat.id), a)
#             if user != None:
#                 for i in user['trainings']:
#                     if 'days_of_week' not in i:    
#                         i['days_of_week']=date
#         with open('data.json', 'w', encoding='UTF-8') as file:
#             json.dump(a,file,ensure_ascii=False, indent=4)
                        
#         bot.send_message(call.message.chat.id, text=f'Вы выбрали дату: {date}')
#         bot.send_message(call.message.chat.id, text='Выберите время:', reply_markup=generate_time_schedule())
#                 # bot.send_message(call.message.chat.id, text='Выберите время', reply_markup=generate_time_schedule(date))

#     elif 'time' in call.data:
#         time = call.data.replace('time: ', '')
#         with open('data.json', 'r', encoding='UTF-8') as file:
#             a=json.load(file)
#             user=id_check(str(call.message.chat.id), a)
#             if user != None:
#                 for i in user['trainings']:
#                     if 'exact_time' not in i:    
#                         i['exact_time']=f'{time}:00'
#                         bot.send_message(call.message.chat.id, text=f'Вы выбрали время: {time}:00')
#                         bot.send_message(call.message.chat.id, text=f"У вас тренировка по {i['days_of_week']} в {time}:00. Не забудьте!")
#         with open('data.json', 'w', encoding='UTF-8') as file:
#             json.dump(a,file,ensure_ascii=False, indent=4)

        
#         # add_appointment(date, time, 'Frank', 'nails')

# def generate_date_schedule(message):
#     keyboard=types.InlineKeyboardMarkup()
#     days_of_week = []
#     for i in list(calendar.day_name):
#         bot.send_message(message.chat.id, text=f'{i}, ?')
#         if schedule_check(str(message.chat.id), i) == True:
#             days_of_week.append(i)
#             # bot.send_message(message.chat.id, text=days_of_week[-1])
#             print(days_of_week)
#     for i in days_of_week:
#         data= f'day: {i}'
#         button=types.InlineKeyboardButton(text=str(i), callback_data=data)
#         keyboard.add(button)
#     return keyboard
    

# def generate_time_schedule():
#     keyboard=types.InlineKeyboardMarkup()
#     times = [str(s) for s in range(6,23)]
#     for i in times:
#         data= f'time: {i}'
#         button=types.InlineKeyboardButton(text=f'{i}:00', callback_data=data)
#         keyboard.add(button)

#     return keyboard




# bot.polling()



# # идеи:
# # спрашивать, уверен ли пользователь, что он хочет сменить свои данные и начать все заново
# # смотреть на сайте норму рост-вес пользователя
# # менять возраст пользователей в случае др


{
    "users": [
        {
            "id": "1989173964",
            "name": "Huff",
            "weigh": "444",
            "growth": "66",
            "age": "555",
            "trainings": []
        },
        {
            "id": "1490919662",
            "name": "Анатолий",
            "weigh": "76",
            "growth": "180",
            "age": "2008",
            "trainings": [
                {
                    "describtion": "Отжимания 1000 раз\nПресс 10000000000 раз\nПодтягивания 180 раз\nБархатные тяги 77 раз\nДлится тренировка 18 лет",
                    "howmany": "3",
                    "days_of_week": [
                        "Thursday"
                    ],
                    "exact_time": [
                        "10:00"
                    ]
                },
                {
                    "describtion": "Сальто передним задом лицом в цезарь 999 раз",
                    "howmany": "1",
                    "days_of_week": [
                        "Monday"
                    ],
                    "exact_time": [
                        "16:00"
                    ]
                },
                {
                    "describtion": "Жим стоя 1777 раз",
                    "howmany": "3",
                    "days_of_week": [
                        "Friday"
                    ],
                    "exact_time": [
                        "19:00"
                    ]
                }
            ]
        },
        {
            "id": "456253971",
            "name": "Дашдамиров Замир Ходаров",
            "weigh": "70",
            "growth": "170",
            "age": "2002",
            "trainings": []
        }
    ]
}



a='1'
f=[1,3,5,6,8]
print(f[-int])
