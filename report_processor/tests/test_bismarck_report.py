import os
import glob
import pandas as pd
import unittest
from unittest import TestCase
from ..bismarck_report import BismarckReport


class BismarckReportTest(TestCase):

    def setUp(self):
        # btest = BismarckReportTest()
        # btest.test_load_report()
        pass

    def test_load_report(self):
        print(os.getcwd())
        report_file_name = glob.glob('{}/report_processor/fixtures/*.xlsx'.format(os.getcwd()))[0]

        if not os.path.isfile(report_file_name):
            print('File not found: {}'.format(report_file_name))
            return

        pandas_excel = pd.ExcelFile(report_file_name)
        b_report = BismarckReport(pandas_excel)
        b_report.process_book()


if __name__ == "__main__":
    unittest.main()
