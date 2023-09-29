import time

import numpy as np # модуль обработки массивов
import cv2
import qrcode
import sys  # системный модуль

from kivy.lang import Builder
from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager

from kivy.core.window import Window

from kivy.properties import StringProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from PIL import Image, ImageDraw
import pandas as pd
import psycopg2
#НИЖЕ НЕ localhost !!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#ЭТО В ФАЙЛЕ ДОЛЖНО ХРАНИТЬСЯ
global id_user
id_user = 2901
global id_check
id_check = ''
global id_box_now
id_box_now = ''
#ВОТ ТО, ЧТО ВЫШЕ

Window.size = (400, 650)


class ContentNavigationDrawer(MDBoxLayout):
    pass


class GIROS(MDApp):
    def qr(self):
        connection = psycopg2.connect(host="localhost", port="2669", password="nast", dbname="GIROS", user="Nast")
        connection.autocommit = True
        video_capture = cv2.VideoCapture(0)
        data = ''
        global id_user
        global id_check
        global id_box_now
        while len(data) == 0:
            qrDecoder = cv2.QRCodeDetector()  # создание объекта детектора
            ret, frame = video_capture.read()
            data, bbox, rectifiedImage = qrDecoder.detectAndDecode(frame)

            #print(bbox)
            #print(type(bbox))

            if type(bbox) is np.ndarray:
                print('lt', bbox[0][3])
                print('rb', bbox[0][1])
                lt, rb = bbox[0][3], bbox[0][1]
                print(int(lt[0]), int(lt[1]), int(rb[0]), int(rb[1]))
                cv2.rectangle(frame, (int(lt[0]), int(lt[1])), (int(rb[0]), int(rb[1])), (0, 255, 0), 2)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) == 27:
                break

            if len(data) > 0:
                print("Decoded Data : {}".format(data))  # вывод декодированной строки
        id_box_now = int(data)
        str_select_if = "select payment from public.history_purch where payment = false and id_user = " + str(id_user)
        if len(pd.read_sql(str_select_if, connection)) == 0:
            connection.cursor().execute("INSERT INTO public.check_table default values")
            cursor = connection.cursor()
            cursor.execute("select max(id_check) from check_table")
            id_check = str(cursor.fetchone()[0])
        str_insert_1 = "INSERT INTO public.history_purch(id_check, id_user, id_place, time_open) " \
                       "VALUES (" + id_check +", " + str(id_user) + ", " \
                       "(Select id_place from history_place where id_box = " + str(id_box_now) + " and data_time_stop is NULL), " \
                       "(select now()));"
        connection.cursor().execute(str_insert_1)

        df_about_dish = pd.read_sql('select dish_name.id_dish, dish_name, calories, composition, '
                              'price_per_100, temp_storage, min_mass, mass_prev from history_purch, '
                              'history_place, dish_name '
                              'where history_place.id_place = history_purch.id_place '
                              'and history_place.id_dish = dish_name.id_dish '
                              'and history_purch.id_user = ' + str(id_user) +
                                    'and history_purch.payment = false', connection)

        #b = webbrowser.open(str(a))
        video_capture.release()
        cv2.destroyAllWindows()

        print('qr was activated')
        self.root.ids.LineListItem1.text = df_about_dish["dish_name"][0]
        self.root.ids.LineListItem1.secondary_text = '0'
        self.root.ids.LineListItem1.tertiary_text = 'Цена за 100 грамм: ' + str(df_about_dish["price_per_100"][0])
        return  id_user, id_check, id_box_now

    def pay(self):
        #self.root.screen_manager.current = 'pay'
        string = "test"  # строка для перевода в QR
        file = "for_pay_screen.jpg"  # файл для хранения полученного штрих кода
        image = qrcode.make(string)  # метод отвечает за преобразование строки в QR
        image.save(file)  # сохранение полученного объекта в файл myrusakov_out.jpg
        self.root.ids.qr_pay.reload()

    def cross(self):
        connection = psycopg2.connect(host="localhost", port="2669", password="nast", dbname="GIROS", user="Nast")
        connection.autocommit = True
        str_insert = 'update public.history_purch set time_close = (select NOW()) ' \
                     'where id_place = (select id_place from history_place where id_box = '+ str(id_box_now) + \
                     'and data_time_stop is NULL) ' \
                     'and mass_hbc is null and time_close is null'
        connection.cursor().execute(str_insert)
        time.sleep(2)
        df_about_dish = pd.read_sql('select dish_name.id_dish, dish_name, calories, composition, '
                                    'price_per_100, temp_storage, min_mass, mass_prev, mass_hbc from history_purch, '
                                    'history_place, dish_name '
                                    'where history_place.id_place = history_purch.id_place '
                                    'and history_place.id_dish = dish_name.id_dish '
                                    'and history_purch.id_user = ' + str(id_user) +
                                    'and history_purch.payment = false', connection)
        self.root.ids.LineListItem1.text = df_about_dish["dish_name"][0]
        self.root.ids.LineListItem1.secondary_text = str(float(df_about_dish["mass_prev"][0]) - float(df_about_dish["mass_hbc"][0]))
        self.root.ids.LineListItem1.tertiary_text = str((float(df_about_dish["mass_prev"][0]) - float(df_about_dish["mass_hbc"][0])) *\
                                                    df_about_dish["price_per_100"][0]/100)

    def build(self):
        return Builder.load_file("front.kv")


if __name__ == '__main__':
    GIROS().run()
run