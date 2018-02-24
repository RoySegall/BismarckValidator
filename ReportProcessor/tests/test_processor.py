import os
import glob
from ..ReportProcessor import ReportProcessor, BismarckReport


class TestReportProcessor(object):

    def test_load_xls(self):

        report = ReportProcessor()
        file_to_load = glob.glob('{}/fixtures/*.xlsx*'.format(os.getcwd()))
        print(file_to_load)
        report.get_report(file_to_load[0])

        assert True

