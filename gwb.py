__Author__ = 'Abhijit Ghongade'
__Version__ = 1.0

import collections
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials

class Workbook(object):
    """
    This contains functions to process parsed excel sheet data.
    It is an extension of gspread module.
    """

    def __init__(self, jsonfile, spreadsheet):
        try:
            json_key = json.load(open(jsonfile))
        except Exception as Ex:
            sys.exit(Ex)
        try:
            print ("Authenticating with google...")
            scope = ['https://spreadsheets.google.com/feeds']
            credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
            client = gspread.authorize(credentials)
            client.login()
            print("Authentication successful")
        except Exception as Ex:
            print("Error occurred while authentication with google.")
            raise Ex
        print("Opening spreadsheet [{}]".format(spreadsheet))
        # wb- workbook
        try:
            self.wb = client.open(spreadsheet)
        except Exception as Ex:
            print('Error occurred while opening spreadsheet [{}]. Please check spreadsheet name'.format(spreadsheet))
            sys.exit(Ex)
        print("Got access to spreadsheet. Fetching data...")
        self.sheet = self.identifySheet()
        # Get all the sheet values - list of list
        self.sheet_matrix = self.sheet.get_all_values()
        self.max_row = len(self.sheet_matrix)
        self.max_col = len(self.sheet_matrix[0])
        self.first_row = 0
        self.first_col = 0

    def __sync(self):
        '''
        Update some attributes when sheets is updated
        '''
        self.sheet_matrix = self.sheet.get_all_values()
        self.max_row = len(self.sheet_matrix)
        self.max_col = len(self.sheet_matrix[0])
        self.first_row = 0
        self.first_col = 0

    def identifySheet(self):
        """
        Logic for identification of desired sheet.
        Raise "Desired Sheet not found" exception if sheet not found.
        """
        # To Do - Need to verify sheet name here
        return self.wb.worksheets()[0]

    def getWorksheets(self):
        return self.wb.worksheets()

    def updateSheet(self, sheet):
        """
        Update sheet attribute with new sheet object
        """
        self.sheet = self.wb.worksheet(sheet)
        self.__sync()
        print('Worksheet updated. Using worksheet [{}]'.format(self.sheet.title))

    def searchStringInRow(self, pattern, row, count=1, compl_str=0, case_sesitive=0):
        """
        Search for pattern or string in specified row.
        Specify count for number of occurrence to search. Default value is 1.
        Returns dictionary having key as 'matched string/pattern' and value
        as list of tuple of Cell objects for count > 1. Value is Cell object
        if count is 1 i.e. default.
        Set compl_str to 1 if you want complete string on search string or pattern
        matches.
        Set case_sesitive to 1 for exact case matching.
        """
        match_info = collections.OrderedDict({})
        row_values = self.sheet_matrix[row]
        match_count = (len(row_values) - 1) if count == "max" else count
        # Empty row
        if not row_values:
            return None
        match_pattern = None
        if case_sesitive:
            match_pattern = re.compile(pattern)
        else:
            match_pattern = re.compile(pattern, re.I)
        for column, value in enumerate(row_values):
            #value = ' '.join(value.split("\n"))
            # skip empty cells
            if not value:
                continue
            match = match_pattern.search(value)
            if match:
                match_count -= 1
                match_str = value if compl_str else match.group()
                if match_str in match_info:
                    match_info[match_str].append(Cell(row, column))
                else:
                    match_info[match_str] = [Cell(row, column)] if match_count > 1 else Cell(row, column)
            if match_count == 0:
                return match_info
            column += 1

        return match_info

    def searchStringInColumn(self, pattern, column, count=1, compl_str=0, case_sensitive=0):
        """
        Search for pattern or string in specified column.
        Specify count for number of occurrence to search. Default value is 1.
        Returns dictionary having key as 'matched string/pattern' and value
        as list of tuple of Cell objects for count > 1. Value is Cell object
        if count is 1 i.e. default.
        Set compl_str to 1 if you want complete string on search string or pattern
        matches.
        Set case_sesitive to 1 for exact case matching.
        """
        match_info = collections.OrderedDict({})
        col_values = self.getColValues(column)
        match_count = (len(col_values) - 1) if count == "max" else count
        if not col_values:
            return None
        match_pattern = None
        if case_sensitive:
            match_pattern = re.compile(pattern)
        else:
            match_pattern = re.compile(pattern, re.I)
        for row, value in enumerate(col_values):
            # skip empty cells
            if not value:
                continue
            match = match_pattern.search(value)
            if match:
                match_count -= 1
                match_str = value if compl_str else match.group()
                if match_str in match_info:
                    match_info[match_str].append(Cell(row, column))
                else:
                    match_info[match_str] = [Cell(row, column)] if match_count > 1 else Cell(row, column)
            if match_count == 0:
                return match_info

        return match_info

    def getRows(self, start_row, count=1):
        """
        Returns list of row/rows starting from row index start_row.
        """
        row = start_row
        row_list = []
        if start_row < 0 or start_row > self.max_row:
            raise ValueError("Row value needs to be between 0 and max_row [{}]".format(self.max_row))
        if count > (self.max_row - start_row):
            raise ValueError("row count exceeds total rows count in sheet")
        while count > 0:
            row_list.append(self.getRowValues(row))
            row += 1
            count -= 1

        return row_list

    def getCols(self, start_col=0, count=1):
        """
        Returns list of column/columns starting from column index start_col.
        """
        column = start_col
        column_list = []
        if start_col < 0 or start_col > self.max_col:
            raise ValueError("Column value needs to be between 0 and max_col [{}]".format(self.max_col))
        if count > (self.max_col - start_col):
            raise ValueError("column count exceeds total column count in sheet")
        while count > 0:
            column_list.append(self.getColValues(column))
            column += 1
            count -= 1
        return column_list

    def getRowValues(self, row, start_col=0, end_col=None):
        """
        Returns a list of values in row starting from index start_col to end_col
        """
        if not end_col:
            end_col = self.max_col
        if start_col == 0 and not end_col:
            return self.sheet_matrix[row]
        else:
            return self.sheet_matrix[row][start_col:end_col]

    def getColValues(self, column, start_row=0, end_row=None):
        """
        Returns a list of values in column starting from index start_row
        to end_row
        """
        if not end_row:
            end_row = self.max_row
        col_values = []
        for index in xrange(start_row, end_row):
            col_values.append(self.sheet_matrix[index][column])
        return col_values

    def getCellValue(self, row, column):
        if row > self.max_row or column > self.max_col:
            raise ValueError('Cell row or column index is greter than max index.')
        return self.sheet_matrix[row][column]

if __name__ == '__main__':
    print(__Author__)