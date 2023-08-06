import os
import uuid
from logging import Logger, LoggerAdapter
from typing import Union, Dict, List

from ..default_logger import DefaultLogger
from .athena_http_session import AthenaHttpSession


class AthenaPrototype:
    """
    Interface to access the prototype of the prediction service.
    """

    def __init__(
        self,
        username: str = "",
        password: str = "",
        endpoint="http://prediction.dev.paretos.io",
        logger: Union[Logger, LoggerAdapter] = None,
    ) -> None:
        """
        :param username: username for prediction service authentication
        :param password: password for prediction service authentication
        :param endpoint: optional, service endpoint
        :param logger: optional, can be used for debugging and logging
        """

        self.__session = AthenaHttpSession(
            api_url=endpoint,
            username=username,
            password=password,
            logger=logger or DefaultLogger(stream=open(os.devnull, "w")),
        )

    def predict(self, model: str, data: List[Dict[str, List[float]]]):
        """
        Uses the specified model to create a prediction from the provided data.
        :param model: name of the model
        :param data: the raw input data as lists of float (numpy etc. not supported)
        """
        request_data = {"model_id": model,
                        "predict_data": [
                            {
                                "id": str(uuid.uuid4()),
                                "prediction_data": [
                                    {
                                        "name": feature_name,
                                        "value": feature_value
                                    } for feature_name, feature_value in
                                    requested_prediction.items()
                                ]
                            } for requested_prediction in data
                        ]}

        response_data = self.__session.request(
            path="/paretos/predict",
            contains_sensitive_data=False,
            data=request_data,
            method="POST",
        )

        return response_data
