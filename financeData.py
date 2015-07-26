import sys
import gtk
import appindicator
import imaplib
import re
import pandas.io.data as web
from datetime import datetime
import matplotlib.pyplot as plt    

PING_FREQUENCY = 10 # seconds

class CheckGMail:
    def __init__(self):
        self.ind = appindicator.Indicator("new-gmail-indicator",
                                           "indicator-messages",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("/home/spedmonkey/Downloads/Visualpharm-Must-Have-Stock-Index-Up.ico")
        self.ind.set_attention_icon("/home/spedmonkey/Downloads/Visualpharm-Must-Have-Stock-Index-Down.ico")
        self.ind.set_label("MSCI")
        self.menu_setup()
        self.ind.set_menu(self.menu)

        self.asdf = appindicator.Indicator("asdf",
                                           "asdf",
                                           appindicator.CATEGORY_APPLICATION_STATUS)
        self.asdf.set_status(appindicator.STATUS_ACTIVE)
        self.asdf.set_attention_icon("/home/spedmonkey/Downloads/Visualpharm-Must-Have-Stock-Index-Up.ico")
        self.asdf.set_attention_icon("/home/spedmonkey/Downloads/Visualpharm-Must-Have-Stock-Index-Down.ico")
        self.asdf.set_label("ASX300")
        self.menu_setup()
        self.asdf.set_menu(self.menu)

    def graphFunc(self, widget):
        end = datetime.now()
        start = datetime(end.year - 2, end.month, end.day)
        asx = web.DataReader('VAS.AX', 'yahoo', start, end)
        msci=web.DataReader("MSCI", 'google', start, end)
        asx['msci']=msci['Close']
        asx['asx300']=asx['Close']
        plots = asx[['asx300', 'msci']].plot(subplots=False, figsize=(10, 10) )
        plt.plot(msci['Close'], label = 'msci')
        plt.show()        

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.quit_item = gtk.MenuItem("Quit")
        self.graph_item = gtk.MenuItem("Graph")
        self.quit_item.connect("activate", self.quit)
        self.graph_item.connect("activate", self.graphFunc)
        self.quit_item.show()
        self.graph_item.show()
        self.menu.append(self.quit_item)
        self.menu.append(self.graph_item)

    def main(self):
        self.check_mail()
        gtk.timeout_add(PING_FREQUENCY * 10, self.check_mail)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

    def check_mail(self):
        messages, unread = self.gmail_checker('spedcr@gmail.com','0xy47abTQ#')
        if unread > 1607:
            self.ind.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.ind.set_status(appindicator.STATUS_ACTIVE)
        return True

    def gmail_checker(self, username, password):
        i = imaplib.IMAP4_SSL('imap.gmail.com')
        try:
            i.login(username, password)
            x, y = i.status('INBOX', '(MESSAGES UNSEEN)')
            messages = int(re.search('MESSAGES\s+(\d+)', y[0]).group(1))
            unseen = int(re.search('UNSEEN\s+(\d+)', y[0]).group(1))
            return (messages, unseen)
        except:
            return False, 0

if __name__ == "__main__":
    indicator = CheckGMail()
    indicator.main()