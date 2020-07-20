from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from icalendar import Calendar, Event, vDatetime
from datetime import datetime
import pytz
from pytz import timezone
import socket


# Fill in your details here to be posted to the login form.
chrome_driver = '/Users/alexrasla/Downloads/chromedriver'
url = 'https://my.sa.ucsb.edu/gold/Login.aspx'

browser = webdriver.Chrome(chrome_driver)
browser.get(url)

username = browser.find_element_by_name('ctl00$pageContent$userNameText')
password = browser.find_element_by_name('ctl00$pageContent$passwordText')

username.send_keys('USER')
password.send_keys('PASS')
password.send_keys(Keys.RETURN)

confirm = browser.find_element_by_name('ctl00$pageContent$confirm')
confirm.send_keys(Keys.RETURN)

my_schedule = 'https://my.sa.ucsb.edu/gold/StudentSchedule.aspx'
browser.get(my_schedule)

browser.find_element_by_xpath('/html/body/div[1]/form/section/div[2]/main/div[1]/div[1]/select/option[3]').click() #testing on winter quarter

my_schedule_weekly = 'https://my.sa.ucsb.edu/gold/WeeklyStudentSchedule.aspx'
browser.get(my_schedule_weekly)

classes = []
calendar = Calendar()
calendar.add('prodid', '-//My calendar product//mxm.dk//')
calendar.add('version', '2.0')

for class_item in browser.find_elements_by_xpath('//*[@id="pageContent_classSchedule"]/table/tbody/tr/td/span'):
    event = Event()
    #need to get rid of null event
    course = class_item.text.splitlines()
    print(course)
    for index, element in enumerate(course):
        day = ""
        if index == 0:
            event.add('summary', element)
        if index == 1:
            event.add('location', element)
        if index == 2:
            times = element.split('-')
            start_time = times[0].split(':')
            end_time = times[1].split(':')
            start_t = 0
            end_t = 0
            if(int(start_time[0]) < 12):
                start_t = int(start_time[0]) + 12
                end_t = int(end_time[0]) + 12
            else:
                start_t = int(start_time[0])
                end_t = int(end_time[0])

            date = input("Start date? ").split('/')
            s_time = datetime(int(date[0]), int(date[1]), int(date[2]), start_t, int(start_time[1]), tzinfo=timezone('US/Pacific'))
            e_time = datetime(int(date[0]), int(date[1]), int(date[2]), end_t, int(end_time[1]), tzinfo=timezone('US/Pacific'))

            event.add('dtstart', vDatetime(s_time))
            event.add('dtend', vDatetime(e_time))

    now = vDatetime(datetime.now())
    uid = str(socket.gethostbyname(socket.gethostname())) +str('@') + str(datetime.now())
    event.add('uid', uid)
    event.add('dtstamp', now)
    event.add('rrule', {'freq': 'weekly', 'count': 10})
    calendar.add_component(event)

ical_file = open('course_schedule.ics', 'wb')
ical_file.write(calendar.to_ical())
ical_file.close()