import unittest
from repository.sample_repository import SampleRepository


class TestSampleRepository(unittest.TestCase):

    def test_sample_repository(self):
        sample_repo = SampleRepository()
        response = sample_repo.sample()
        expected_result = {"message": "sample"}
        assert response == expected_result
