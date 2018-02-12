import yaml
import os

from Validations import Validations


class Rosetta(object):

    # The folder of the yml files.
    folder = ''

    # Holds the list of contexts.
    contexts = []

    # Holds the list of contexts.
    rosetta = {}

    def __init__(self, folder, contexts=None):
        if contexts is None:
            contexts = ['in_israel', 'not_in_israel']

        self.folder = folder
        self.contexts = contexts

    def get_constraints(self):
        """
        Specifying the file which holds the sub files.

        :return:
            All the constraints.
        """

        for filename in os.listdir(self.folder):
            if not filename.endswith(".yml"):
                continue

            stream = open(self.folder + "/" + filename)
            yml_file = yaml.load(stream)

            self.rosetta[filename.split(".")[0]] = yml_file['fields']

        return self.rosetta

    def get_tab(self, tab):
        """
        Get info for tab.

        :param tab:
            The tab. i.e cache.

        :return:
        """
        if self.rosetta == {}:
            self.get_constraints()

        return self.rosetta[tab]

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
