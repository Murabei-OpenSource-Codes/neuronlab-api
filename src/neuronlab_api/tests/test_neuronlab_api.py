"""Test Neuron Lab API."""

import unittest
import os
from neuronlab_api.data import NeuronLabAPI

NEURONLAB_AUTH_TOKEN = os.getenv("NEURONLAB_AUTH_TOKEN")
NEURONLAB_URL = os.getenv("NEURONLAB_URL")
CNPJ_TEST_INPUT = os.getenv("CNPJ_TEST_INPUT").split(",")
CPF_TEST_INPUT = os.getenv("CPF_TEST_INPUT").split(",")


class TestNeuronLabAPI(unittest.TestCase):
    """Test Neuron Lab api."""

    def test__fetch_cnpj_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api.get_cnpj_dataset(cnpjs=CNPJ_TEST_INPUT)
        self.assertEqual(response["totalCNPJs"], len(CNPJ_TEST_INPUT))

    def test__fetch_cpf_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api.get_cpf_dataset(cpfs=CNPJ_TEST_INPUT)
        self.assertEqual(response["totalCPFs"], len(CNPJ_TEST_INPUT))

    def test__fetch_one_cnpj_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api.get_cnpj_dataset(cnpjs=CNPJ_TEST_INPUT[:1])
        self.assertEqual(response["totalCNPJs"], 1)

    def test__fetch_one_cpf_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api.get_cpf_dataset(cpfs=CNPJ_TEST_INPUT[:1])
        self.assertEqual(response["totalCPFs"], 1)
