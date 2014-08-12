#!/usr/bin/env python

import sys  # DEBUG

import powerapi
import re

ps = powerapi.core('https://powerschool.ramonausd.net/')

username = str(raw_input('Username: '))
password = str(raw_input('Password: '))

try:
    user = ps.auth(username, password)
except Exception as err:
    print "Whoops! Something went wrong with PowerAPI:", err
    sys.exit()

courses = user.getCourses()
for course in courses:
    period = course.getPeriod()
    course_raw = course.getName()
    course_name = str(course_raw.replace('&amp;', '&'))
    teacher_raw = course.getTeacher()['name']
    teacher_name = teacher_raw[:teacher_raw.find('</a>')]
    teacher_room = teacher_raw[teacher_raw.find('Rm:'):teacher_raw.find('</td>')]
    print("%s - %s\n\t\t%s (%s)" % (period, course_name, teacher_name, teacher_room))