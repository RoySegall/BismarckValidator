from Validations import Validations


class TestsPlugins(object):

    def test_plus(self):
        assert 1 + 1 == 2

    def test_not_null(self):
        validators = Validations()
        assert validators.not_null(val='').items() <= ({'result': False, 'msg': "Invalid empty string value"}).items()
        assert validators.not_null(val=None).items() <= ({'result': False, 'msg': "Invalid 'None' value"}).items()
