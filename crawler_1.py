#!/usr/bin/env python

import httplib
import sys
import re
import urllib
import csv
from HTMLParser import HTMLParser


class miniHTMLParser( HTMLParser ):

    viewedQueue = []
    instQueue = []
    tutorQueue = []

    def get_next_link( self ):
        if self.instQueue == []:
            return ''
        else:
            return self.instQueue.pop(0)

    def gethtmlfile( self, site, page ):
        try:
            httpconn = httplib.HTTPConnection(site)
            httpconn.request("GET", page)
            resp = httpconn.getresponse()
            resppage = resp.read()
        except:
            resppage = ""

        return resppage

    def handle_starttag( self, tag, attrs ):
        if tag == 'a':
            newstr = str(attrs[0][1])
            if re.search('http', newstr) == None:
                if re.search('mailto', newstr) == None:
                    if ( (newstr in self.tutorQueue) == False ) and ( re.search('matematik-', newstr) != None ):
                        self.tutorQueue.append( newstr )
                        print "    adding tutor count: ",str(len(self.tutorQueue)), newstr
                    elif (newstr in self.viewedQueue) == False:
                        self.instQueue.append( newstr )
                        self.viewedQueue.append( newstr )
                else:
                    print "    ignoring", newstr
            else:
                print "    ignoring", newstr

def main():

    if sys.argv[1] == '':
        print "usage is ./minispider.py site link"
        sys.exit(2)

    mySpider = miniHTMLParser()

    link = "/"
    while link != '':
        if len(mySpider.tutorQueue) >= 20:
            print "count ref = " + str(len(mySpider.tutorQueue))
            break

        print "\nChecking link out ", link 

        retfile = mySpider.gethtmlfile( sys.argv[1], link )
        mySpider.feed(retfile)
        link = mySpider.get_next_link()

    print "*******************************************************************************"
    with open('tutors.csv', 'w') as csvfile:
        fieldnames = ['full-name', 'email', 'phone-number', 'city', 'country', 'subject', 'url-of-profile', 'url-of-photo']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        name = ''
        email = ''
        phone = ''
        city = ''
        country = ''
        subject = ''
        urlPhoto = ''

        for tut in mySpider.tutorQueue:
            #analis
            print "url: " + tut
            infile = urllib.urlopen("http://" + sys.argv[1] + tut)
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
                    print " phone   : " + phone
                    
                if 'Ders verilebilece' in line:
                    without_space = lines[i+3].strip()
                    city = without_space[0:-5].strip()
                    print " city    : " + city

                    country = "Turkey"
                    print " country : " + country                

                    subject = "Mathematics"
                    print " subject : " + subject

                if 'retmen bilgiler' in line:
                    without_space = lines[i+6].strip()
                    urlPhoto = without_space[10:-5].strip()
                    urlPhoto = urlPhoto[0:-2].strip()
                    print " urlPhoto: " + urlPhoto
            #Write to file
            print ""
            writer.writerow({'full-name': name, 'email': email, 'phone-number': phone, 'city': city, 'country': country, 'subject': subject, 'url-of-profile': tut, 'url-of-photo': urlPhoto})

    mySpider.close()

    print "\ndone\n"

if __name__ == "__main__":
    main()
