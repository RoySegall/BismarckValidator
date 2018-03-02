import os
import glob
import pandas as pd
import unittest
from unittest import TestCase
from bismarck_report import BismarckReport


class TestsBismarkReport(TestCase):
    """
    Testing the file processing.
    """

    def test_load_report(self):
        """
        Testing the file is being processed into an object correctly.
        """
        report_file_name = glob.glob('{}/report_processor/fixtures/*.xlsx'.format(os.getcwd()))[0]

        # todo: Check the list of sheets are in the object.
        # todo: Check the list of fields are in the object.
        # todo: Check we have values in the object.
        return
        if not os.path.isfile(report_file_name):
            print('File not found: {}'.format(report_file_name))
            return

        pandas_excel = pd.ExcelFile(report_file_name)
        b_report = BismarckReport(pandas_excel)
        b_report.process_book()


if __name__ == "__main__":
    unittest.main()
