import unittest
from unittest.mock import patch
from repository.sample_repository import AbstractSampleRepository
from service.sample_service import SampleService

class MockSampleRepository(AbstractSampleRepository):
    def sample(self, message: str) -> dict:
        return {'message': 'success to create sample'}

class TestSampleService(unittest.TestCase):

    #パッチを当てる事で、モック化する
    @patch('repository.sample_repository.AbstractSampleRepository', MockSampleRepository)
    def test_sample_service_with_patch(self):
        mock_repository = MockSampleRepository()
        sample_service = SampleService(sample_repository=mock_repository)
        data = sample_service.sample(message="sample")
        expected_result = {'message': 'success to create sample'}
        self.assertEqual(data, expected_result)
