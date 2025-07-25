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

    def test__fetch_one_cnpj_with_score(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api\
                    .with_score()\
                    .get_cnpj_dataset(cnpjs=CNPJ_TEST_INPUT[:1])
        self.assertEqual(response["totalCNPJs"], 1)

        # test if negative data is present and populated
        print('cnpj', response)
        cnpj = response["fetchResults"][0]
        negative_data = cnpj.get("negative_data")
        self.assertIsNotNone(negative_data)

        pefin = negative_data.get("pefin")
        self.assertIsNotNone(pefin)
        pefin_summary = pefin.get("summary")
        self.assertIsNotNone(pefin_summary)
        self.assertEqual(pefin_summary.get("balance"), 3124.56)
        self.assertEqual(pefin_summary.get("count"), 2)

    def test__fetch_one_cpf_with_score(self):
        neuronlab_api = NeuronLabAPI(
            neuronlab_auth_token=NEURONLAB_AUTH_TOKEN,
            url=NEURONLAB_URL)

        response = neuronlab_api\
                    .with_score()\
                    .get_cpf_dataset(cpfs=CPF_TEST_INPUT)

        cpf = response["RFInfo"][0]
        negative_data = cpf.get("negative_data")
        self.assertIsNotNone(negative_data)

        refin = negative_data.get("refin")
        self.assertIsNotNone(refin)
        refin_summary = refin.get("summary")
        self.assertIsNotNone(refin_summary)
        self.assertEqual(refin_summary.get("balance"), 324.22)
        self.assertEqual(refin_summary.get("count"), 1)
