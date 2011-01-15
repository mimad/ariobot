# coding: utf-8
##   Copyright (C) 2010-2011 Amin Oruji (aminpy@gmail.com)
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as published by
##   the Free Software Foundation; either version 2, or (at your option)
##   any later version.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.

import socket
import foshes
from xgoogle.translate import Translator
from time import localtime
from time import strftime
from calverter import Calverter
from django.utils.encoding import smart_str

class Gholam(object):
    
    def __init__(self, username, channel):
        self.username = smart_str(username)
        self.channel = smart_str(channel)
        self.pc = 'PRIVMSG ' + self.channel + ' :'
        self.network = "irc.freenode.net"
        self.port = 6667
        self.zaman = ""
        self.whoBot = ""
        self.isFosh = False
        self.connect()


    def connect(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((self.network, self.port))
        self.data = self.irc.recv(4096)
        self.irc.send("nick " + self.username + "\r\n")
        self.irc.send("user " + self.username + " " + self.username + " " + self.username + " :Python IRC\r\n")
        self.irc.send("join " + self.channel + "\r\n")
        
    
    def listen(self):
        counter = 1
        while True:
            data = self.irc.recv(4096)
            if data:
                print str(counter) + ") " + repr(data) + "\n"
                
                if data.find("PING") != -1:
                    pinger = data.split()[1]
                    self.irc.send("PONG " + pinger + "\r\n")
                    
                
                if data.find(":" + self.username + "!~" + self.username) != -1 and data.find("JOIN :" + self.channel) != -1:
                    zaman = strftime("%H:%M:%S | %A, %Y/%B/%d", localtime())
            
                if data.find(":la_fen!~la_fen@") != -1:
                    data = data[data.index("PRIVMSG " + self.username + " :") + 16:]
                    self.irc.send(self.pc + self.whoBot + ", " + data + "\r\n")
            
                elif data.find(self.pc) != -1:
                    lod = data.split("!")
                    who = lod[0]
                    who = who[1:]
                    pm = self.pc + who + ', '
            
            # -------------- help
            
                    if data.find(':!help') != -1:
                        if data.find(self.username + "!") == -1:
                            self.irc.send(pm + "https://bitbucket.org/aminpy/gholam/issue/1/gholam-commands\r\n")
            
            # ------------- khuruj
            
                    elif data.find(":!birun") != -1:
                        self.irc.send(self.pc + "chashm :(\r\n")
                        self.irc.send("QUIT\r\n")
            
            # ---------------- about
            
                    elif data.find(":!about") != -1:
                        self.irc.send(pm + "My name is " + self.username + ", I was born in 28 December 2010 and I\'m written in python.\r\n")
                            
            # --------------- time
                            
                    elif data.find(":!time") != -1:
                        self.irc.send(pm + strftime("%H:%M:%S", localtime()) + "\r\n")
                    
                    elif data.find(":!when") != -1:
                        self.irc.send(pm + zaman + "\r\n")
                        
                    elif data.find(":!date") != -1:
                        tagh = strftime("%Y/%m/%d", localtime()).split("/")
                        taghvim = Calverter().gregorian_to_iranian(int(tagh[0]), int(tagh[1]), int(tagh[2]))
                        year = taghvim[0]
                        month = taghvim[1]
                        day = taghvim[2]
                        wikDay = taghvim[3]
                        self.irc.send(pm + strftime("%a, %Y/%b/%d", localtime()) + " | " + wikDay + " " + day + " " + month + " " + year + "\r\n")
                        
            # ---------- dot commands
            
                    elif data.find(':.') != -1:
                        lod = data.split(":")
                        who = lod[1].split("!")[0]
                        lang = lod[2].split(" ")[0]
                        ebarat = ' '.join(lod[2].split(" ")[1: ])
                        
                        if ebarat.endswith("\r\n"):
                            ebarat = ebarat[:-2]
                            
                        try:
            
            #<GoogleSearch>
                            if data.find(":.web ") != -1:
                                url = "http://www.google.com/search?q=" + ebarat
                                self.irc.send(pm + url.replace(" ", "+") + "\r\n")
                                
                            elif data.find(":.img") != -1:
                                url = "http://www.google.com/images?q=" + ebarat
                                self.irc.send(pm + url.replace(" ", "+") + "\r\n")
                                
                            elif data.find(":.vid") != -1:
                                url = "http://www.google.com/search?q=" + ebarat + "&tbs=vid:1"
                                self.irc.send(pm + url.replace(" ", "+") + "\r\n")
            #</GoogleSearch>
            
            #<ContactWithRobot>
            
                            elif data.find(":.w") != -1:
                                self.irc.send("PRIVMSG la_fen :.w " + ebarat + "\r\n")
                                self.whoBot = who
            
                            elif data.find(":.dict") != -1:
                                self.irc.send("PRIVMSG la_fen :.dict " + ebarat + "\r\n")
                                self.whoBot = who
                                
            #</ContactWithRobot>
    
            #<Translate>
                            else:
                                lt = lang[1:3]
                                lf = lang[-2:]
                                matn = smart_str(Translator().translate(ebarat, lf, lt))
                                self.irc.send(str(pm) + matn + str("\r\n"))
            #</Translate>
                                
                        except Exception, e:
                            print e
                    
                # <5hit>
                                    
                if self.isFosh:
                    for s in foshes.foshes:
                        if data.find(s):
                            if foshes.isFosh(s, data):
                                try:
                                    lod = data.split(":")
                                    who = lod[1].split("!")[0]
                                    self.irc.send(pm + "kheyli bi adabi!!!\r\n")
                                except Exception, e:
                                    print e
                                break
                            
                if self.channel == "#5hit" and data.find("fuck up") != -1:
                    self.isFosh = True
                    
                # </5hit>

                counter += 1

            else:
                self.connect()
