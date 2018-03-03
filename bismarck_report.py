class BismarckReport(object):

    # Hold the list of the sheets and their code.
    instrument_dict = {
        'מזומנים': 'CASH',
        'תעודות התחייבות ממשלתיות': 'GDC',
        'תעודות חוב מסחריות': 'CDC',
        'אג"ח קונצרני': 'CB',
        'מניות': 'STOCK',
        'תעודות סל': 'ETF',
        'קרנות נאמנות': 'MF',
        'כתבי אופציה': 'WARRANTS',
        'אופציות': 'OPTIONS',
        'חוזים עתידיים': 'FC',
        'מוצרים מובנים': 'SP',
        'לא סחיר - תעודות התחייבות ממשלתי': 'GDC',
        'לא סחיר - תעודות התחייבות ממשלת': 'GDC',
        'לא סחיר - תעודות חוב מסחריות': 'CDC',
        'לא סחיר - אג"ח קונצרני': 'CB',
        'לא סחיר - מניות': 'STOCK',
        'לא סחיר - קרנות השקעה': 'IF',
        'לא סחיר - כתבי אופציה': 'WARRANTS',
        'לא סחיר - אופציות': 'OPTIONS',
        'לא סחיר - חוזים עתידיים': 'FC',
        'לא סחיר - מוצרים מובנים': 'SP',
        'הלוואות': 'LOANS',
        'פקדונות מעל 3 חודשים': 'DOTM',
        'זכויות מקרקעין': 'LR',
        'השקעות אחרות': 'OI',
        'השקעה בחברות מוחזקות': 'IC',
        'יתרת התחייבות להשקעה': 'ICB',
        'עלות מותאמת אג״ח קונצרני סחיר': 'CBAC',
        'עלות מותאמת אג״ח קונצרני לא סחיר': 'CBAC',
        'עלות מותאמת מסגרות אשראי ללווים': 'BCAC',
    }

    # Keep the list of fields and their english representation.
    field_list = {
        'מספר ני"ע': 'instrument_id',
        'מספר מנפיק': 'issuer_id',
        'דירוג': 'rating',
        'שם מדרג': 'rating_Agency',
        'סוג מטבע': 'currency',
        'שיעור ריבית': 'intrest_Rate',
        'תשואה לפידיון': 'yield',
        'שווי שוק': 'market_Cap',
        'שעור מנכסי אפיק ההשקעה': 'rate_of_investment_channel',
        'שעור מסך נכסי השקעה': 'rate_of_Fund',
        'זירת מסחר': 'trading_floor',
        'תאריך רכישה': 'date_of_purchase',
        'מח"מ': 'average_of_Duration',
        'ערך נקוב': 'par_value',
        'שער': 'rate',
        'שעור מערך נקוב מונפק': 'rate_of_ipo',
        'ספק המידע': 'informer',
        'שווי הוגן': 'fair_value',
        'ענף מסחר': 'activity_industry',
        'תאריך שערוך אחרון': 'date_of_revaluation',
        'אופי הנכס': 'type_of_asset',
        'שעור תשואה במהלך התקופה': 'tmp_name',
        'סכום ההתחייבות': 'liabilities',
        'תאריך סיום ההתחייבות': 'expiry_date_of_liabilities',
        'שער ריבית': 'rate',
        'ריבית אפקטיבית': 'effective_rate',
        'עלות מתואמת': 'coordinated_cost',
        'נכס הבסיס': 'underlying_asset',
        'קונסורציום כן/לא': 'consortium',
        'שיעור ריבית ממוצע': 'average rate',
        'שווי מוערך': 'par_value',
        'כתובת הנכס': 'instrument_address',
        'פדיון/ ריבית לקבל': 'revenue_interest_receivable',
        'שם המנפיק/שם נייר ערך': 'issuer_name',
        'תנאי ושיעור ריבית': 'condition_and_interest_rate',
    }

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
        """
        Constructor.

        :param pandas_excel:
            The pandas object wrapping the excel file.
        """
        self.pandas_excel = pandas_excel

    def process_book(self):
        """
        Processing the excel file.
        """
        for sheet_name in self.pandas_excel.sheet_names:
            if sheet_name not in ('סכום נכסי הקרן'):
                self.process_sheet(self.pandas_excel, sheet_name)

    def process_sheet(self, xsl_object, sheet_name):
        """
        Processing a specific sheet.

        :param xsl_object:
            The pandas object wrapping the excel file.
        :param sheet_name:
            The sheet name.
        """
        sheet = xsl_object.parse(sheet_name, skiprows=7)

        context_range = self.get_sheet_context_range(sheet)

        for column in sheet.columns:

            if 'Unnamed' in column:
                continue

            for index, row_value in enumerate(sheet[column]):

                if str(row_value) == 'nan' or index >= 5:
                    continue

                context = self.get_context_from_context_range(context_range, index)

                print([self.instrument_dict[sheet_name], self.field_list[column], context, row_value])
                print([row_value, index, ])
                # row_name = str(sheet.index[index])
                # self.process_cell(column, index, row_name, row_value, context[index])

    def process_cell(self, column, index, row_name, row_value, context):
        """
        Processing a file.

        :param column:
        :param index:
        :param row_name:
        :param row_value:
        :param context:

        """
        # todo: Add preperation actions before rosseta checks.
        self.errors_output.append(self.check_rosseta(column, index, row_name, row_value, context))

    def check_rosseta(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        # todo implement connection to rosseta module.
        return ''

    def get_sheet_context_range(self, sheet):
        """
        Build the context range. Due to fact that when iterating the lines we cannot know for sure what is the
        contexts we need to create a range dictionary; The dictionary will tell us when a context start and it's end
        thus gives us the option to know what is the current context when iterating.

        :param sheet:
            The sheet object.

        :return:
            List of contexts.
        """
        range_dict = {}
        for column in sheet.columns:

            if 'Unnamed' in column:
                continue

            i = 1
            for _, value in sheet[column].iteritems():

                if value == 'סה"כ בישראל':
                    range_dict['il'] = {
                        'start': i
                    }

                if value == 'סה"כ בחו"ל':
                    range_dict['il']['end'] = i
                    range_dict['not_il'] = {
                        'start': i
                    }

                i = i + 1
        return range_dict

    def get_context_from_context_range(self, context_range, index):
        """
        Get the context of the current line from the context range and line number.

        :param context_range:
            The context range dict.
        :param index:
            The index of the row.
        :return:
        """
        if context_range['il']['start'] <= index <= context_range['il']['end']:
            return 'il'
        else:
            return 'not_il'
