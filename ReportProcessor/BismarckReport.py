import pandas as pd


class BismarckReport(object):
    """
    Data class representing single report file to be validated with bismarck reports validator.
    """
    data = {
        'metadata': {
            'file_name': '',
            'managing_body': '',
            'checksum': '',
            'year': '',
            'month': '',
            'quarter': '',
            'file_level_results': [
                {
                    'result': '',
                    'msg': ''
                },
            ],
        },
        'sheets': [
            {
                'sheet_name': '',
                'sheet_code': '',
                'rows_to_skip': '',
                'number_of_columns': '',
                'source_data': pd.DataFrame,
                'sheet_level_results': [
                    {
                        'result': '',
                        'msg': ''
                    },
                ],
                'validation_results': [
                    {
                        'column_name': '',
                        'column_code': '',
                        'column_level_results': [
                            {
                                'result': '',
                                'msg': ''
                            },
                        ],
                        'rows': [
                            {
                                'row_number': '',
                                'context': '',
                                'number_of_validations': '',
                                'row_level_results': [
                                    {
                                        'result': '',
                                        'msg': ''
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }

    def get_file_metadata(self):
        pass

    def append_file_metadata(self):
        pass

    def get_sheet(self):
        pass

    def append_sheet(self):
        pass

    def get_validation_results(self):
        pass

    def append_validation_results(self):
        pass

