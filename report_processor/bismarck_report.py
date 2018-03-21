import os
import json
import pandas as pd
from rosetta.rosetta import Rosetta


class BismarckReport(object):
    __SKIP_ROWS = 7
    __SKIP_ROWS_PADDING = 9
    __MUTED_SHEET_NAME = 'סכום נכסי הקרן'

    meta_report = {}
    compact_report = {}
    flat_report = []

    def __init__(self, report_file_name=None, pandas_excel=None):
        self.is_ready = False
        if not report_file_name and not pandas_excel:
            raise ValueError('Expected either report_file_name or pandas_excel args')
        if not pandas_excel:
            pandas_excel = pd.ExcelFile(report_file_name)
        self.pandas_excel = pandas_excel
        self.rosetta = Rosetta()

    def process_book(self):
        for sheet_name in self.pandas_excel.sheet_names:
            if sheet_name not in self.__MUTED_SHEET_NAME:
                self.process_sheet(self.pandas_excel, sheet_name)

        self.is_ready = True

        if self.flat_report:
            with open('flat_report.json', 'a', encoding='utf-8') as the_file:
                the_file.write(str(self.flat_report))

        if self.flat_report:
            self.get_compact()
            with open('compact_report.json', 'a', encoding='utf-8') as the_file:
                the_file.write(str(json.dumps(
                    self.compact_report,
                    ensure_ascii=False,
                    skipkeys=True,
                    indent=2,
                    allow_nan=True)))

    def process_sheet(self, xsl_object, sheet_name):
        sheet = xsl_object.parse(sheet_name, skiprows=self.__SKIP_ROWS, index_col=1)

        context = self.get_sheet_context(sheet)

        # append calculated column for rating validation
        if 'שם מדרג' in sheet.columns:
            sheet = self.gen_rating_merged(sheet, 'שם מדרג', 'דירוג')
        elif 'שם המדרג' in sheet.columns:
            sheet = self.gen_rating_merged(sheet, 'שם המדרג', 'דירוג')

        for column in sheet.columns:
            if 'Unnamed' in column:
                continue
            for index, row_value in enumerate(sheet[column]):
                row_name = str(sheet.index[index])

                self.process_cell(sheet_name=sheet_name,
                                  column=column,
                                  index=index,
                                  context=context[index],
                                  row_name=row_name,
                                  row_value=row_value)

    def process_cell(self, **kwargs):
        if kwargs.get('context'):
            kwargs['field'] = kwargs.pop('column')
            rosetta_result = self.check_rosetta(**kwargs)

            # aggregate validation results
            if rosetta_result:
                result_dict = {'sheet_code': '', 'field_code': ''}
                result_dict.update(kwargs)

                result_dict['sheet_code'] = self.rosetta.get_sheet(result_dict['sheet_name'])
                result_dict['field_code'] = self.rosetta.get_field(result_dict['field'])
                result_dict['results'] = '{}'.format(str(rosetta_result).replace('"', '').replace("'", ""))
                result_dict['index'] = kwargs['index'] + self.__SKIP_ROWS_PADDING
                self.flat_report.append(result_dict)

    def check_rosetta(self, *args, **kwargs):
        return self.rosetta.validate(*args, **kwargs)

    def get_sheet_context(self, sheet):
        # find context column
        context_col = ''
        for col in sheet.columns:
            if col in [
                'שם המנפיק/שם נייר ערך',
                'שם נייר ערך',
                'שם נ"ע',
                'מספר הנייר',
                'מספר נ"ע',
                'אופי הנכס',
                'מספר ני"ע',
                'מספר מנפיק',
                'תאריך סיום ההתחייבות',
            ]:
                context_col = col
                break

        # identify context for each row: Israel=IL, Abroad=ABR, Other=None
        context = []
        is_israel = True

        for index, row_value in enumerate(sheet[context_col]):
            # check if abroad section reached
            row_name = str(sheet.index[index])
            if 'במט"ח' in row_name or 'סה"כ בחו"ל' in row_name:
                is_israel = False

            # register context
            if not str(row_value) in 'nan' and row_name not in ['nan', '0'] and is_israel:
                context.append('IL')
            elif not str(row_value) in 'nan' and row_name not in ['nan', '0'] and not is_israel:
                context.append('ABR')
            else:
                context.append(None)

            # print('{};{};{};{}'.format(index, sheet.index[index], row_value, context[index]))

        return context

    def gen_rating_merged(self, sheet, *args):
        # df = pd.DataFrame({'Year': ['2014', '2015'], 'quarter': ['q1', 'q2']})
        # df['period'] = df[['Year', 'quarter']].apply(lambda x: ''.join(x), axis=1)
        sheet['agencyplusrating'] = sheet[args[0]] + sheet[args[1]]
        return sheet

    def is_ready(self):
        return self.is_ready

    def get_flat(self):
        return self.flat_report

    def get_compact(self):
        compact_report = {}
        for row in self.flat_report:
            if not row['sheet_code'] in compact_report:
                compact_report[row['sheet_code']] = {}
                compact_report[row['sheet_code']][row['field_code']] = {}
            elif not row['field_code'] in compact_report[row['sheet_code']]:
                compact_report[row['sheet_code']][row['field_code']] = {}

            compact_report[row['sheet_code']][row['field_code']][str(row['index'])] = row['results']

        self.compact_report = compact_report
        return compact_report

    def get_xsl(self, path):
        # report_file_name
        writer = pd.ExcelWriter(path)
        df1 = pd.DataFrame(self.flat_report)
        df1.to_excel(writer, 'Sheet1')
        writer.save()
