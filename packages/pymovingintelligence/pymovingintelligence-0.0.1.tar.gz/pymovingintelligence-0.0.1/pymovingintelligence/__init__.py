"""Python 3 API wrapper for Moving Intelligence."""
import hashlib
import json
import logging
import secrets
import time
from typing import Optional

import requests
from requests.exceptions import HTTPError, RequestException, Timeout

from .errors import InvalidAuthError, InvalidPermissionsError

_LOGGER = logging.getLogger("pymovingintelligence")


class MovingIntelligence:
    """Class for communicating with the Moving Intelligence API."""

    def __init__(
        self,
        username: str = None,
        apikey: str = None,
    ):
        """Init module."""
        self._base_url = "https://api-app.movingintelligence.com"
        self._username = username
        self._apikey = apikey

    def get_objects(self) -> dict:
        """Get objects."""

        return self._request(
            "GET",
            endpoint="/v1/objects",
            log_msg="get objects",
        )

    def get_persons(self) -> dict:
        """Get persons."""

        return self._request(
            "GET",
            endpoint="/v1/persons",
            log_msg="get persons",
        )

    def get_trip_classifications(self) -> dict:
        """Get trip classifications."""

        return self._request(
            "GET",
            endpoint="/v1/tripclassifications",
            log_msg="get trip classifications",
        )

    def get_trip_periods(self) -> dict:
        """Get trip periods."""

        return self._request(
            "GET",
            endpoint="/v1/tripperiods",
            log_msg="get trip periods",
        )

    def get_odometer(self, object_id:str, date=None) -> dict:
        """Get odometer readings."""

        return self._request(
            "GET",
            endpoint=f"/v1/object/{object_id}/odometer",
            log_msg="get odometer for object",
            params=self._clean_request_params({"date": date}),
        )

    def get_person_trips(
        self, person_id: str, period: str, classifications, startdate=None, enddate=None
    ) -> dict:
        """Get trips for person."""

        return self._request(
            "GET",
            endpoint=f"/v1/person/{person_id}/trips",
            log_msg="get trips for person",
            params=self._clean_request_params(
                {
                    "startDate": startdate,
                    "endDate": enddate,
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

    def get_person_detailed_trips(
        self, person_id: str, period: str, classifications, startdate=None, enddate=None
    ) -> dict:
        """Get detailed trips for person."""

        return self._request(
            "GET",
            endpoint=f"/v1/person/{person_id}/detailedtrips",
            log_msg="get detailed trips for person",
            params=self._clean_request_params(
                {
                    "startDate": startdate,
                    "endDate": enddate,
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

    def get_object_trips(
        self, object_id: str, period: str, classifications, startdate=None, enddate=None
    ) -> dict:
        """Get trips for object."""

        return self._request(
            "GET",
            endpoint=f"/v1/object/{object_id}/trips",
            log_msg="get trips for object",
            params=self._clean_request_params(
                {
                    "startDate": startdate,
                    "endDate": enddate,
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

    def get_object_detailed_trips(
        self, object_id: str, period: str, classifications, startdate=None, enddate=None
    ) -> dict:
        """Get detailed trips for object."""

        return self._request(
            "GET",
            endpoint=f"/v1/object/{object_id}/detailedtrips",
            log_msg="get detailed trips for object",
            params=self._clean_request_params(
                {
                    "startDate": startdate,
                    "endDate": enddate,
                    "period": period,
                    "classifications": classifications,
                }
            ),
        )

    @staticmethod
    def _clean_request_params(params: dict) -> dict:
        """Create clean parameters."""
        clean_params = {}
        for key, value in params.items():
            if value is not None:
                clean_params[key] = str(value)

        return clean_params

    def _create_headers(self, endpoint: str, params: dict) -> str:
        """Return signature."""
        params_string = ""
        nonce = secrets.token_hex(10)
        timestamp = int(time.time())

        if params:
            params_string = "&".join([f"{key}={val}" for key, val in params.items()])
            endpoint = f"{endpoint}?{params_string}"

        sha512str = (
            "sha512 "
            + hashlib.sha512(
                str(
                    endpoint + self._username + nonce + str(timestamp) + self._apikey
                ).encode("utf-8")
            ).hexdigest()
        )
        headers = {
            "X-Mi-User": self._username,
            "X-Mi-Nonce": nonce,
            "X-Mi-Timestamp": str(timestamp),
            "X-Signature": sha512str,
        }

        return headers

    def _request(
        self,
        method: str,
        endpoint: str,
        log_msg: str,
        params: dict = None,
        body: dict = None,
    ) -> Optional[str]:
        """Makes a request to the movingintelligence API."""

        headers = self._create_headers(endpoint, params)
        url = f"{self._base_url}{endpoint}"

        _LOGGER.debug("Making request to %s endpoint to %s: url: %s, headers: %s, params: %s, body: %s" , endpoint, log_msg, url, headers, params, body
        )

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=body,
                timeout=10,
            )

            log_msg = response.json()

            _LOGGER.debug("Request response: %s: %s", response.status_code,log_msg)

            response.raise_for_status()
            return response.json()
        except HTTPError:
            json_payload = {}
            try:
                json_payload = response.json()
            except json.decoder.JSONDecodeError:
                _LOGGER.debug("Invalid JSON payload received")

            if response.status_code == 500:
                raise InvalidAuthError("Invalid credentials")

            if response.status_code == 401:
                status = json_payload.get("status")
                message = json_payload.get("message")
                if status == "UNAUTHORIZED":
                    raise InvalidPermissionsError(message)
                _LOGGER.error("Error while attempting to %s: %s %s", log_msg, response.status_code, json_payload)
        except Timeout:
            _LOGGER.error("Connection timed out while attempting to %s. Possible connectivity outage.", log_msg
            )
        except (RequestException, json.decoder.JSONDecodeError):
            _LOGGER.error("Error connecting while attempting to %s. %s", log_msg, response.status_code
            )

        return None
