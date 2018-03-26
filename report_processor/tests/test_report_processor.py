import os
import glob
import pandas as pd
import unittest
from unittest import TestCase
from report_processor.bismarck_report import BismarckReport
from report_processor.report_processor import ReportProcessor


class ReportProcessorTest(TestCase):

    def test_load_report(self):
        print(os.getcwd())

        report_files = glob.glob('{}/report_processor/fixtures/batch'.format(os.getcwd()))[0]
        reports = ReportProcessor()
        reports.process_folder(report_files)

if __name__ == "__main__":
    unittest.main()
