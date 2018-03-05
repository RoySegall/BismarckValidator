from rosetta.validations import Validations


class TestsPlugins(object):

    def test_not_null(self):
        validators = Validations()

        assert validators.not_null(val='').items() <= ({'result': False, 'msg': "Invalid empty string value"}).items()
        assert validators.not_null(val=None).items() <= ({'result': False, 'msg': "Invalid 'None' value"}).items()

    def test_asset_type(self):
        validators = Validations()
        asset_types = ['הלוואות', 'ניירות ערך סחירים', 'ניירות ערך לא סחירים', 'מזומנים', 'זכויות', 'השקעות אחרות']

        # Positive value tests.
        for asset in asset_types:
            assert validators.asset_type(asset).items() <= ({'result': True}).items()

        # Negative value tests.
        assert validators.asset_type(val='junk value').items() <= (
            {'result': False, 'msg': "unrecognized asset type"}).items()

        assert validators.asset_type(val=None).items() <= (
            {'result': False, 'msg': "unrecognized asset type"}).items()

        assert validators.asset_type(val='').items() <= (
            {'result': False, 'msg': "unrecognized asset type"}).items()

    def test_decimal_positive(self):
        validators = Validations()
        assert validators.decimal_positive(val=1.11).items() <= ({'result': True, 'msg': ''}).items()
        assert validators.decimal_positive(val=1).items() <= (
            {'result': False, 'msg': "The value 1 must have 2 numbers after decimal point"}).items()
        assert validators.decimal_positive(val=1.111).items() <= (
            {'result': False, 'msg': "The value 1.111 must have 2 numbers after decimal point"}).items()
        assert validators.decimal_positive(val='abc').items() <= (
            {'result': False, 'msg': "The value abc not a decimal or not defined"}).items()
        assert validators.decimal_positive(val=-1.11).items() <= (
            {'result': False, 'msg': "The value -1.11 must be positive decimal"}).items()
        assert validators.decimal_positive(val=None).items() <= (
            {'result': False, 'msg': "The value None not a decimal or not defined"}).items()

    def test_decimal_negative(self):
        validators = Validations()
        assert validators.decimal_negative(val=-1.11).items() <= ({'result': True, 'msg': ''}).items()
        assert validators.decimal_negative(val=-1).items() <= (
            {'result': False, 'msg': "The value -1 must have 2 numbers after decimal point"}).items()
        assert validators.decimal_negative(val=-1.111).items() <= (
            {'result': False, 'msg': "The value -1.111 must have 2 numbers after decimal point"}).items()
        assert validators.decimal_negative(val='abc').items() <= (
            {'result': False, 'msg': "The value abc not a decimal or not defined"}).items()
        assert validators.decimal_negative(val=1.11).items() <= (
            {'result': False, 'msg': "The value 1.11 must be negative decimal"}).items()
        assert validators.decimal_negative(val=None).items() <= (
            {'result': False, 'msg': "The value None not a decimal or not defined"}).items()

    def test_is_positive(self):
        validators = Validations()
        assert validators.is_positive(val=1).items() <= ({'result': True}).items()
        assert validators.is_positive(val=-1).items() <= ({'result': False, 'msg': "Not a positive number"}).items()

    def test_is_float(self):
        validators = Validations()
        assert validators.is_float(val=1.2313).items() <= ({'result': True}).items()
        assert validators.is_float(val=1).items() <= ({'result': False, 'msg': "Not a float"}).items()

    def test_valid_currency(self):
        validators = Validations()

        currencies_list = ['דולר אוסטרליה', 'ריאל ברזילאי', 'דולר קנדי', 'פרנק שוויצרי', 'פסו ציליאני',
                           'יואן סיני', 'כתר דני', 'אירו', 'ליש"ט', 'דולר הונג קונג', 'פורינט הונגרי',
                           'רופי הודי', 'יין יפני', 'פזו מכסיקני', 'שקל חדש ישראלי', 'כתר נורווגי',
                           'ניו זילנד דולר', 'זלוטי פולני', 'רובל רוסי', 'כתר שוודי', 'דולר סינגפורי',
                           'לירה טורקית', 'דולר טיוואני', 'דולר ארהב', 'רנד דרא"פ', 'UNKNOWN',
                           ]

        # Positive value tests.
        for currency in currencies_list:
            assert validators.valid_currency(currency).items() <= ({'result': True}).items()

        # Negative value tests.
        assert validators.valid_currency(val='junk value').items() <= (
            {'result': False, 'msg': "currency junk value not recognized"}).items()

        assert validators.valid_currency(val=None).items() <= (
            {'result': False, 'msg': "currency None not recognized"}).items()

        assert validators.valid_currency(val='').items() <= (
            {'result': False, 'msg': "currency  not recognized"}).items()

    def test_date_format(self):
        validators = Validations()
        assert validators.date_format("06/25/1989", "%d/%m/%Y").items() <= (
            {'result': False, 'msg': "Incorrect date format, should be DD/MM/YYYY"}).items()

        assert validators.date_format("25/06/1989", "%d/%m/%Y").items() <= (
            {'result': True}).items()

    def test_digits_amount(self):
        validators = Validations()

        # Positive value tests.
        assert validators.digits_amount(1000, 2).items() <= (
            {'result': True}).items()

        # Negative value tests.
        assert validators.digits_amount(10000, 10).items() <= (
            {'result': False, 'msg': "Value exceeded digits boundary"}).items()

    def test_number_in_range(self):
        validators = Validations()

        assert validators.number_in_range(50, 20, 60).items() <= ({'result': True}).items()
        assert validators.number_in_range(20, 50, 60).items() <= (
            {'result': False, 'msg': "Value is not in the correct range."}
        ).items()

    def test_instrument_sub_type(self):
        validators = Validations()

        # Positive value tests.
        assert validators.instrument_sub_type("תעודות התחייבות ממשלתיות").items() <= (
            {'result': True}).items()

        # Negative value tests.
        assert validators.instrument_sub_type("Pizza").items() <= (
            {'result': False, 'msg': "unrecognized asset type"}).items()
