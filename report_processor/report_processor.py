import os
import glob
import pandas as pd
import dateutil.parser
from .bismarck_report import BismarckReport


class ReportProcessor(object):

    def process_folder(self, path):

        for file in glob.glob('{}/*.xlsx'.format(path)):
            filename, file_extension = os.path.splitext(file)
            if file_extension == '.xlsx':
                try:
                    b_report = BismarckReport(file)
                    b_report.process_book()
                    b_report.get_xlsx(path)
                except Exception as e:
                    print(file)
                    print(e)
        return
