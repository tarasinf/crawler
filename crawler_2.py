#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import httplib
import sys
import re
import urllib
import csv
from HTMLParser import HTMLParser


class CustomParser():

    viewedQueue = []
    tutorCount = 0
    exceptionCount = 0

    def validLink(self, link):
        if link != '':
            if re.match('/', link) != None:
                if re.search('http', link) == None:
                    if re.match('//', link) == None:
                        if re.search('mailto', link) == None:
                            if (link in self.viewedQueue) == False:

                                return True
        return False

    def checkTutor(self, link):
        if link[1:2].isdigit() == True:
            print "link is Tutor: " + link
            return True
        return False

    def parsePage(self, link):
        print " link    : " + link
        if self.checkTutor(link) == True:
            self.parseTutor(link)
            return

        link = "http://" + sys.argv[1] + link
        try:
            lines = urllib.urlopen(link).readlines()
        except IOError:
            self.exceptionCount = self.exceptionCount + 1
            return
                
        for i in range(len(lines)):
            line = lines[i] 
            if '<a ' in line:
                begin = line.find('href=') + 6 
                end = line.find('\"',begin)
                nextLink = ''
                if begin >= 0 and end >= 0:
                    nextLink = line[begin:end]

                if self.validLink(nextLink) == True:
                    self.viewedQueue.append(nextLink)
                    self.parsePage(nextLink)

    def parseTutor(self, url):
        print ""
        print "*******************************************************************************"
        name = '-'
        email = '-'
        phone = '-'
        city = '-'
        regions = '-'
        country = '-'
        subject = '-'
        urlPhoto = '-'

        tut = "http://" + sys.argv[1] + url
        self.tutorCount = self.tutorCount + 1
        print str(self.tutorCount) + "  url: " + tut
        infile = urllib.urlopen(tut)
        lines = infile.readlines()
        for i in range(len(lines)):
            line = lines[i] 
            if 'Ad/Soyad' in line:
                without_space = lines[i+3].strip()
                name = without_space[0:-5].strip()
                print " name    : " + name

            if 'E-mail' in line:
                without_space = lines[i+3].strip()
                email = without_space[21:-20].strip()
                print " email   : " + email

            if 'Telefon' in line:
                without_space = lines[i+3].strip()
                phone = without_space[0:-5].strip()
                # phone  = re.sub(' ', '', phone)
                # phone  = re.sub('-', '', phone)
                # if phone[0] == '0':
                #     phone = phone[1:]
                # if phone[0] == '5' and len(phone) >= 10:
                #     phone = phone[:10]
                # else:
                #     phone = '-'
                print " phone   : " + phone
                
            if 'Ders verilebilece' in line:
                without_space = lines[i+3].strip()
                location = without_space[0:-5].strip()
                pos = location.rfind(",")
                if pos >= 0:
                    city = location[pos+1:].capitalize()
                    regions = location[0:pos].lower()
                print " city    : " + city
                print " regions : " + regions

                country = "Turkey"
                print " country : " + country                

                subject = "Mathematics"
                print " subject : " + subject

            if 'retmen bilgiler' in line:
                without_space = lines[i+6].strip()
                urlPhoto = without_space[10:-5].strip()
                urlPhoto = urlPhoto[0:-2].strip()
                if 'nophoto' in urlPhoto:
                    urlPhoto = '-'
                print " urlPhoto: " + urlPhoto
        #Write to file
        print "*******************************************************************************"
        print ""
        writer.writerow({'full-name': name, 'email': email, 'phone-number': phone, 'city': city, 'regions': regions, 'country': country, 'subject': subject, 'url-of-profile': tut, 'url-of-photo': urlPhoto})

def main():

    if sys.argv[1] == '':
        print "usage is ./minispider.py site link"
        sys.exit(2)

    global csvfile
    csvfile = open('tutors.csv', 'w')
    fieldnames = ['full-name', 'email', 'phone-number', 'city', 'regions', 'country', 'subject', 'url-of-profile', 'url-of-photo']
    global writer
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()

    spider = CustomParser()
    link = "/"
    spider.viewedQueue.append(link)
    spider.parsePage(link)

    csvfile.close()


    print "//////////////////////////////////"
    print "exceptionCount: " + str(spider.exceptionCount)
    print spider.viewedQueue
    print len(spider.viewedQueue)
    print "\ndone\n"


if __name__ == "__main__":
    main()
