import os
import glob
import pandas as pd
import dateutil.parser
from .bismarck_report import BismarckReport


class ReportProcessor(BismarckReport):

    def __init__(self):
        pass

    def get_report(self, report_file_name):
        b_report = BismarckReport
        pandas_excel = pd.ExcelFile(report_file_name)

        b_report_metadata = self.get_report_metadata(report_file_name, pandas_excel)

        # Loop over all the sheets in the file
        for sheet_name in pandas_excel.sheet_names:
            if sheet_name not in ('סכום נכסי הקרן'):
                self.get_sheet_data(pandas_excel, sheet_name)

        return BismarckReport

    def get_report_metadata(self, report_file_name, pandas_excel):
        """
        example for metadata dict structure:
        {
            'file_name': '',
            'managing_body': '',
            'year': '',
            'month': '',
            'quarter': '',
            'file_level_results': []
        }
        :param pandas_excel:
        :return: dict of above structure
        """

        meta_data = {}
        meta_data['file_name'] = os.path.basename(report_file_name)

        return {
            'file_name': '',
            'managing_body': '',
            'year': '',
            'month': '',
            'quarter': '',
            'file_level_results': []
        }

    """
    private functions
    """
    def get_sheet_data(self, pandas_excel, sheet_name):
        pass

    def _calculate_rows_to_skip(self, xls_file, sheet_name):
        """ ToDo - refactor the function for current class """
        rows_to_skip_calculated = 0

        while rows_to_skip_calculated < 10:
            pre_sheet = xls_file.parse(sheet_name, skiprows=rows_to_skip_calculated)
            pre_sheet_columns = list()

            # Something
            if len(pre_sheet.columns) > 0:
                pre_sheet_columns = list(pre_sheet.columns.str.strip())

            # Something
            if ('שם נ"ע' in pre_sheet_columns) or \
                    ('שם המנפיק/שם נייר ערך' in pre_sheet_columns) or \
                    ('שם נייר ערך' in pre_sheet_columns) or \
                    ('מזומנים ושווי מזומנים' in pre_sheet_columns) or \
                    ('מספר נ"ע' in pre_sheet_columns) or \
                    ('זכויות במקרעין' in pre_sheet_columns):
                return rows_to_skip_calculated

            # Move to the next row
            rows_to_skip_calculated += 1

        return rows_to_skip_calculated

    def read_sheet(self, xls_file, sheet_name):
        # Loop over all the sheets in the file
        for sheet_name in xls_file.sheet_names:
            if sheet_name not in ('סכום נכסי הקרן'):
                read_sheet(xls_file, sheet_name, split_filename[0], quarter)

        print('Finish with {filename}'.format(filename=filename))
