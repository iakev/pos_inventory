from .test_setup import TestSetUp

class TestModels(TestSetUp):
    def test_suppler_can_be_created(self):
        res = self.client.post(self.business_url)
        assert "Authentication credentials were not provided." in str(res.content)