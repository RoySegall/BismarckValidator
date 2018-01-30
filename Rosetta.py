import yaml
import sys


class Rosetta(object):

    def wrapper_file(self, folder):
        """
        Specifying the file which holds the sub files.

        :param folder:

        :return:
        """

        # Open the file.
        items = open(folder)

        # Iterate over the files.
        rosetta = []

        for item in items:
            stream = open(folder + "/" + item, "r")
            content = yaml.load(stream)

            # Todo: strip out data we don't need.
            rosetta.append(content)

        return rosetta
