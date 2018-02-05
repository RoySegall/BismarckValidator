import json

from Rosetta import Rosetta
import os


class TestsRosetta(object):

    def _get_rosetta(self):
        """
        Helper function to get the rosetta stone.

        :return:
        """
        return Rosetta(os.getcwd() + "/validations_templates")

    def test_list_of_files(self):
        """
        Testing the rosetta return the list of files.

        :return:
        """
        constraints = self._get_rosetta().get_constraints()
        assert ['cash'] == list(constraints.keys())

    def test_contexts(self):
        """
        Testing contexts issue methods.

        :return:
        """
        tab = self._get_rosetta().get_tab('cash')
        assert 'instrument_id' in tab.keys()
        assert list(tab['instrument_id'].keys()) == self._get_rosetta().contexts

    def test_validate_object(self):
        asset = open(os.getcwd() + "/pytest_assets/cash_object_1.json")
        results = self._get_rosetta().validate_object(json.load(asset))
        assert results == {}
