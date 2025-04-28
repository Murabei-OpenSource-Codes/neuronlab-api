"""Test Neuron Lab API."""

import unittest
import configparser
import os
from neuronlab_api.data import NeuronLabAPI

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read("{}/test_parameters.ini".format(dir_path))

NEURONLAB_AUTH_TOKEN = config["DEFAULT"]["NEURONLAB_AUTH_TOKEN"].strip()
NEURONLAB_URL = config["DEFAULT"]["NEURONLAB_URL"].strip()
CNPJ_TEST_INPUT = config["DEFAULT"]["CNPJ_TEST_INPUT"].strip().split(",")
CPF_TEST_INPUT = config["DEFAULT"]["CPF_TEST_INPUT"].strip().split(",")


class TestNeuronLabAPI(unittest.TestCase):
    """Test Neuron Lab api."""

    def test__fetch_cnpj_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL,
        )

        response = neuronlab_api.get_cnpj_dataset(cnpjs=CNPJ_TEST_INPUT)
        self.assertEqual(response["totalCNPJs"], len(CNPJ_TEST_INPUT))

    def test__fetch_cpf_ok(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL,
        )

        response = neuronlab_api.get_cpf_dataset(cpfs=CNPJ_TEST_INPUT)
        self.assertEqual(response["totalCPFs"], len(CNPJ_TEST_INPUT))
