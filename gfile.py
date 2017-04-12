"""
Module to interact with file on google drive
"""

__Author__ = 'Abhijit Ghongade'
__Version__ = 1.0

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
from StatusLogger import LOGFILE_PATH
from StatusLogger import SCRIPT_DIR
CLIENT_SECRETS_JSON = 'client_secrets.json'

class GFile():
	
	def __init__(self):
		self.logfile = LOGFILE_PATH
		self.drive = self._authenticate()
		
	def _authenticate(self):
		"""
		Authenticate with google drive
		"""
		# Check if client_secret file is present for authentication
		self._check_secrets_file()
		return GoogleAuth(self)

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

	def updateFileContent(self, gfile, contentStr="", source_file=None):
		"""
		Updates file contents on google drive
		:param filename: Name of the file on google drive
		:return: None
		"""
		gfileObj = self._get_file(gfile)
		if source_file:
			gfileObj.SetContentFile(source_file)
		else:
			gfileObj.SetContentString(contentStr)
		# Upload the file
		gfileObj.Upload()

	
