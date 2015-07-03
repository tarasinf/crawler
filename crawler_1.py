#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import httplib
import sys
import re
import urllib
import csv
from HTMLParser import HTMLParser


class miniHTMLParser(HTMLParser):

    viewedQueue = []
    instQueue = []
    tutorQueue = []
    linkNumber = 0

    def get_next_link(self):
        if self.instQueue == []:
            return ''
        else:
            return self.instQueue.pop(0)

    def gethtmlfile(self, site, page):
        try:
            httpconn = httplib.HTTPConnection(site)
            httpconn.request("GET", page)
            resp = httpconn.getresponse()
            resppage = resp.read()
        except:
            resppage = ""

        return resppage

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            newstr = str(attrs[0][1])
            if re.search('http', newstr) == None:
                if re.match('//', newstr) == None:
                        if re.search('mailto', newstr) == None:
                            # if ((newstr in self.tutorQueue) == False) and (re.search('matematik-', newstr) != None):
                            if ((newstr in self.tutorQueue) == False) and (newstr[1:2].isdigit() == True):
                                self.tutorQueue.append(newstr)
                                self.viewedQueue.append(newstr)
                                print "    adding tutor count: ", str(len(self.tutorQueue)), newstr
                                self.parseTutor(newstr)
                            elif (newstr in self.viewedQueue) == False:
                                self.instQueue.append(newstr)
                                self.viewedQueue.append(newstr)
                        else:
                            print "    ignoring", newstr
                else:
                    print "    ignoring", newstr
            else:
                print "    ignoring", newstr

    def parseTutor(self, url):
        print "*******************************************************************************"
        #analis
        name = '-'
        email = '-'
        phone = '-'
        city = '-'
        regions = '-'
        country = '-'
        subject = '-'
        urlPhoto = '-'

        tut = "http://" + sys.argv[1] + url
        self.linkNumber = self.linkNumber + 1
        print str(self.linkNumber) + "  url: " + tut
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
                phone_dirty = without_space[0:-5].strip()

                phone = ''
                for c in phone_dirty:
                	if c in ('0','1','2','3','4','5','6','7','8','9'):
                		phone = phone + c
                fivePos = phone.find('5')
                if fivePos >= 0:
                	phone = phone[fivePos:fivePos + 10]
                if len(phone) != 10:
                	phone = '-'

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
        writer.writerow({'full-name': name, 'email': email, 'phone-number': phone, 'city': city, 'regions': regions, 'country': country, 'subject': subject, 'url-of-profile': tut, 'url-of-photo': urlPhoto})


def main():

    if sys.argv[1] == '':
        print "usage is ./minispider.py site link"
        sys.exit(2)

    mySpider = miniHTMLParser()

    link = "/"
    exceptionCount = 0
    global csvfile
    csvfile = open('tutors.csv', 'w')
    fieldnames = ['full-name', 'email', 'phone-number', 'city', 'regions', 'country', 'subject', 'url-of-profile', 'url-of-photo']
    global writer
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    while link != '':
        # if len(mySpider.tutorQueue) >= 200:
        #     print "count ref = " + str(len(mySpider.tutorQueue))
        #     break

        print "Checking link out ", link 

        try:
            retfile = mySpider.gethtmlfile(sys.argv[1], link)
            mySpider.feed(retfile)
        except UnicodeDecodeError:
            exceptionCount = exceptionCount + 1
            print "!!!!!!!!!!!!!!!!!!!!!! exception in link " + str(exceptionCount) + " " + link
        link = mySpider.get_next_link()

    csvfile.close()
    mySpider.close()

    print "\ndone\n"
    print "exceptionCount: " + str(exceptionCount)

if __name__ == "__main__":
    main()
