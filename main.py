import Token as T
import telebot
import json
from datetime import date, time, datetime, timedelta
from telebot import types
import calendar

user_data={}
training={'describtion': None, 'howmany': None, 'days_of_week': [], 'exact_time': []}

bot=telebot.TeleBot(T.TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['add_info'])
def registration(message):
    questions=['Введите Ваше ФИО:', 'Введите Ваш вес в кг:', "Введите Ваш рост в см:", "Введите Ваш год рождения:"]
    keys=['name','weigh', 'growth', 'age']
    user_data['id']=str(message.chat.id)
    num=0
    ask(message,questions,num,keys)

def ask(message,questions,num, keys):
    bot.send_message(message.chat.id, text=questions[num])
    bot.register_next_step_handler_by_chat_id(message.chat.id, get_answer, questions,num,keys)

def get_answer(message,questions,num,keys):
    if num==1 or num==2 or num==3:
        try:
            int(message.text)
            user_data[keys[num]]=message.text
            if num==1 or num ==2:
                num+=1
                ask(message,questions,num,keys)
            else:
                save_to_data(message)
        except ValueError:
            bot.send_message(message.chat.id, 'Введите ТОЛЬКО цифры')
            ask(message,questions,num,keys)
    elif num==0:
        user_data[keys[num]]=message.text
        num+=1
        ask(message,questions,num,keys)


def id_check(id,a):
    b=a['users']
    for i in b:
        if i['id']==str(id):
            return i
    return None



def schedule_check(id, day):
    with open('data.json', 'r', encoding='UTF-8') as file:
        a=json.load(file)
        bobik=id_check(id,a)
        if bobik!= None:
            if bobik["trainings"]!=[]:
                for i in bobik["trainings"]:
                    for b in i["days_of_week"]:
                        if b!=day:
                            pass
                        else:
                            return False
    return True

def save_to_data(message):
    with open('data.json', 'r', encoding='UTF-8') as file:
        a=json.load(file)
        b=a['users']
        m=id_check(str(message.chat.id),a)
        print(m)
        if m==None:
            user_data['trainings']=[]
        elif m!=None:
            user_data['trainings']=m['trainings']
            b.remove(m)
        print(user_data)
        b.append(user_data)
    with open('data.json', 'w', encoding='UTF-8') as file:
        json.dump(a,file,ensure_ascii=False, indent=4)
    bot.send_message(message.chat.id, 'Успешно сохранено!')
    

@bot.message_handler(commands=['add_workout'])
def start_add_workout(message):
    questions=['Подробно опишите свою тренировку: упражнения, кол-во походов и длительность:', 'Сколько раз в неделю хотите выполнять данную тренировку?', 'Выберите дни недели:']
    keys=['describtion', 'howmany', 'days_of_week', 'exact_time']
    num=0
    with open('data.json', 'r', encoding='UTF-8') as file:
        a=json.load(file)
    if id_check(str(message.chat.id), a)!=None:
        bot.send_message(message.chat.id, 'Давайте приступим к созданию тренировки!')
        add_workout(message, questions, keys, num) 
    else: bot.send_message(message.chat.id, 'Чтобы создать тренировку необходима регистрация!\n /add_info')

def add_workout(message, questions, keys, num):
    if num==0 or num==1:
        bot.send_message(message.chat.id, questions[num])
        bot.register_next_step_handler_by_chat_id(message.chat.id, check_answers, questions, keys, num)
    if num==2:
        bot.send_message(message.chat.id, text=questions[num], reply_markup=generate_date_schedule(message))
        num+=1
    # bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=questions[num], reply_markup=generate_time_schedule())
    

def check_answers(message, questions, keys, num):
    if num==0:
        training[keys[num]]=message.text
        num+=1
        add_workout(message, questions, keys, num)
    elif num==1:
        try:
            if int(message.text) <=7 and int(message.text) >0:
                print(keys[num])
                training[keys[num]]=message.text
                num+=1
                add_workout(message, questions, keys, num)
            else: int('a')
        except ValueError:
            bot.send_message(message.chat.id, 'Введите ТОЛЬКО цифры, от 1 до 7')
            add_workout(message, questions, keys, num)
        training[keys[num]]=message.text

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    # if training['days_of_week'].isdigit:
    #     training['days_of_week']=[] 
    if 'day' in call.data:
        date = call.data.replace('day: ', '')
        print(training['describtion'])
        print(training['howmany'])
        print(training['days_of_week'])
        # print(training['exact_time'])
        training['days_of_week'].append(date)
        bot.send_message(call.message.chat.id, text=f'Вы выбрали дату: {date}')
        bot.send_message(call.message.chat.id, text='Выберите время:', reply_markup=generate_time_schedule())
                # bot.send_message(call.message.chat.id, text='Выберите время', reply_markup=generate_time_schedule(date))

    elif 'time' in call.data:
        time = call.data.replace('time: ', '')
        training['exact_time'].append(f'{time}:00')
        bot.send_message(call.message.chat.id, text=f'Вы выбрали время: {time}:00')
        if len(training['days_of_week']) == int(training['howmany']):
            with open('data.json', 'r', encoding='UTF-8') as file:
                a=json.load(file)
                user=id_check(str(call.message.chat.id), a)
                if user != None:
                    user['trainings'].append(training)  
                    bot.send_message(call.message.chat.id, text=f"У вас тренировка по {training['days_of_week']} в {time}:00. Не забудьте!")
            with open('data.json', 'w', encoding='UTF-8') as file:
                json.dump(a,file,ensure_ascii=False, indent=4)
        else:
            bot.send_message(call.message.chat.id, text='Выберите дни недели:', reply_markup=generate_date_schedule(call.message))

    elif 'delete' in call.data:
        delete = call.data.replace('delete: Удалить тренировку №', '')
        print(delete, 1234567890)
        with open('data.json', 'r', encoding='UTF-8') as file:
            a=json.load(file)
            user=id_check(str(call.message.chat.id), a)
            del user['trainings'][int(delete)-1]
        with open('data.json', 'w', encoding='UTF-8') as file:
                json.dump(a,file,ensure_ascii=False, indent=4)
        bot.send_message(call.message.chat.id, text='Готово! Тренировка удалена! Ну и оставайся жирдяем, лентяй!')

        
        # add_appointment(date, time, 'Frank', 'nails')

def generate_date_schedule(message):
    keyboard=types.InlineKeyboardMarkup()
    days_of_week = []
    for i in list(calendar.day_name):
        if schedule_check(str(message.chat.id), i) == True:
            days_of_week.append(i)
            # bot.send_message(message.chat.id, text=days_of_week[-1])
            # print(days_of_week)
    for i in days_of_week:
        data= f'day: {i}'
        button=types.InlineKeyboardButton(text=str(i), callback_data=data)
        keyboard.add(button)
        print(training['days_of_week'])
    return keyboard
    

def generate_time_schedule():
    keyboard=types.InlineKeyboardMarkup()
    times = [str(s) for s in range(6,23)]
    for i in times:
        data= f'time: {i}'
        button=types.InlineKeyboardButton(text=f'{i}:00', callback_data=data)
        keyboard.add(button)

    return keyboard



@bot.message_handler(commands=['delete_workout'])
def check_possibility(message):
    with open('data.json', 'r', encoding='UTF-8') as file:
        a=json.load(file)
        exact_user=id_check(message.chat.id, a)
    if exact_user!=None:
        if exact_user['trainings'] != []:  
            delete_workout(message, exact_user['trainings'])
        else: bot.send_message(message.chat.id, 'У вас нет тренировок')
    else: bot.send_message(message.chat.id, 'Вы не зарегистрированы! Необходима регистрация!\n /add_info')

def delete_workout(message, trains): 
    n=1
    which_delete=[]
    for_buttons=[]
    for i in trains:
        k=i['describtion']
        bot.send_message(message.chat.id, f'Тренировка №{n}:\n {k}')
        which_delete.append(n)
        n+=1
    print(which_delete)
    for i in which_delete:
        for_buttons.append(f'Удалить тренировку №{i}')
    bot.send_message(message.chat.id, text='Выберите какую тренировку хотите удалить:', reply_markup=delete_buttons(message, for_buttons))


def delete_buttons(message, for_buttons):
    keyboard=types.InlineKeyboardMarkup()
    for i in for_buttons:
        data= f'delete: {i}'
        button=types.InlineKeyboardButton(text=str(i), callback_data=data)
        keyboard.add(button)
        print(1)
    return keyboard


bot.polling()



# идеи:
# спрашивать, уверен ли пользователь, что он хочет сменить свои данные и начать все заново
# смотреть на сайте норму рост-вес пользователя
# менять возраст пользователей в случае др