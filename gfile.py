"""
Module to interact with file on google drive
Refs: 
1) https://googledrive.github.io/PyDrive/docs/build/html/filemanagement.html#upload-a-new-file
2) https://developers.google.com/identity/protocols/OAuth2WebServer
3) https://stackoverflow.com/questions/31092397/how-to-use-google-drive-api-without-web-browser
"""

__Author__ = 'Abhijit Ghongade'
__Version__ = 1.0

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
from constants import LOGFILE_PATH
from constants import SCRIPT_DIR
from constants import CLIENT_SECRETS_JSON

class GFile():
    def __init__(self):
        self.logfile = LOGFILE_PATH
        gauth = self._authenticate()
        self.drive = GoogleDrive(gauth)

    def _authenticate(self):
        """
        Authenticate with google drive
        """
        # Check if client_secret file is present for authentication
        self._check_secrets_file()
        return GoogleAuth()

    def _check_secrets_file(self):
        """
        Check if client_secrets.json file is present or not
        """
        if not os.path.exists(os.path.join(SCRIPT_DIR, CLIENT_SECRETS_JSON)):
            raise ValueError("{} file not found at path {}".format(CLIENT_SECRETS_JSON, SCRIPT_DIR))

    def _get_file(self, filename):
        """
        Returns file object of 'filename' on google drive
        :param filename: Name of the file on google drive
        :return: GoogleDriveFile object
        """
        files_list = [gfile for gfile in self.drive.ListFile().GetList() if gfile['title'] == filename]
        if len(files_list) == 0:
            raise ValueError("File {} not found on google drive".format(filename))
        return files_list[0]

    def createFile(self, filename):
        """
        Returns file object of 'filename' on google drive
        :param filename: Name of the file to be created on google drive
        :return: GoogleDriveFile object
        """
        gfile = self.drive.CreateFile({'title': filename})
        gfile.Upload() # Upload the file
        return gfile

    def updateFileContent(self, gfile, contentStr="", source_file=None):
        """
        Updates file contents on google drive
        :param filename: Name of the file on google drive
        :return: None
        """
        # Create new file if not exists
        try:
            gfileObj = self._get_file(gfile)
        except ValueError:
            gfileObj = self.createFile(gfile)
        if source_file:
            gfileObj.SetContentFile(source_file)
        else:
            print "contentStr:", contentStr
            gfileObj.SetContentString(contentStr)
        # Upload the file
        gfileObj.Upload()

if __name__ == "__main__":
    gfile = GFile()
