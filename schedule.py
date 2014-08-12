#!/usr/bin/env python

import sys  # DEBUG

import powerapi


class Schedule(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.ps = powerapi.core('https://powerschool.ramonausd.net/')

    def auth(self):
        try:
            self.user = self.ps.auth(username, password)
        except Exception as err:
            print "Whoops! Something went wrong with PowerAPI:", err
            sys.exit()

    def courses(self):
        self.return_list = []
        courses = self.user.getCourses()
        for course in courses:
            period = course.getPeriod()
            course_raw = course.getName()
            course_name = str(course_raw.replace('&amp;', '&'))
            teacher_raw = course.getTeacher()['name']
            teacher_name = teacher_raw[:teacher_raw.find('</a>')]
            teacher_room = teacher_raw[teacher_raw.find('Rm:'):teacher_raw.find('</td>')]

            self.return_list.append(
                {'period': period, 'name': course_name, 'teacher': {'name': teacher_name, 'room': teacher_room}})

        return self.return_list


if __name__ == '__main__':
    username = str(raw_input('Username: '))
    password = str(raw_input('Password: '))

    my_powerschool = Schedule(username, password)
    my_powerschool.auth()

    my_courses = my_powerschool.courses()
    for course in my_courses:
        period = course['period']
        course_name = course['name']
        teacher_name = course['teacher']['name']
        teacher_room = course['teacher']['room']

        print("%s - %s\n\t\t%s (%s)" % (period, course_name, teacher_name, teacher_room))