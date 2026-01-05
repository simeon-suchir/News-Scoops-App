# Importing Required Modules  

import time,requests,json
from tkinter import messagebox
from tkinter import *
import tkinter.filedialog as filedialog
from tkinter import ttk
from PIL import ImageTk,Image
from tkinterweb.htmlwidgets import HtmlLabel
import textwrap
from tkhtmlview import HTMLLabel
import sqlite3
from datetime import datetime,date
import pandas
import itertools
from fpdf import FPDF
import unicodedata


# Setting Window Configurations 

window = Tk()
window.title('News Scoops')
window.overrideredirect(True)
w,h = window.winfo_screenwidth(),window.winfo_screenheight()
app_width,app_height=1280,720
x=(w/2)-(app_width/2)
y=(h/2)-(app_height/2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
window.iconphoto(False,ImageTk.PhotoImage(file='pics/News Scoop trans.png'))

# Setting Theme

window.tk.call('source','Sun-Valley-ttk-theme-master/sun-valley.tcl')
window.tk.call("set_theme", "dark")

# Initialising Account Database 

conector=sqlite3.connect('news_scoops_user_accounts.db')
cursor=conector.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS user_details(indexes integer PRIMARY KEY AUTOINCREMENT,name text NOT NULL,email text NOT NULL,password text NOT NULL,phno integer NOT NULL)')
conector.commit()
conector.close()

news_gen_connector=sqlite3.connect('news_scoops_news_gen.db')
news_gen_cursor=news_gen_connector.cursor()
news_gen_cursor.execute('CREATE TABLE IF NOT EXISTS news_gen( id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, url text NOT NULL , urltoimg text, content text )')
news_gen_connector.commit()
news_gen_connector.close()


# Defining Functions


def log_in_main_window():

    global in_which,where_list,menu_frame_info
    conector=sqlite3.connect('news_scoops_user_accounts.db')
    cursor=conector.cursor()
    email=email_id_textbox.get()
    passw=password_textbox.get()
    
    if email==''and passw=='':
        messagebox.showwarning('News Scoops','Enter Both Email  Password !')
    elif email=='' or passw=='':
        messagebox.showwarning('News Scoops','Enter Both Email Password !')
    if email!='' and passw!='':
        cursor.execute(f"SELECT COUNT(*) from user_details WHERE email = '{email}'")
        result=cursor.fetchone()
        

        if int(result[0])==0:
            messagebox.showwarning('News Scoops','This Username Does Not Exist !')
            email_id_textbox.delete(0,END)
            password_textbox.delete(0,END)

        else:
            cursor.execute(f"SELECT * from user_details WHERE email='{email}'")
            res=cursor.fetchone()
            if res[3] == passw:
                conector.commit()
                conector.close()
                email_id_textbox.delete(0,END)
                password_textbox.delete(0,END)
                log_in_window_label.forget()
                email_id_textbox.forget()
                password_textbox.forget()
                log_in_button.forget()
                create_account_button.forget()
                in_which='top headlines'  
                where_list=['top headlines']
                create_title_bar()
                create_weather_time_window()
                menu_frame_info='i-o'
                menu_place()
                populate(in_which)
                
            else:
                messagebox.showwarning('News Scoops','Wrong Password ! Please Enter Correct Password !')
                password_textbox.delete(0,END)
     
def reload():# Destroying The Inner Elements Then Proceeding

    news_frame1.destroy()
    populate(in_which)
    if menu_frame_info=='o-i':
        menu_mover()
    

def menu_mover():
    global menu_frame_info
    if menu_frame.winfo_x()==-305:
        for i in[-305,-200,-100,-20,0]:
            
            menu_frame.configure(menu_frame.place(x=i,y=103))
            window.update()
            time.sleep(0.01)
            menu_frame_info='o-i'
    else:
        for i in [0,-20,-100,-200,-305]:
            menu_frame.configure(menu_frame.place(x=i,y=103))
            window.update()
            time.sleep(0.01)
            menu_frame_info='i-o'


def getweather():

    global weatherdata,cityname
    weather_api_key='069dd683a7928cef21845176b4f9aa5f'
    cityname='Coimbatore'
    weather_api_link=f'https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={weather_api_key}'
    weatherdata=requests.get(weather_api_link).json()
    
news_pic_test_img=Image.open(r'pics\pic of news.png')
news_resized_pic_img=news_pic_test_img.resize((388,295),Image.Resampling.LANCZOS)
news_pic_img=ImageTk.PhotoImage(image=news_resized_pic_img)

def weather_populate():

    getweather()
    if weatherdata['cod']=='404':
        error_label=Label(weather_time_frame)
        error_label.place(x=60,y=60)
    else:
        temp=int(round(weatherdata['main']['temp']-273.15,0))
        weather_desp=weatherdata['weather'][0]['description'].title()
        hmdt=weatherdata['main']['humidity']
        windspd=weatherdata['wind']['speed']
        weather_icon = weatherdata['weather'][0]['icon']
        temp_min=str(int(round(weatherdata['main']['temp_min']-273.15,0))) +chr(0x2103)
        temp_max=str(int(round(weatherdata['main']['temp_max']-273.15,0))) +chr(0x2103)
        cityname_label=Label(weather_time_frame,text=cityname,font=('Heveltica',25),background='#2e2e2e')
        temp_label=Label(weather_time_frame,text=temp,font=('Heveltica',50),background='#2e2e2e')
        weather_desp_label=Label(weather_time_frame,text=weather_desp,font=('Heveltica',25),background='#2e2e2e')
        hmdt_label=Label(weather_time_frame,text=hmdt,font=('Heveltica',25),background='#2e2e2e')
        windspd_label=Label(weather_time_frame,text=windspd,font=('Heveltica',25),background='#2e2e2e')
        news_pic_label=Label(weather_time_frame,image=news_pic_img,borderwidth=0)
        weather_icon_label =HtmlLabel(weather_time_frame)
        temp_min_label=Label(weather_time_frame,text= temp_min,font=('Heveltica',18),background='white',foreground='black')
        temp_max_label=Label(weather_time_frame,text=temp_max,font=('Heveltica',18),background='white',foreground='black')
        cityname_label.place(x=35,y=150)
        temp_label.place(x=35,y=195)
        weather_desp_label.place(x=35,y=280)
        hmdt_label.place(x=200,y=330)
        windspd_label.place(x=250,y=380)
        news_pic_label.place(x=0,y=440)
        weather_icon_label.load_html(f"<html><body><img src='http://openweathermap.org/img/wn/{weather_icon}.png' style='width: 100px; height: 100px; object-fit: cover;' ></body></html>")
        weather_icon_label.place(x=250,y=165)
        temp_min_label.place(x=250,y=250)
        temp_max_label.place(x=310,y=250)

def convert(s):
    return unicodedata.normalize('NFKD', s).encode('latin-1', 'ignore').decode('latin-1')

def get_pdf():
    savedialog = filedialog.asksaveasfile(defaultextension='.pdf',initialdir='"C:/Users/SimiLemi/Documents',title='Save File',initialfile='News Scoops Todays Headlines')

    pdf = FPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 12)
    pdf.image('pics/News Scoop trans.png',x=85,y=10,w=40,h=40)
    pdf.ln(45)
    getnews('top headlines')
    for i in range(len(titles)):
        text=convert(titles[i])
        pdf.multi_cell(0,5,f'{i+1}. '+text.upper(),0,1)
        pdf.ln(5)
    pdf.output(savedialog.name)
       
def getnews(news_type):

    global titles,links_to_web,url_to_img,content_of_article
    country='us'
    api_key='69451af3dd2e48119efe3e9dcdd219c5'


    if news_type=='top headlines':
        url1=f'https://newsapi.org/v2/top-headlines?pageSize=40&country={country}&apiKey={api_key}'

    if news_type in ['business','entertainment','science','technology','sports','health']:
        url1=f'https://newsapi.org/v2/top-headlines?pageSize=40&category={news_type}&language=en&apiKey={api_key}'
         
    news1=requests.get(url1).json()


    articles1=news1['articles']

    for redarticle in articles1:
        del redarticle['source']
        del redarticle['author']
        del redarticle['description']
        del redarticle['publishedAt']

   
    df = pandas.json_normalize(articles1)
    
    news_gen_connector=sqlite3.connect('news_scoops_news_gen.db')
    news_gen_cursor = news_gen_connector.cursor()
    df.to_sql("news_gen",news_gen_connector,if_exists='replace')
    news_gen_cursor.execute('update news_gen set urlToImage="https://www.feednavigator.com/var/wrbm_gb_food_pharma/storage/images/9/2/8/5/235829-6-eng-GB/Feed-Test-SIC-Feed-20142.jpg" where urlToImage is null')
    news_gen_connector.commit()
    news_gen_cursor.execute('select * from news_gen')
    news_res=news_gen_cursor.fetchall()
    
    titles=[]
    links_to_web=[]
    url_to_img=[]
    content_of_article=[]
    
    for i in news_res :
        titles.append(i[1])
        links_to_web.append(i[2])
        url_to_img.append(i[3])
        content_of_article.append(i[4])

weather_pane_label_img=ImageTk.PhotoImage(file=r'pics\WEATHER PANE BLACK.png')

def create_weather_time_window():

    global time_label,weather_time_frame
    
    weather_time_frame=Frame(window,borderwidth=0)
    weather_time_label=Label(weather_time_frame,width=55,height=43,background='#2e2e2e')
    time_label=Label(weather_time_frame ,text='',background='#2e2e2e',font=('Helvetica',22))
    weather_pane_label=Label(weather_time_frame,image=weather_pane_label_img,borderwidth=0)
    weather_time_frame.place(x=0,y=103)
    weather_time_label.pack()
    time_label.place(x=30,y=20)
    weather_pane_label.place(x=0,y=140)
    clock()
    weather_populate()

def create_scroll_window(): #News Workspace

    global news_frame1,news_canvas,news_frame2,news_vsb 

    news_frame1= Frame(window,borderwidth=0)
    news_canvas=Canvas(news_frame1, borderwidth=0)
    news_frame2= Frame(news_canvas,borderwidth=0)
    news_vsb=Scrollbar(news_canvas, orient="vertical", command=news_canvas.yview)
    news_canvas.configure(yscrollcommand=news_vsb.set)
    news_frame2.bind("<Configure>",lambda e:news_canvas.configure(scrollregion= news_canvas.bbox("all")))
    news_frame1.place(x=390, y=103, width=1146, height=735)
    news_frame2.pack(fill=BOTH,expand=1)
    news_vsb.pack(side="right", fill="y")
    news_canvas.pack(side="left", fill="both", expand=True)
    news_canvas.create_window((0,0), window=news_frame2, anchor="nw",tags="news_frame2")

def menu_forget():

    menu_frame.destroy()
    top_headlines_button.destroy()
    technology_button.destroy()
    health_button.destroy()
    science_button.destroy()
    business_button.destroy()
    sport_button.destroy()
    entertainment_button.destroy()
    log_out_button.destroy()

def menu_place():
    
    global menu_frame,top_headlines_button,business_button,entertainment_button,science_button,technology_button,sport_button,health_button,log_out_button
    menu_frame=Frame(window,background='#2e2e2e',borderwidth=0)
    top_headlines_button=Button(menu_frame,image=top_headlines_button_img,borderwidth=0,bd=0,highlightthickness=0,command=top_headlines)
    business_button=Button(menu_frame,image=business_button_img,borderwidth=0,bd=0,highlightthickness=0,command=business)
    entertainment_button=Button(menu_frame,image=entertainment_button_img,borderwidth=0,bd=0,highlightthickness=0,command=entertainment)
    science_button=Button(menu_frame,image=science_button_img,borderwidth=0,bd=0,highlightthickness=0,command=science)
    technology_button=Button(menu_frame,image=technology_button_img,borderwidth=0,bd=0,highlightthickness=0,command=technology) 
    sport_button=Button(menu_frame,image=sport_button_img,borderwidth=0,bd=0,highlightthickness=0,command=sport)
    health_button=Button(menu_frame,image=health_button_img,borderwidth=0,bd=0,highlightthickness=0,command=health)   
    log_out_button=Button(menu_frame,image=log_out_button_img,borderwidth=0,bd=0,highlightthickness=0,command=log_out)
    menu_frame.place(x=-305,y=103,width=305,height=740)
    top_headlines_button.pack()
    technology_button.pack()
    health_button.pack()
    science_button.pack()
    business_button.pack()
    sport_button.pack()
    entertainment_button.pack()
    log_out_button.pack()

def read_more(e):

    menu_forget()
    menu_button.place_forget()
    get_pdf_button.place_forget()
    back_button_title.place_forget()
    reload_button.place_forget()
    news_frame1.destroy()

    def go_to_detail_window():

        global detail_title_label, detail_image_label
        global detail_content_string, detail_html_link_label, detail_content_label

        create_scroll_window()

        detail_label = Label(
            news_frame2,
            text='PREVIEW OF NEWS',
            font=('Verdana', 30),
            background='#1c1c1c',
            foreground='#154fe2'
        )
        detail_label.pack(pady=20)

        news_frame3 = Frame(news_frame2, background='black')
        news_frame3.pack(fill=BOTH, expand=1, pady=10)

        back_button.place(x=10, y=20)

        detail_title_value = titles[e]
        wrapper = textwrap.TextWrapper(width=75)
        detail_title_string = wrapper.fill(text=detail_title_value)

        detail_title_label = Label(
            news_frame3,
            text=detail_title_string,
            font=('Helvetica', 20, 'bold'),
            background='black',
            fg='white',
            justify=LEFT
        )
        detail_title_label.pack(anchor='nw', padx=30)

        img_url = url_to_img[e] if url_to_img[e] else "https://via.placeholder.com/1000x500"

        img_frame = Frame(news_frame3, background='black')
        img_frame.pack(fill='x', pady=30)

        detail_image_label = HtmlLabel(
            img_frame,
            messages_enabled=False
        )

        detail_image_label.load_html(
            f"""
            <html>
                <body style="text-align:center;">
                    <img src="{img_url}" width="1000" height="500"/>
                </body>
            </html>
            """
        )

        detail_image_label.pack()

        detail_content_value = content_of_article[e] or ""

        wrapper = textwrap.TextWrapper(width=70)
        detail_content_string = wrapper.fill(text=detail_content_value)

        for tag in ['<ul>', '</ul>', '<ol>', '</ol>', '<li>', '</li>']:
            detail_content_string = detail_content_string.replace(tag, '')

        detail_content_label = Label(
            news_frame3,
            text=detail_content_string,
            font=('Helvetica', 18),
            background='black',
            fg='white',
            justify=LEFT
        )
        detail_content_label.pack(padx=30, pady=30)

        detail_html_link_label = HTMLLabel(
            news_frame3,
            html=f"<h2><a href='{links_to_web[e]}'>READ MORE</a></h2>",
            background='black',
            width=30,
            height=5
        )
        detail_html_link_label.pack(anchor='center', pady=20)

        empty_label = Label(news_frame3, height=5, background='black')
        empty_label.pack()

    go_to_detail_window()

def back_button_cmd():
    
    menu_place()
    back_button.place_forget()
    menu_button.place(x=10,y=10)
    get_pdf_button.place(x=100,y=10)
    back_button_title.place(x=1310,y=10)
    reload_button.place(x=1425,y=10)
    news_frame1.destroy()
    populate(in_which)

ret=lambda e:(lambda p : read_more(e))

def populate(news_type):

    global newsshowerframe, news_empt_frame, htmllabels
    global title_label, author_label, htmllinks, which_news_label

    create_scroll_window()

    newsshowerframe = {}
    news_empt_frame = {}
    htmllabels = {}
    htmllinks = {}
    title_label = {}
    author_label = {}

    getnews(news_type)

    colour_list = [('#404040', 'white'), ('#2e2e2e', 'white')]
    colour_count = 0

    which_news_label = Label(
        news_frame2,
        text=in_which.upper(),
        font=('Verdana', 30),
        foreground='#154fe2'
    )
    which_news_label.pack(anchor='center', pady=20)

    for i in range(len(titles)):

        if colour_count >= len(colour_list):
            colour_count = 0

        newsshowerframe[i] = Frame(
            news_frame2,
            background=colour_list[colour_count][0]
        )
        newsshowerframe[i].pack(
            fill=BOTH, expand=1, padx=60, pady=30, anchor='nw', ipadx=9
        )
        newsshowerframe[i].bind('<Button-1>', ret(i))

        news_empt_frame[i] = Frame(
            newsshowerframe[i],
            background=colour_list[colour_count][0]
        )
        news_empt_frame[i].pack(fill=BOTH, expand=1, ipadx=16)
        news_empt_frame[i].bind('<Button-1>', ret(i))

        colour_count += 1

    colour_count = 0

    for i in range(len(titles)):

        if colour_count >= len(colour_list):
            colour_count = 0

        news_shower_text = list(str(titles[i]).rpartition('-'))

        if '-' in news_shower_text[0][-1:-4:-1]:
            temp_list = list(news_shower_text[0].rpartition('-'))
            news_shower_text[2] = temp_list[2] + '  ' + news_shower_text[2]
            news_shower_text[0] = temp_list[0]

        news_title_string = news_shower_text[0].title()
        news_author_text = news_shower_text[2].upper()

        wrapper = textwrap.TextWrapper(width=80)
        news_title_text = wrapper.fill(text=news_title_string)

        title_label[i] = Label(
            news_empt_frame[i],
            text=news_title_text,
            font=('Helvetica', 18),
            background=colour_list[colour_count][0],
            justify=LEFT,
            fg=colour_list[colour_count][1]
        )
        title_label[i].pack(anchor='nw')
        title_label[i].bind('<Button-1>', ret(i))

        author_label[i] = Label(
            news_empt_frame[i],
            text=news_author_text,
            font=('Helvetica', 16),
            background=colour_list[colour_count][0],
            fg=colour_list[colour_count][1]
        )
        author_label[i].pack(anchor='nw', pady=10)
        author_label[i].bind('<Button-1>', ret(i))

        colour_count += 1

    colour_count = 0

    for i in range(len(titles)):

        if colour_count >= len(colour_list):
            colour_count = 0

        htmllinks[i] = HTMLLabel(
            news_empt_frame[i],
            html=f"<h5><a href='{links_to_web[i]}'>READ MORE</a></h5>",
            background=colour_list[colour_count][0],
            width=20,
            height=5
        )
        htmllinks[i].pack(anchor='nw')

        colour_count += 1

    colour_count = 0

    for i in range(len(titles)):

        img_url = url_to_img[i] if url_to_img[i] else "https://via.placeholder.com/500x200"

        htmllabels[i] = HtmlLabel(
            newsshowerframe[i],
            messages_enabled=False
        )

        htmllabels[i].load_html(
            f"""
            <html>
                <body>
                    <img src="{img_url}" width="500" height="200"/>
                </body>
            </html>
            """
        )

        htmllabels[i].pack(anchor='center', pady=10)
        htmllabels[i].bind('<Button-1>', ret(i))

    

# Defining More Functions

def create_account_navigation():
    
    email_id_textbox.delete(0,END)
    password_textbox.delete(0,END)
    log_in_window_label.place_forget()
    email_id_textbox.place_forget()
    password_textbox.place_forget()
    log_in_button.place_forget()
    create_account_button.place_forget()
    create_account_window_label.pack()
    create_account_window_create_account_button.place(x=730,y=720)
    create_account_back_button.place(x=400,y=722)
    create_account_name_textbox.place(x=550,y=350)
    create_account_email_textbox.place(x=550,y=440)
    create_account_password_textbox.place(x=550,y=530)
    create_account_phno_textbox.place(x=550,y=620)


def create_account_window_create_account():
    
    new_name = create_account_name_textbox.get()
    new_email=create_account_email_textbox.get()
    new_password=create_account_password_textbox.get()
    new_phno=create_account_phno_textbox.get()
    if new_name=='' or new_email==''or new_password=='' or new_phno=='':
        messagebox.showwarning('News Scoops','Dont leave any fields empty !')
    else:
        
        
        is_email=True
        is_phno=True
        is_password=True
        warning=''
        if '@' not in new_email:
            is_email=False
            warning +='\nInvalid Email'
        else:
            split_email=new_email.partition('@')
            if split_email[2] not in ['gmail.com','reddit.com','yahoo.com','yahoo.co.in','hotmail.com','outlook.com']:
                is_email=False
                warning +='\nInvalid Email'

        if len(new_phno)!=10:
            is_phno=False
            warning+='\nInvalid Phno(Please Type 10-digit Phone Number)'
        if len(new_password)>20:
            is_password=False
            warning+='\nInvalid Password (Password Must be within 20 characters)'
        if is_email==False or is_phno==False or is_password==False:
            messagebox.showwarning('News Scoops',warning)
        
        if is_email and is_phno and is_password:
            conector=sqlite3.connect('news_scoops_user_accounts.db')
            cursor=conector.cursor()
            cursor.execute(f"SELECT COUNT(*) from user_details WHERE email = '{new_email}'")
            result=cursor.fetchone()
            print(result)
            if int(result[0])>0:
                
                messagebox.showwarning('News Scoops','The username already exists')
                create_account_name_textbox.delete(0,END)
                create_account_email_textbox.delete(0,END)
                create_account_password_textbox.delete(0,END)
                create_account_phno_textbox.delete(0,END)
            else:
                
                cursor.execute('INSERT INTO user_details(name,email,password,phno)VALUES(:name,:email,:password,:phno)',{'name':new_name,'email':new_email,'password':new_password,'phno':new_phno})
                conector.commit()
                conector.close()
                
                create_account_name_textbox.delete(0,END)
                create_account_email_textbox.delete(0,END)
                create_account_password_textbox.delete(0,END)
                create_account_phno_textbox.delete(0,END)

                create_account_window_label.pack_forget()
                create_account_window_create_account_button.place_forget()
                create_account_back_button.place_forget()
                create_account_name_textbox.place_forget()
                create_account_email_textbox.place_forget()
                create_account_password_textbox.place_forget()
                create_account_phno_textbox.place_forget()

                log_in_window_label.place(x=0,y=0)
                email_id_textbox.place(x=500,y=400)
                password_textbox.place(x=500,y=540)
                log_in_button.place(x=600,y=625)
                create_account_button.place(x=760,y=735)
                
                messagebox.showinfo('News Scoops','You have created your News Scoops Account!')


def top_headlines():

    global in_which
    
    menu_mover()
    news_frame1.destroy()
    populate('top headlines')
    which_news_label.configure(text='TOP HEADLINES')
    in_which='top headlines'
    where_list.append(in_which)


def business():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('business')
    which_news_label.configure(text='BUSINESS')
    in_which='business'
    where_list.append(in_which)


def entertainment():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('entertainment')
    which_news_label.configure(text='ENTERTAINMENT')
    in_which='entertainment'
    where_list.append(in_which)


def science():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('science')
    which_news_label.configure(text='SCIENCE')
    in_which='science'
    where_list.append(in_which)


def technology():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('technology')
    which_news_label.configure(text='TECHNOLOGY')
    in_which='technology'
    where_list.append(in_which)


def sport():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('sports')
    which_news_label.configure(text='SPORTS')
    in_which='sports'
    where_list.append(in_which)

def health():

    global in_which
    menu_mover()
    news_frame1.destroy()
    populate('health')
    which_news_label.configure(text='HEALTH')
    in_which='health'
    where_list.append(in_which)


def create_account_back():

    create_account_name_textbox.delete(0,END)
    create_account_email_textbox.delete(0,END)
    create_account_password_textbox.delete(0,END)
    create_account_phno_textbox.delete(0,END)

    create_account_window_label.pack_forget()
    create_account_window_create_account_button.place_forget()
    create_account_back_button.place_forget()
    create_account_name_textbox.place_forget()
    create_account_email_textbox.place_forget()
    create_account_password_textbox.place_forget()
    create_account_phno_textbox.place_forget()

    log_in_window_label.place(x=0,y=0)
    email_id_textbox.place(x=500,y=400)
    password_textbox.place(x=500,y=540)
    log_in_button.place(x=600,y=625)
    create_account_button.place(x=760,y=735)


def log_out():
    is_logout=messagebox.askyesno('News Scoops','Do you want to log out?')
    if is_logout==1:
        destroy_title_bar()
        menu_forget()
        news_frame1.destroy()
        weather_time_frame.destroy()
        time_label.destroy()

        log_in_window_label.place(x=0,y=0)
        email_id_textbox.place(x=500,y=400)
        password_textbox.place(x=500,y=540)
        log_in_button.place(x=600,y=625)
        create_account_button.place(x=760,y=735)

        messagebox.showinfo('News Scoops','You have been logged out')
    else:
        pass

weekday_list=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def clock():
    weekday=datetime.today().weekday()
    day=weekday_list[weekday]
    datetdy=date.today().strftime("%B %d, %Y")
    hour_clock=time.strftime("%I")
    minute_clock=time.strftime("%M")
    second_clock=time.strftime("%S")
    ampm_clock=time.strftime("%p")
    time_label.config( text = f'{day}  {datetdy}\n\n{int(hour_clock)}:{minute_clock}:{second_clock} {ampm_clock}')
    time_label.after(1000,clock)

def back_button_title_comm():

    global in_which,where_list

    where_list = [g for g,_ in itertools.groupby(where_list)]
    
    if  len(where_list) !=1:
        news_frame1.destroy()
        populate(where_list[len(where_list)-2])
        which_news_label.configure(text=where_list[len(where_list)-2].upper())
        in_which = where_list[len(where_list)-2]
        del where_list[len(where_list)-1]
        if menu_frame_info=='o-i':
            menu_mover()

def create_title_bar():

    global title_bar_main_window_label,menu_button,reload_button,back_button,back_button_title,get_pdf_button

    title_bar_main_window_label=Label(window,image=title_bar_main_window_img)
    menu_button=Button(window,image=menu_button_img,borderwidth=0,bd=0,highlightthickness=0,command=menu_mover)
    reload_button=Button(window,image=reload_button_img,borderwidth=0,bd=0,highlightthickness=0,command=reload)
    back_button=Button(window,image = back_button_img,borderwidth=0,bd=0,highlightthickness=0,command=back_button_cmd)
    back_button_title=Button(window,image = back_button_title_img,borderwidth=0,bd=0,highlightthickness=0,command=back_button_title_comm)
    get_pdf_button=Button(window,image=get_pdf_img,borderwidth=0,bd=0,highlightthickness=0,command=get_pdf)
    title_bar_main_window_label.pack()
    menu_button.place(x=10,y=10)
    get_pdf_button.place(x=100,y=10)
    back_button_title.place(x=1250,y=10)
    reload_button.place(x=1350,y=10)

def destroy_title_bar():

    menu_button.destroy()
    get_pdf_button.destroy()
    back_button.destroy()
    back_button_title.destroy()
    reload_button.destroy()
    title_bar_main_window_label.destroy()
    
    
# Creating Loading Window Elements 

loading_window_bg = Image.open(r'pics/News Scoops Loading Screen.png')
resized_loading_window_bg=loading_window_bg.resize((1280,720),Image.Resampling.LANCZOS)
loading_window_final_bg=ImageTk.PhotoImage(image=resized_loading_window_bg)
loading_window_label= Label(window,image=loading_window_final_bg)
loading_window_label.place(x=0,y=0)
loading_bar = ttk.Progressbar( window,orient= HORIZONTAL ,length=600,mode='determinate')
loading_bar.place(x=350,y=550)

def start_loading():

    for i in range(1,101):
        loading_bar['value']=i
        window.update()
        time.sleep(0.07)
    return True


loading_is_over = start_loading()

# Creating Login Screeen Elements

def email_id_textbox_info_place(e):

    global email_id_textbox_info
    email_id_textbox_info=Label(window,text='Enter Your Email Id',font=('Verdana',16),background='#242424')
    email_id_textbox_info.place(x=500,y=375,height=25)

def password_textbox_info_place(e):

    global password_textbox_info
    password_textbox_info=Label(window,text='Enter Your Password',font=('Verdana',16),background='#242424')
    password_textbox_info.place(x=500,y=515,height=25)

log_in_window_bg = Image.open(r'pics\Log In bg.png') 
resized_log_in_window_bg=log_in_window_bg.resize((w,h),Image.Resampling.LANCZOS)
log_in_window_final_bg=ImageTk.PhotoImage(image=resized_log_in_window_bg)
log_in_window_label=Label(window,image=log_in_window_final_bg,borderwidth=0)
email_id_textbox=ttk.Entry(window,width=28,font=('Verdana',25))
email_id_textbox.bind('<Enter>',email_id_textbox_info_place)
email_id_textbox.bind('<Leave>',lambda e: email_id_textbox_info.destroy())
password_textbox=ttk.Entry(window,width=28,font=('Verdana',25),show=chr(0x2022))
password_textbox.bind('<Enter>',password_textbox_info_place)
password_textbox.bind('<Leave>',lambda e: password_textbox_info.destroy())
log_in_button_bg=ImageTk.PhotoImage(file=r'pics/LOGIN BUTTON.png',)
log_in_button=Button(window,image=log_in_button_bg,borderwidth=0,bd=0,highlightthickness=0,relief=FLAT,background='#212121',command=log_in_main_window)
create_account_button_bg=ImageTk.PhotoImage(file=r'pics/Create Account Button.png')
create_account_button=Button(window,image=create_account_button_bg,borderwidth=0,bd=0,relief=FLAT, highlightthickness=0,command=create_account_navigation)


if loading_is_over:

    def do_stuff():
        window.overrideredirect(False)
        window.geometry(f'{w}x{h}+0+0')
        loading_window_label.destroy()
        loading_bar.destroy()
        log_in_window_label.place(x=0,y=0)
        email_id_textbox.place(x=500,y=400)
        password_textbox.place(x=500,y=540)
        log_in_button.place(x=600,y=625)
        create_account_button.place(x=760,y=735)

    window.after(3000,do_stuff)
    

# NEWS WINDOW #

#Menu Images

top_headlines_button_img=ImageTk.PhotoImage(file=r'pics\TOP HEADLINES BUTTON.png')
business_button_img=ImageTk.PhotoImage(file=r'pics\BUSINESS BUTTON.png')
entertainment_button_img=ImageTk.PhotoImage(file=r'pics\ENTERTAIMENT BUTTON.png')
science_button_img=ImageTk.PhotoImage(file=r'pics\SCIENCE BUTTON.png')
technology_button_img=ImageTk.PhotoImage(file=r'pics\TECHNOLOGY BUTTON.png')
sport_button_img=ImageTk.PhotoImage(file=r'pics\SPORTS BUTTON.png')
health_button_img=ImageTk.PhotoImage(file=r'pics\HEALTH BUTTON.png')
log_out_button_img=ImageTk.PhotoImage(file=r'pics\LOG OUT BUTTON.png')



# Title Bar

title_bar_main_window_img=ImageTk.PhotoImage(file=r'pics/TILTE BAR LABEL.png')
menu_button_img=ImageTk.PhotoImage(file=r'pics\MENU BUTTON.png')
reload_button_img=ImageTk.PhotoImage(file=r'pics/RELOAD.png')
back_button_img=ImageTk.PhotoImage(file=r'pics\BACK BUTTON.png')
back_button_title_img=ImageTk.PhotoImage(file=r'pics\Back Button Title.png')
get_pdf_img=ImageTk.PhotoImage(file=r'pics\GET PDF.png')

# Create Account Window

def create_account_name_info_place(e):

    global create_account_name_info
    create_account_name_info=Label(window,text='Enter Your Name',font=('Verdana',16),background='#242424')
    create_account_name_info.place(x=550,y=320,height=25)

def create_account_email_info_place(e):

    global create_account_email_info
    create_account_email_info=Label(window,text='Enter Your Email',font=('Verdana',16),background='#242424')
    create_account_email_info.place(x=550,y=410,height=25)

def create_account_password_info_place(e):

    global create_account_password_info
    create_account_password_info=Label(window,text='Enter a Strong Password within 20 characters',font=('Verdana',16),background='#242424')
    create_account_password_info.place(x=550,y=500,height=25)

def create_account_phno_info_place(e):

    global create_account_phno_info
    create_account_phno_info=Label(window,text='Enter Your 10-digit Phone Number',font=('Verdana',16),background='#242424')
    create_account_phno_info.place(x=550,y=590,height=25)


    
create_account_window_img=ImageTk.PhotoImage(file=r'pics\CREATE ACCOUNT BG.png')
create_account_window_label= Label(window,image=create_account_window_img,borderwidth=0,bd=0,highlightthickness=0)
create_account_window_create_account_button_img=ImageTk.PhotoImage(file=r'pics\CREATE ACCOUNT  BUTTON CREATE ACCOUNT WINDOW.png')
create_account_window_create_account_button=Button(window,image=create_account_window_create_account_button_img,borderwidth=0,bd=0,highlightthickness=0,command=create_account_window_create_account)
create_account_back_button_img=ImageTk.PhotoImage(file=r'pics\BACK BUTTON 2.png')
create_account_back_button=Button(window,image=create_account_back_button_img,borderwidth=0,bd=0,highlightthickness=0,command=create_account_back)
create_account_name_textbox=ttk.Entry(window,width=38,font=('Verdana',25))
create_account_name_textbox.bind('<Enter>',create_account_name_info_place)
create_account_name_textbox.bind('<Leave>',lambda e:create_account_name_info.destroy())
create_account_email_textbox=ttk.Entry(window,width=38,font=('Verdana',25))
create_account_email_textbox.bind('<Enter>',create_account_email_info_place)
create_account_email_textbox.bind('<Leave>',lambda e:create_account_email_info.destroy())
create_account_password_textbox=ttk.Entry(window,width=38,font=('Verdana',25),show=chr(0x2022))
create_account_password_textbox.bind('<Enter>',create_account_password_info_place)
create_account_password_textbox.bind('<Leave>',lambda e: create_account_password_info.destroy())
create_account_phno_textbox=ttk.Entry(window,width=38,font=('Verdana',25))
create_account_phno_textbox.bind('<Enter>',create_account_phno_info_place)
create_account_phno_textbox.bind('<Leave>',lambda e: create_account_phno_info.destroy())



window.mainloop()
