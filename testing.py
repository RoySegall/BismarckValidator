import pandas as pd
import os

from ReportProcessor.BismarkReport import BismarkReport

pandas_excel = pd.ExcelFile(os.getcwd() + '/ReportProcessor/513026484_gsum_0317.xlsx')
new_report = BismarkReport(pandas_excel)
print(new_report)

