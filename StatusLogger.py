__Author__ = 'Abhijit Ghongade'
__Version__ = 1.0

import os
import sys
from cmd import Cmd
from gwb import Workbook
import datetime
import pickle


LOGFILE_NAME = 'Status.txt'
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
MAXLINE_LEN = 100
fileobj = None
LOGFILE_PATH = os.path.join(SCRIPT_DIR, LOGFILE_NAME)
CONFIGFILE_PATH = os.path.join(SCRIPT_DIR, 'Config.zip')
CONFIG_DATA = {'lastdate': '',
               'alldates': []}


def cur_date():
    date_format = '%d-%m-%Y'
    now = datetime.datetime.now()
    return now.strftime(date_format)

class StatusLogger(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.data_dict = {}
        try:
            self.fileobj = open(LOGFILE_PATH, "a+")
            self.configdata = self._getconfigdata() or CONFIG_DATA
        except:
            print('Unable to open status log file [{}]'.format(LOGFILE_PATH))
            self._do_exitapp()

    def do_add(self, line):
        """
        Method to add new data.
        """
        print('Enter your data')
        count = 0
        data = raw_input('{} =>'.format(count))
        while(len(data) > 0):
            self.data_dict[str(count)] = data
            count += 1
            data = raw_input('{} =>'.format(count))

    def _do_exitapp(self):
        return True

    def do_view(self, line):
        """
        Method to view data added.
        """
        for key, data in self.data_dict.iteritems():
            print("{} : {}".format(key, data))

    def update_data(self):
        """
        Method to update the data added.
        """
        self.do_view()
        print('\n Enter index of record to update')
        index = raw_input('>')
        if index in self.data_dict:
            print("Enter new data")
            new_data = raw_input('>')
            self.data_dict[index] = new_data
        else:
            print('invalid index selected')

    def do_help(self, line):
        """
        Method to display help message.
        """
        print('Below commands are supported')
        help_content = """
        add: Add data to status logger
        view: View entered data
        update: Update entered data
        commit: Write data to status log file
        exit: Eit from log file
        """
        print(help_content)

    def do_commit(self, line):
        """
        Method to write data to log file.
        """
        header_str = '*'*50 + '\n' + 'date \n' + '*'*50 + '\n\n'
        curdate = cur_date()
        if not self._is_same_day_commit():
            date = ' Date: ' + curdate
            self.fileobj.write(header_str.replace('date', date))
            self.configdata['lastdate'] = curdate
            self.configdata['alldates'].append(curdate)
            print('debug: alldates ', self.configdata['alldates'])
            # Update conf file - To Do: Move this part at exit point
            pickle.dump(self.configdata, open(CONFIGFILE_PATH, "w"))
        for index in self.data_dict:
            self.fileobj.write("=> {} \n".format(self.data_dict[index]))

    def _is_same_day_commit(self):
        """
        Function to verify if commit is of same date or new date.
        :return:  True if same date commit
        """
        if self.configdata:
            lastrec_date = self.configdata['lastdate']
            curdate = cur_date()
            return lastrec_date == curdate
        else:
            return False

    def _getconfigdata(self):
        """
        Method to retrieve config data
        """
        if os.path.exists(CONFIGFILE_PATH):
            with open(CONFIGFILE_PATH) as fh:
                return pickle.load(fh)
        else:
            return None

    def do_exit(self, line):
        return True

if __name__ == "__main__":
    StatusLogger().cmdloop()

