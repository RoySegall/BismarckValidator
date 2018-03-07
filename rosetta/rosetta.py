import yaml
import os

from .validations import Validations
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
    contexts = []

    # Holds the list of contexts.
    rosetta = {}

    # Keep the list of fields and their english representation.
    filds_list = RosettaConfig.FIELDS_LIST

    # Hold the list of the sheets and their code.
    instrument_dict = RosettaConfig.INSTRUMENT_DICT

    # constraints dict
    constraints_dict = {}

    def __init__(self, folder=None, contexts=None):
        if not contexts:
            contexts = ['in_israel', 'not_in_israel']
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

    def validate_object_test(self, *args, **kwargs):
        """
        helper function during development.
        generates input data for rosetta tests
        :param **sheet_name = sheet_name,
        :param **column = column,
        :param **index = index,
        :param **row_name = row_name,
        :param **row_value = row_value,
        :param **context = context[index]
        :return:
        """
        with open('pre_rosetta.json', 'a', encoding='utf-8') as the_file:
            the_file.write(
                '{"sheet_name": "%s", "column": "%s", "index": %s,"row_name": "%s",'
                ' "row_value": "%s", "context": "%s"},\n' % (
                    str(kwargs.get('sheet_name')).replace("'", "\\'").replace('"', '\\"'),
                    str(kwargs.get('column')).replace("'", "\\'").replace('"', '\\"'),
                    kwargs.get('index'),
                    str(kwargs.get('row_name')).replace("'", "\\'").replace('"', '\\"'),
                    str(kwargs.get('row_value')).replace("'", "\\'").replace('"', '\\"'),
                    str(kwargs.get('context')).replace("'", "\\'").replace('"', '\\"')
                ))

        return

    def get_sheet(self, sheet):
        """
        Get info for tab.

        :param sheet:
            The tab. i.e cache.

        :return:
        """
        if self.rosetta == {}:
            self.get_constraints()

        return self.rosetta[sheet]

    def validate_object(self, tab, _object):
        """
        Get an object and validate with the rosetta constraints.

        :param tab:
            The tab we need to validate.
        :param _object:
            The object to validate.

        :return:
        """
        obj = _object[tab]
        rosetta = self.get_tab(tab)

        errors = {}

        validations = Validations()

        for field, contexts in rosetta.items():
            for context, callbacks in contexts.items():
                for callback in callbacks:
                    for value in obj[field][context]:

                        # Init the key if not exists.
                        if field not in errors.keys():
                            errors[field] = []

                        # Setting up the val in the callbacks and pass it to the callback function.
                        callback['args']['val'] = value

                        results = getattr(validations, callback['func'])(**callback['args'])
                        results['value'] = value

                        # Appending the results.
                        errors[field].append(results)
        return errors
