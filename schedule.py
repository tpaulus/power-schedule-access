#!/usr/bin/env python

import sys

import powerapi


class Schedule(object):
    def __init__(self, username, password, url):
        """
        Schedule fetches the users schedule from a Powerschool server regardless if the web portal is active as it uses
        the PowerAPI.

        :param username: Username used to login to PowerSchool
        :type username: str
        :param password: Password for User
        :type password: str
        :param url: The Web URL used to access the student portal of Powerschool
        :type url: str
        :return: None
        """
        self.username = username
        self.password = password

        self.user = None
        self.ps = powerapi.core(url)

    def auth(self):
        """
        Authenticate the user whose credentials were used to instantiate the class.

        :return: None
        """
        try:
            self.user = self.ps.auth(self.username, self.password)
        except Exception as err:
            print "Whoops! Something went wrong with PowerAPI:", err
            sys.exit()

    def courses(self):
        """
        Fetches and returns the authenticated users courses.
        :return: A list of Courses, each course has a dictionary of elements: Name, Period and Teacher Data
                Teacher Data consists of the teacher's Name and Room.
        """
        if self.user is None:
            # Make sure that the user is logged on before trying to access data
            self.auth()

        return_list = []
        all_courses = self.user.getCourses()
        for c in all_courses:
            period = c.getPeriod()
            name = str(c.getName()).replace('&amp;', '&')
            teacher_raw = c.getTeacher()['name']
            teacher_data = {'name': teacher_raw[:teacher_raw.find('</a>')],
                            'room': teacher_raw[teacher_raw.find('Rm:'):teacher_raw.find('</td>')]}

            return_list.append(
                {'period': period, 'name': name, 'teacher': teacher_data})

        return return_list


if __name__ == '__main__':
    power_username = str(raw_input('Username: '))
    power_password = str(raw_input('Password: '))
    power_url = 'https://powerschool.ramonausd.net/'

    my_powerschool = Schedule(power_username, power_password, power_url)
    my_powerschool.auth()

    my_courses = my_powerschool.courses()
    for course in my_courses:
        course_period = course['period']
        course_name = course['name']
        teacher_name = course['teacher']['name']
        teacher_room = course['teacher']['room']

        print("%s - %s\n\t\t%s (%s)" % (course_period, course_name, teacher_name, teacher_room))