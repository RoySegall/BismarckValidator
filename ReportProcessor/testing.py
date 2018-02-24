import pandas as pd
import os


from ReportProcessor.NewBismarkReport import NewBismarkReport

pandas_excel = pd.ExcelFile(os.getcwd() + '/tests/')
new_report = NewBismarkReport(pandas_excel)

