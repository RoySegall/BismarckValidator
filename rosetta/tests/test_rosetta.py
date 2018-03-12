import os
import json
import unittest
from unittest import TestCase
from ..rosetta import Rosetta


class TestsRosetta(TestCase):

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
        assert 'currency' in tab.keys()
        assert list(tab['currency'].keys()) == self._get_rosetta().contexts

    def _test_validate_object(self):
        # todo: fix.
        asset = open(os.getcwd() + "/pytest_assets/cash_object_1.json")
        errors = self._get_rosetta().validate_object('cash', json.load(asset))

        instrument = errors['instrument_id']
        assert {'result': False, 'msg': 'Value is not in the correct range.', 'value': 50} in instrument
        assert {'result': True, 'value': 1001} in instrument
        assert {'result': False, 'msg': 'Value is not in the correct range.', 'value': 9999991} in instrument
        assert {'result': True, 'value': '25/06/1989'} in instrument
        assert {'result': True, 'value': '14/02/2016'} in instrument
        assert {'result': False, 'msg': 'Incorrect date format, should be DD/MM/YYYY', 'value': '02/14/1999'} in \
            instrument


if __name__ == "__main__":
    unittest.main()
