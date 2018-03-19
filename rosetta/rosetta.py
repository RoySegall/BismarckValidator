import yaml
import os

from .rosetta_validations import Validations
from .rosetta_config import RosettaConfig


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Rosetta(object, metaclass=Singleton):

    # The folder of the yml files.
    folder = os.path.join(os.path.dirname(__file__), 'validation_templates')

    # Holds the list of contexts.
    rosetta = {}

    # Keep the list of fields and their english representation.
    fields_list = RosettaConfig.FIELDS_LIST

    # Hold the list of the sheets and their code.
    instrument_dict = RosettaConfig.INSTRUMENT_DICT

    # Constraints dict
    constraints_dict = {}

    def __init__(self, folder=None):
        if folder:
            self.folder = folder
        self.constraints_dict = self.get_constraints()

    def get_constraints(self):
        """
        Load sheets validations Specs.
        :return:
        """
        for filename in os.listdir(self.folder):
            if not filename.endswith('.yml'):
                continue
            with open(os.path.join(self.folder, filename), 'rt') as stream:
                yml_file = yaml.load(stream)
            self.rosetta[filename.split('.')[0]] = yml_file['fields']

        return self.rosetta

    def validate_proxy(self, *args, **kwargs):
        """
        Helper function during development, channels piped data to files for debug.
        """
        if self.validate(**kwargs):
            prn = self.validate(**kwargs)
            # json output
            with open('rosetta_results.json', 'a', encoding='utf-8') as the_file:
                the_file.write(
                    '{"sheet_name": "%s", "field": "%s", "index": %s, "row_name": "%s",'
                    ' "row_value": "%s", "context": "%s", "results": %s},\n' % (
                        str(kwargs.get('sheet_name')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('field')).replace("'", "\\'").replace('"', '\\"'),
                        kwargs.get('index'),
                        str(kwargs.get('row_name')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('row_value')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('context')).replace("'", "\\'").replace('"', '\\"'),
                        str(self.validate(**kwargs))
                    ))
            # csv output
            with open('rosetta_results.csv', 'a', encoding='utf-8') as the_file:
                the_file.write(
                    '%s|%s|%s|%s|%s|%s|%s\n' % (
                        str(kwargs.get('sheet_name')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('field')).replace("'", "\\'").replace('"', '\\"'),
                        kwargs.get('index'),
                        str(kwargs.get('row_name')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('row_value')).replace("'", "\\'").replace('"', '\\"'),
                        str(kwargs.get('context')).replace("'", "\\'").replace('"', '\\"'),
                        str(self.validate(**kwargs))
                    ))

            # with open('post_rosetta.json', 'a', encoding='utf-8') as the_file:
            #     the_file.write(str(self.validate(**kwargs)))
            # return self.validate(**kwargs)
        return

    def get_sheet(self, sheet):
        if sheet in self.instrument_dict:
            return self.instrument_dict[sheet]
        return

    def get_field(self, field):
        if field in self.fields_list:
            return self.fields_list[field]
        return

    def validate(self, *args, **kwargs):
        """
        Validates cell level data with the rosetta constraints.
        :param **sheet_name = sheet_name,
        :param **field = field,
        :param **index = index,
        :param **row_name = row_name,
        :param **row_value = row_value,
        :param **context = context[index]
        :return: errors list, if any found
        """
        result_list = []

        # lookup sheet and field (hebrew input to standardized  english)
        sheet = str(self.get_sheet(kwargs.get('sheet_name'))).lower()
        if not sheet:
            return 'Invalid sheet error: {}'.format(kwargs.get('sheet_name'))
        field = str(self.get_field(kwargs.get('field'))).lower()
        if not field:
            return 'Invalid field error: {}'.format(kwargs.get('field'))

        # if no validations exist for current sheet or field, skip validation
        if not (sheet in self.constraints_dict) or not (field in self.constraints_dict[sheet]):
            return

        validator = Validations()
        for validation in self.constraints_dict[sheet][field]:
            validate = getattr(validator, validation['func'])
            try:
                result = validate(val=kwargs.get('row_value'), **validation['args'])
                # register only failed asserts
                if not result['result']:
                    result_list.append(result['msg'])
            except Exception as e:
                result_list.append(e)

        return result_list
