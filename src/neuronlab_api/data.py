"""NeuronLab Python API."""
import datetime
import json
import os
import requests
import time
from neuronlab_api.exceptions import (
    NeuronLabAPIException, NeuronLabInvalidDocumentException,
    NeuronLabBadRequestException, NeuronLabUserNotFoundException,
    NeuronLabInternalServerException,
)
from typing import List

class NeuronLabAPI:
    def __init__(self, neuronlab_auth_token: str, user_id: str):
        """__init__.

        Args:
            neuronlab_auth_token (str): Authentication token for Neuron Lab API.
            user_id (str): User id for Neuron Lab API.
        """
        self.neuronlab_auth_token = neuronlab_auth_token
        self.user_id = user_id
    
    def get_cnpj_dataset(self, list_cnpj: List[str]) -> dict:
        """Call Neuron Lab API to fetch dataset for a list of CNPJ.

        Args:
            list_cnpj (List[str]): List of cnpjs to be fetched.
        
        Returns:
            dict: Information available on Neuron Lab.
        
        Raises:
        """
        url = "https://trial-plataform-server.braveocean-99c2da72.brazilsouth.azurecontainerapps.io/api/integration/company"

        headers = {
            "Authorization": f"Bearer {self.neuronlab_auth_token}",
        }

        payload = {
            "data": ",".join(list_cnpj),
            "user_id": self.user_id,
        }

        for i in range(5):
            try:
                response = requests.get(url, headers=headers, params=payload)
                response.raise_for_status()
                response_json = response.json()
                # print(f"Code: {response.status_code}")
                if response.status_code == 200:
                    response_data = response_json['responses']
                    response_message = response_json['message']
                    if 'error' in response_data:
                        raise NeuronLabInvalidDocumentException(
                            message=response_message,
                            payload={'list_cnpj': list_cnpj}
                            )
                    return response_data
                elif response.status_code == 400:
                    raise NeuronLabBadRequestException(
                        message=response_message,
                        payload={'list_cnpj': list_cnpj}
                    )
                elif response.status_code == 403:
                    raise NeuronLabUserNotFoundException(
                        message=response_message,
                        payload={'list_cnpj': list_cnpj}
                    )
                elif response.status_code == 500:
                    raise NeuronLabInternalServerException(
                        message=response_message,
                        payload={'list_cnpj': list_cnpj}
                    )

                return response_data

            except Exception as e:
                print(f"Erro na requisição: {e}")
