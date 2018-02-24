import pandas as pd
import os


from ReportProcessor.NewBismarkReport import NewBismarkReport

pandas_excel = pd.ExcelFile(os.getcwd() + '/tests/513026484_gsum_0317.xlsx')
new_report = NewBismarkReport(pandas_excel)

