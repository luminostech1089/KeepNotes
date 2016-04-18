import os,sys
from cmd import Cmd


filename = 'Status.txt'
script_dir = os.path.dirname(os.path.realpath(__file__))
maxchar = 500
maxline_len = 100
data_dict = {} # dictionary to store input data
fileobj = None
statusfile = os.path.join(script_dir, filename)


class StatusLogger(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.data_dict = {}
        try:
            self.fileobj =  open(statusfile, "a+")
        except:
            print('Unable to open status log file [{}]'.format(statusfile))
            self._do_exitapp()

    def do_add(self, line):
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
        for key, data in self.data_dict.iteritems():
            print("{} : {}".format(key, data))

    def update_data(self):
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
        for index in self.data_dict:
            self.fileobj.write(self.data_dict[index])

    def _is_same_day_commit(self):
        """
        Function to verify if commit is of same date or new date.
        :return:  True if same date commit
        """


    def do_exit(self, line):
        return True


if __name__ == "__main__":
    StatusLogger().cmdloop()

