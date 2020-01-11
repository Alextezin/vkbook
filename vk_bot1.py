import datetime
import sys
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from answers import *   

weekdays=["понедельник","вторник","среда",
                  "четверг","пятница","суббота","воскресенье"]

class VkBot():
    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id


    def answerer(self, text):
        # Расписание в зависимости от дня недели
        if text.lower() in weekdays:
            timetab=self.timetable(text)
            return timetab
        # Расписание звонков
        elif text.lower() == "расписание звонков":
            return rasp_zvon
        elif text.lower() == "клавиатура":
            return "клавиатура"
        elif text.lower() == "меню":
            return "меню"
        elif text.lower() == "расписание уроков":
            return "расписание уроков"
        elif text.lower() == "назад":
            return "назад"
        else:
            return "Я вас не понял!"
        # Список учебников
        #elif text.lower() in ('u', 'у'):
            #return 'textbooks'
        #else:
            #return "Я вас не понял!"
##        # Расписание на сегодня
##        else:
##            today = datetime.date.today()
##            wd = today.weekday()
##            chisl = today.isocalendar()[1] % 2
##            return rasp_chisl[wd] if chisl else rasp_znam[wd]
        
#Функция которая возвращает строку состоящая из дня недели и расписания в этот день 
    def timetable(self, text):
        i=0
        for day in weekdays:
            i+=1
            if day == text.lower():
                return rasp_today[i-1] + rasp_chisl[i-1]
