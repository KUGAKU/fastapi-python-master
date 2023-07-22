import unittest
from unittest.mock import patch
from business_logic.sample_service import SampleService
from data_access.sample_repository import AbstractSampleRepository


class MockSampleRepository(AbstractSampleRepository):
    def sample(self, message: str) -> dict:
        return {"message": "success to create sample"}


class TestSampleService(unittest.TestCase):
    # パッチを当てる事で、モック化する
    @patch(
        "data_access.sample_repository.AbstractSampleRepository", MockSampleRepository
    )
    def test_sample_service_with_patch(self):
        mock_repository = MockSampleRepository()
        sample_service = SampleService(sample_repository=mock_repository)
        data = sample_service.sample(message="sample")
        expected_result = {"message": "success to create sample"}
        self.assertEqual(data, expected_result)
