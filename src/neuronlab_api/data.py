"""NeuronLab Python API."""

import os
from typing import List
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from neuronlab_api.exceptions import (
    NeuronLabInternalServerException,
    NeuronLabBadRequestException,
    NeuronLabUserNotFoundException,
    NeuronLabInvalidArgs)


class NeuronLabAPI:
    def __init__(
            self, neuronlab_auth_token: str, url: str,
            max_tries: int = 5, proxy: str = None):
        """__init__.

        Args:
            neuronlab_auth_token (str): Authentication token for Neuron Lab API.
            url (str): Neuron Lab API URL.
            max_tries (int): Limit of fetch attempts.
        """
        self._neuronlab_auth_token = neuronlab_auth_token
        self._url = url

        # Mount session
        HTTP_BACKOFF_FACTOR = 0.2
        retry_strategy = Retry(
            total=max_tries, backoff_factor=HTTP_BACKOFF_FACTOR,
            raise_on_status=False)

        if proxy is None:
            proxy = os.getenv("SERASA_API_PROXY")
        self._proxy = proxy

        self._session = requests.Session()
        self._session.mount(self._url, HTTPAdapter(max_retries=retry_strategy))
        self._session.proxies = {"http": self._proxy, "https": self._proxy}

    def get_cnpj_dataset(self, cnpjs: List[str]):
        """Call Neuron Lab API to fetch data for a list of CNPJ.

        Args:
            cnpjs (List[str]):
                A list of cnpj to be fetch.

        Returns:
            list:
                Dataset containing query information and a list of query results for CNPJ.

        Raises:
            NeuronLabAPIException
        """

        return self._get_document_dataset("cnpj", cnpjs)

    def get_cpf_dataset(self, cpfs: List[str]):
        """Call Neuron Lab API to fetch data for a list of CPF.

        Args:
            cnpjs (List[str]):
                A list of cpf to be fetch.

        Returns:
            list:
                Dataset containing query information and a list of query results for CPF.

        Raises:
            NeuronLabAPIException
        """

        return self._get_document_dataset("cpf", cpfs)

    def _get_document_dataset(self, document_type: str, documents: List[str]) -> dict:
        """Call Neuron Lab API to fetch dataset for a list of document data.

        Args:
            document_type (str):
                The type of document to be fetch, cpf or cnpj.

            documents (List[str):
                A list of document to be enriched.

        Returns:
            dict:
                Dataset containing query information and a list of query results.

        Raises:
            NeuronLabAPIException
        """

        if len(documents) == 0:
            raise NeuronLabInvalidArgs(
                message="Empty document list, at least one document expected")

        headers = {"Authorization": f"Bearer {self._neuronlab_auth_token}"}

        comma_separated_documents = ",".join(documents)
        payload = {}
        payload["{}s".format(document_type)] = comma_separated_documents

        try:
            document_endpoint = "{}/api/{}/search-{}s".format(
                self._url, document_type, document_type)
            response = self._session.get(
                document_endpoint, headers=headers, params=payload)
            response.raise_for_status()
            response_json = response.json()

            return response_json["data"]

        except requests.exceptions.HTTPError as e:
            err_response = e.response
            err_response_json = err_response.json()

            response_message = "Unknown error"
            if "error" in err_response_json and "message" in err_response_json["error"]:
                response_message = err_response_json["error"]["message"]

            if response.status_code == 400:
                raise NeuronLabBadRequestException(
                    message=response_message, payload=payload)
            elif response.status_code == 403:
                raise NeuronLabUserNotFoundException(
                    message=response_message, payload=payload)
            else:
                raise NeuronLabInternalServerException(
                    message=response_message, payload=payload)
