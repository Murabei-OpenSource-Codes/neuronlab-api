"""Test Neuron Lab API."""
import os
import unittest
from neuronlab_api.data import NeuronLabAPI

NEURONLAB_AUTH_TOKEN = "f32x1v3mYTI7HzPwjqsq5FyINwNhxRugFHf6A8z61dE"
NEURONLAB_USER_ID = "658a37f0d3f81bb1b7dc526a"
list_cnpj = ["87654321000199", "94007614000149"]

class TestNeuronLabAPI(unittest.TestCase):
    """Test Neuron Lab api."""

    def test__ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            user_id=NEURONLAB_USER_ID,
        )
        neuronlab_api.get_cnpj_dataset(list_cnpj=list_cnpj)