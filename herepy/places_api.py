#!/usr/bin/env python

from __future__ import division

import sys
import json
import requests

from herepy.here_api import HEREApi
from herepy.utils import Utils
from herepy.error import HEREError
from herepy.models import PlacesResponse

class PlacesApi(HEREApi):
    """A python interface into the HERE Places (Search) API"""

    def __init__(self,
                 app_id=None,
                 app_code=None,
                 timeout=None):
        """Return a PlacesApi instance.
        Args:
          app_id (string): App Id taken from HERE Developer Portal.
          app_code (string): App Code taken from HERE Developer Portal.
          timeout (int): Timeout limit for requests.
        """

        super(PlacesApi, self).__init__(app_id, app_code, timeout)
        self._base_url = 'https://places.cit.api.here.com/places/v1/discover/search'

    def __get(self, data):
        url = Utils.build_url(self._base_url, extra_params=data)
        response = requests.get(url, timeout=self._timeout)
        json_data = json.loads(response.content.decode('utf8'))
        if json_data.get('results') != None:
            return PlacesResponse.new_from_jsondict(json_data)
        else:
            return HEREError(json_data.get('message', 'Error occured on ' + sys._getframe(1).f_code.co_name))

    def onebox_search(self, coordinates, query):
        """Request a list of nearby places based on a query string
        Args:
          coordinates (array): array including latitude and longitude in order.
          query (string): search term.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'q':  query,
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)

    def places_at(self, coordinates):
        """Request a list of popular places around a location
        Args:
          coordinates (array): array including latitude and longitude in order.
        Returns:
          PlacesResponse instance or HEREError"""

        data = {'at': str.format('{0},{1}', coordinates[0], coordinates[1]),
                'app_id': self._app_id,
                'app_code': self._app_code}
        return self.__get(data)