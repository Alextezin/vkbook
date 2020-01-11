import random
import datetime
import sys
import time
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import requests
import token
# --
from vk_bot1 import VkBot 
# --

s=0

#Функция write_msg получает id пользователя ВК <user_id>, которому оно отправит сообщение и собственно само сообщение .
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})

#Функция photos отправляет пользователю фотографию 
def photos(user_id):
    a=vk.method("photos.getMessagesUploadServer")
    b=requests.post(a['upload_url'], files={'photo': open('sasha.png','rb')}).json()
    c=vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    d="photo{}_{}".format(c["owner_id"], c["id"])
    vk.method('messages.send', {'user_id': user_id, 'attachment': d, 'random_id': random.randint(0, 2048)})

def get_button(label, color, payload=""):
    return{
        "action":{
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
            },
        "color": color
        }

##get_button(label="Понедельник", color="positive"),
##                get_button(label="Вторник", color="positive"),
##                get_button(label="Среда", color="positive"),
##                get_button(label="Четверг", color="positive"),
##                get_button(label="Пятница", color="positive"),
##                get_button(label="Суббота", color="positive")

def keyboarde(choice, i=0):
    if choice.lower()=="клавиатура":
        keyboard= {
            "one_time": False,
            "buttons":[
                [
                get_button(label="Меню", color="primary")
                ]
                ]
            }
        keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
        keyboard=str(keyboard.decode('utf-8'))
        #return keyboard
                
    elif choice.lower()=="меню":
        keyboard= {
            "one_time": False,
            "buttons":[
                [
                get_button(label="Расписание уроков", color="positive"),
                get_button(label="Расписание звонков", color="positive")
                ],
                [
                get_button(label="Назад", color="negative")
                ]
                ]
            }
        keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
        keyboard=str(keyboard.decode('utf-8'))

    elif choice.lower()=="расписание уроков":
        keyboard= {
            "one_time": False,
            "buttons":[
                [
                get_button(label="Понедельник", color="positive"),
                get_button(label="Вторник", color="positive")
                ],
                [
                get_button(label="Среда", color="positive"),
                get_button(label="Четверг", color="positive")   
                ],
                [
                get_button(label="Пятница", color="positive"),
                get_button(label="Суббота", color="positive")
                ],
                [
                get_button(label="Назад", color="negative")    
                ]
                ]
            }
        keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
        keyboard=str(keyboard.decode('utf-8'))

    elif choice.lower()=="назад" and i==3:
        keyboard= {
            "one_time": False,
            "buttons":[
                [
                get_button(label="Расписание уроков", color="positive"),
                get_button(label="Расписание звонков", color="positive")
                ],
                [
                get_button(label="Назад", color="negative")
                ]
                ]
            }
        keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
        keyboard=str(keyboard.decode('utf-8'))


    elif choice.lower()=="назад" and i==2:
        keyboard= {
            "one_time": False,
            "buttons":[
                [
                get_button(label="Меню", color="primary")
                ]
                ]
            }
        keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
        keyboard=str(keyboard.decode('utf-8'))
        
    return keyboard
        
      

##keyboard=json.dumps(keyboard,ensure_ascii=False).encode('utf-8')
##keyboard=str(keyboard.decode('utf-8'))

#Открываем файл с API-ключом созданный ранее
token_file = open('token.txt', 'r')

#Считываем ключ из файла
token=token_file.read().split('#')


# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token[0])

#Закрываем файл
token_file.close()

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")
while True:
    try:
        for event in longpoll.listen():

            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:

                    print(f'New message from {event.user_id}', end='')

                    bot = VkBot(event.user_id)
                    
                    answer = bot.answerer(event.text)

                    #vk.method('messages.send', {'user_id': event.user_id, 'message': "Выбери кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    
                    if answer.lower()=="я вас не понял!":
                        write_msg(event.user_id, answer+" Введите как показано на картинке")
                        photos(event.user_id)
                    elif answer.lower()=="клавиатура" and s==0:
                        s+=1#1
                        keyboard=keyboarde(answer)
                        vk.method('messages.send', {'user_id': event.user_id, 'message': "Выберите кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    elif answer.lower()=="меню" and s==1:
                        s+=1#2
                        keyboard=keyboarde(answer)
                        vk.method('messages.send', {'user_id': event.user_id, 'message': "Выберите кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    elif answer.lower()=="расписание уроков" and s==2:
                        s+=1#3
                        keyboard=keyboarde(answer)
                        vk.method('messages.send', {'user_id': event.user_id, 'message': "Выберите кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    elif answer.lower()=="назад" and s==3:
                        keyboard=keyboarde(answer, s)
                        s-=1
                        vk.method('messages.send', {'user_id': event.user_id, 'message': "Выберите кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    elif answer.lower()=="назад" and s==2:
                        keyboard=keyboarde(answer, s)
                        s-=1
                        vk.method('messages.send', {'user_id': event.user_id, 'message': "Выберите кнопку", 'keyboard': keyboard, 'random_id': random.randint(0, 2048)})
                    elif answer.lower()=="меню" and s!=1 or answer.lower()=="расписание уроков" and s!=2 or answer.lower()=="назад" and s!=3 or answer.lower()=="клавиатура" and s!=0:
                        write_msg(event.user_id, "Вы уже вводили данные команды или сейчас данные команды не доступны. Введите как показано на картинке ")
                        photos(event.user_id)
                    else:
                        write_msg(event.user_id, answer)

    except Exception as E:
        print(E)
        time.sleep(1)

            #if event.text[0] == "/":
                #write_msg(event.user_id, commander.do(event.text[1::]))
            #else:
                #write_msg(event.user_id, bot.new_message(event.text))

            #print('Text: ', event.text)
            #print("-------------------")
