import requests
import os
import unittest
from unittest import TestCase


class TestsFlask(TestCase):
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

    def test_process_files(self):
        """
        Testing file process.

        :return:
        """
        files = {'upload_file': open('pytest_assets/513026484_gsum_0317.xlsx', 'rb')}
        r = requests.post('http://localhost:8080/upload', files=files)
        file_path = dict(r.json())['file']

        # Testing errors.
        self.assertEqual(requests.post('http://localhost:8080/process_files').json(),
                         {'error': 'The files property is empty.'})

        data = {'files': [file_path]}
        self.assertEqual(requests.post('http://localhost:8080/process_files', data=data).json(),
                         {'error': 'You need to provide the pusher room.'})

        # Testing the results of the endpoint.
        data['room'] = 'testing'
        response = dict(requests.post('http://localhost:8080/process_files', data=data).json())['data']
        self.assertTrue('id' in response.keys())
        self.assertTrue('513026484_gsum_0317.xlsx' in response['results'].keys())

    def test_process_files_results(self):
        """
        Testing the process files.

        :return:
        """

        # Upload a file.
        files = {'upload_file': open('pytest_assets/513026484_gsum_0317.xlsx', 'rb')}
        r = requests.post('http://localhost:8080/upload', files=files)

        # Prepare payload and send data.
        data = {
            'files': [dict(r.json())['file']],
            'room': 'testing',
        }
        response = dict(requests.post('http://localhost:8080/process_files', data=data).json())['data']

        # Making sure the data are the same.
        get_response = dict(requests.get('http://localhost:8080/process_files/' + response['id']).json())
        self.assertEqual(get_response['results'], response['results'])


if __name__ == "__main__":
    unittest.main()
