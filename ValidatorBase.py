class ValidatorBase(object):

    # The header size.
    header_size = 0

    # The columns.
    columns_count = 0

    # The number of rows.
    rows_count = 0

    # The instrument name.
    instrument = ''

    # Field name.
    field = ''

    # Define if the current value is context or not.
    is_context = False

    # The context name.
    context_name = ''

    # The name of sub spreadsheet.
    instrument_dict_validations = {
        'CASH': 'cash_validation',
    }

    # List of errors.
    errors = []

    # todo Add setters and getters.

    # todo: move to a sub plugin.
    def cash_validation(self, value):
        if value == 'roy':
            return

        self.errors.append({
            "field": "name",
            "line": 24,
            "error": "The value must be roy."
        })
