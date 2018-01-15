import decimal
import datetime


class Validations(object):
    currencies_list = [
        'דולר אוסטרליה',
        'ריאל ברזילאי',
        'דולר קנדי',
        'פרנק שוויצרי',
        'פסו ציליאני',
        'יואן סיני',
        'כתר דני',
        'אירו',
        'ליש"ט',
        'דולר הונג קונג',
        'פורינט הונגרי',
        'רופי הודי',
        'יין יפני',
        'פזו מכסיקני',
        'שקל חדש ישראלי',
        'כתר נורווגי',
        'ניו זילנד דולר',
        'זלוטי פולני',
        'רובל רוסי',
        'כתר שוודי',
        'דולר סינגפורי',
        'לירה טורקית',
        'דולר טיוואני',
        'דולר ארהב',
        'רנד דרא"פ',
        'UNKNOWN',
    ]

    def not_null(self, val):
        """
        Check if the value is none or not defined.
        """
        try:
            if val is None:
                return {'result': False, 'msg': "Invalid 'None' value"}
        except NameError:
            return {'result': False, 'msg': "undefined value"}

        return {'result': True}

    def asset_type(self, val):
        """
        Check if value is one of the asset types.
        """
        asset_types = ['הלוואות', 'ניירות ערך סחירים', 'ניירות ערך לא סחירים', 'מזומנים', 'זכויות', 'השקעות אחרות']

        if val in asset_types:
            return {'result': True}

        return {'result': False, 'msg': "unrecognized asset type"}

    def decimal_positive(self, val):
        """
        Check if value is decimal positive with 2 positions after floating point.
        """
        return self.__decimal(val, True)

    def decimal_negative(self, val):
        """
        Check if value is decimal positive with 2 positions after floating point.
        """
        return self.__decimal(val, False)

    def __decimal(self, val, is_positive=True):
        """
        Check if the variable is decimal or not.

        :param val:
            The value to check.
        :param is_positive:
            Determine if we allowed that the value can be positive or not.

        :return:
        """

        # The object with the results of the functions.
        results = {
            'result': True,
            'msg': '',
        }

        try:
            d = decimal.Decimal(val)

            if d.as_tuple().exponent == -2:
                sign = "positive"
                if not is_positive:
                    sign = "negative"
                    d = d * -1

                if d > 0:
                    return results
                else:
                    return {
                        'result': False,
                        'msg': "The value %s must be %s decimal" % (val, sign)
                    }

            else:
                return {
                    'result': False,
                    'msg': "The value %s must have 2 numbers after decimal point" % val
                }

        except ValueError:
            return {
                'result': False,
                'msg': "The value %s not a decimal or not defined" % val
            }

    def is_positive(self, val):
        """

        :param val:
        :return:
        """
        number = float(val)
        if number > 0:
            return {'result': True}
        else:
            return {'result': False, 'msg': "Not a positive number"}

    def is_float(self, val):
        """

        :param val:
        :return:
        """
        try:
            float(val)
            return {'result': True}
        except ValueError:
            return {'result': False, 'msg': "Not a float"}

    def valid_currency(self, val):
        """

        :param val:
        :return:
        """

        if val in self.currencies_list:
            return {'result': True}

        print("currency %s not recognized" % val)
        return False

    def date_format(self, val):
        """

        :param val:
        :return:
        """
        try:
            datetime.datetime.strptime(val, '%d/%m/%Y')
            return {'result': True}
        except ValueError:
            return {'result': False, 'msg': "Incorrect date format, should be DD/MM/YYYY"}

    def digits_amount(self, val, min_digits, max_digits=0):
        """
        
        :param val:
        :param min_digits:
        :param max_digits:
        :return:
        """
        if val.lenght > min_digits & max_digits == 0:
            return {'result': True}

        if val.lenght > min_digits & val.lenght < max_digits:
            return {'result': True}

        return {'result': False, 'msg': "Value exceeded digits boundary"}

