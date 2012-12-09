#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  senza nome.py
#  
#  Copyright 2012 thezero <silvethebest@yahoo.it>
#
#  Some part of code is
#  Copyright © 2009  Fotis Tsamis <ftsamis at gmail dot com>
#  (From CPU-G Beta)
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os, sys, requests, json, string
from pprint import pprint
try:
    import pygtk, gtk, gtk.glade, gobject, webkit
    pygtk.require("2.0")
except:
    print 'You need to have PyGTK 2.10.0, GTK.Glade and GTK+ 2.10.0 or higher  \
           installed in your system in order to run MangaEden Downloader.'
    sys.exit(1)
    
    
from threading import Thread
    
class CPUG:
    """Description"""
    
    def __init__(self):
        self.gladefile = "mangaeden.glade"
        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.gladefile)
        
        dic = { 
                "on_close_clicked" : self.kill,
                "on_mainwindow_destroy" : self.kill,
                "on_search_clicked" : self.search,
        }
        self.wTree.connect_signals(dic) 

        self.webview = webkit.WebView() 
        self.webview.show()
        self.vbox = gtk.VBox(False, 0)
        self.vbox.set_size_request(70, 190)
        self.vbox.add(self.webview)
        self.wTree.get_object("hbox1").add(self.vbox)
    
    def search(self, widget):
		# Prelevo il link del manga
        alfa = self.wTree.get_object("mlink").get_text()
        print alfa
        # Se inizia per http:// ok se no lo aggiungo
        try:
            alfa.index("://")
        except:
            alfa = "http://"+alfa
        # Splitto la stringa per ottenere le mie info
        arr = alfa.split('/')
        self.nick = arr[4]
        lang = arr[3]
        print self.nick
        # Rilevo la lingua del manga
        if lang == "it-manga":
            lang = 1
        elif lang == "en-manga":
            lang = 0
        t = Thread(target=CPUG.download, args=(self,lang,))
        t.start()
        print "Start"
      
    def download(self,lingua):
	    # Scarico la lista manga API
		url = r'http://www.mangaeden.com/api/list/%d/' % lingua
		g = requests.get(url)
		print url
		a = json.loads(g.text)
		# Scorro l'array in cerca del manga
		for row in a["manga"]:
			if row["a"] == self.nick:
				title = row["t"]
				manga_id = row["i"]
				image = row["im"]		
		# Setto l'immagine e la visualizzo
		self.webview.load_uri('http://cdn.mangaeden.com/mangasimg/%s' % image)  
		self.vbox.show()  
		# Imposto il nome manga
		self.wTree.get_object("mname").set_text(title)
		# Prelevo altre info
		g = requests.get(r'http://www.mangaeden.com/api/manga/%s/' % manga_id)
		a = json.loads(g.text)
		categories=""
		for cat in a["categories"]:
			categories += cat
			categories += " "
		if lingua == 1:
			lingua = "Italiano"
		else:
			lingua = "Inglese"
		self.wTree.get_object("mdesc").set_text(a["description"])
		self.wTree.get_object("mcat").set_text(categories)
		self.wTree.get_object("mlang").set_text(lingua)
		self.wTree.get_object("mcapn").set_text("%d" % a["chapters"][0][0])  
           
    def kill(self, widget):
        print "Quit"
        sys.exit(0)
        

if __name__ == '__main__':
    CPUG()
    gtk.main()
    
