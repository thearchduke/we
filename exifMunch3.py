import os, re
from iptcinfo import IPTCInfo
import csv

csvOut = csv.writer(open('forGregg.csv', 'w'))
csvOut.writerow(['uri', 'make & model', 'year', 'description'])
i = 0
errs = 0
cars = set()


'''
THIS ROUTINE NEEDS DOCUMENTATION
Briefly, test for IPTC metadata; if so, get caption; if so, strip whitespace & stuff and 
search for car via regex, then see if it matches or not; then str.find() "Description:"
and use math to parse the whole desc thing. 

Please remember that we need to add in the rest of the (headers?) (the stuff that 
is like location and whatever and source and things that you haven't included; 
see allthedata.txt)
'''

for f in os.listdir('.'):
    try:
        for pic in os.listdir(f):
            if 'jpg' in str(pic).lower() or 'jpeg' in str(pic).lower() or 'gif' in str(pic).lower() or 'bmp' in str(pic).lower():
                i += 1
                #print f + '/' + pic
                iterPhoto = open(f + '/' + pic)
                try:
                    info = IPTCInfo(iterPhoto)
                except:
                    print "IPTC Error (not present)"
                if info:
                    try:
                        d = info.getData()['caption/abstract']
                    except:
                        print "IPTC, but no caption"
                        d = False
                    if d:
                        dStripped = ''.join(d.splitlines())
                        #print dStripped
                        i += 1
                        p = re.compile('<b>Car:</b><br>(.*?)<p>')
                        car = False
                        try:
                            car = p.match(dStripped).group(1)
                        except:
                            print "Could not determine model"
                        year = False
                        try:
                            year = int(car[0:3])
                        except:
                            year = ''
                        isDesc = dStripped.find("Description:")
                        desc = False
                        if isDesc:
                            isLoc = dStripped.find("<p><b>Location:")
                            if isLoc:
                                desc = dStripped[isDesc+20:isLoc]
                            else:
                                desc = dStripped[isDesc+20:]
                        if year and car:
                            carOut = car[5:]
                            yearOut = car[0:4]
                            csvOut.writerow([f + '/' + pic, carOut, yearOut, desc])
                            #print carOut, yearOut, desc
                        elif car:
                            carOut = car
                            csvOut.writerow([f + '/' + pic, carOut, year, desc])
                        else:
                            msg = "Unspecified error with " + pic + " (probably in the metadata)"
                            #csvOut.writerow([msg])
                iterPhoto.close()
                print i
    except OSError as e:
        print e

#csvOut.close()
print str(i) + " pictures processed, with " + str(errs) + " errors"
print len(cars)
