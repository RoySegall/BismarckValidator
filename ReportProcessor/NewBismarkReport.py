class NewBismarkReport(object):

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

    general_errors = {

    }

    errors_output = []

    # errors_output = {
    #     'CASH': [
    #         14: [
    #             3: ['The field cannot be empty', 'The field is not in the right range']
    #         ]
    #     ]
    # }

    def __init__(self, pandas_sheets):
        """
        Init the objct.

        :param pandas_sheets:
            The pandas object of the file.
        """
        self.pandas_sheets = pandas_sheets

    def process_file(self):
        for sheet in self.pandas_sheets.sheet_names:
            if sheet not in ('סכום נכסי הקרן'):
                self.get_sheet_data(sheet)

    def get_sheet_data(self, sheet):
        """
        Process the sheet.

        :param sheet:
            The name of the sheet.
        """
        # for index, row in df.iterrows():
    # Get the table fields.
    # Start to the values of the table.
