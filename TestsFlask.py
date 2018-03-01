import requests
import os


class TestsFlask(object):
    """
    Testing the flask integration.
    """

    def test_index(self):
        """
        Testing that the index route returns a message with 404 status code.

        :return:
        """
        r = requests.get('http://localhost:8080')
        assert r.json() == {'message': 'woops... It seems that you got the wrong place'}
        assert r.status_code == 404

    def test_upload(self):
        """
        Making sure that the upload route is supported for now.

        :return:
        """
        files = {'upload_file': open('pytest_assets/Financial_Sample.xlsx', 'rb')}
        r = requests.post('http://localhost:8080/upload', files=files)
        assert r.json() == {'file': os.getcwd() + '/uploads/Financial_Sample.xlsx'}
