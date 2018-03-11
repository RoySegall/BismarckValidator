import os
from rosetta.rosetta import Rosetta


class BismarckReport(object):

    general_errors = {}

    # errors_output = {
    #     'CASH': [
    #         14: [
    #             3: ['The field cannot be empty', 'The field is not in the right range']
    #         ]
    #     ]
    # }
    errors_output = []
    meta_report = {}

    def __init__(self, pandas_excel):
        self.pandas_excel = pandas_excel

    def process_book(self):
        for sheet_name in self.pandas_excel.sheet_names:
            if sheet_name not in ('סכום נכסי הקרן'):
                self.process_sheet(self.pandas_excel, sheet_name)

    def process_sheet(self, xsl_object, sheet_name):
        sheet = xsl_object.parse(sheet_name, skiprows=7, index_col=1)

        context = self.get_sheet_context(sheet)

        for column in sheet.columns:
            if 'Unnamed' in column:
                continue
            for index, row_value in enumerate(sheet[column]):
                row_name = str(sheet.index[index])

                self.process_cell(sheet_name=sheet_name,
                                  column=column,
                                  index=index,
                                  row_name=row_name,
                                  row_value=row_value,
                                  context=context[index])

        # if self.errors_output:
        #     with open('post_rosetta.json', 'a', encoding='utf-8') as the_file:
        #         the_file.write(str(self.errors_output))

    def process_cell(self, **kwargs):
        if kwargs.get('context'):
            kwargs['field'] = kwargs.pop('column')
            rosetta_result = self.check_rosseta(**kwargs)

            # aggregate validation results
            if rosetta_result:
                self.errors_output.append(str(rosetta_result))

    def check_rosseta(self, *args, **kwargs):
        return Rosetta().validate_proxy(*args, **kwargs)

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
