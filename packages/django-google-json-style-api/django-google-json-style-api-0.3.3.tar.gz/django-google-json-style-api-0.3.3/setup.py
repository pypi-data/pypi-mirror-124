# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_google_json_style_api']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.0,<4.0.0', 'pydantic>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'django-google-json-style-api',
    'version': '0.3.3',
    'description': 'Implementation of Google JSON Style Guide for Django',
    'long_description': '[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![autoflake: on](https://img.shields.io/badge/autoflake-on-brightgreen)](https://github.com/myint/autoflake)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/django-google-json-style-api)](https://pypi.org/project/django-google-json-style-api/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-google-json-style-api)](https://pypi.org/project/django-google-json-style-api/)\n\n---\n\n# Django Google JSON Style API\n\nImplementation of Google JSON Style Guide for Django\n\n## Install\n\n    pip install django-google-json-style-api\n\n## Example\n\n    # models.py\n\n    from django.db import models\n\n\n    class City(models.Model):\n        city_name = models.TextField()\n\n    # schemas.py\n\n    from typing import List\n\n    from pydantic import BaseModel\n\n    from django_google_json_style_api.base import CamelModel\n    from django_google_json_style_api.responses import BaseResponseData, BaseSuccessResponse\n\n\n    class AddCityRequest(CamelModel):\n        city_name: str\n\n\n    class AddCitiesRequest(BaseModel):\n        cities: List[AddCityRequest]\n\n\n    class CityDataItem(CamelModel):\n        id: int\n        city_name: str\n\n\n    class CityResponseData(BaseResponseData[CityDataItem]):\n        ...\n\n\n    class CityResponse(BaseSuccessResponse[CityResponseData]):\n        __kind__ = "City"\n\n    # urls.py\n\n    from django.urls import path\n    from django.views.decorators import csrf\n\n    from . import views\n\n    urlpatterns = [\n        path(\n            "add/",\n            csrf.csrf_exempt(views.AddCitiesView.as_view()),\n            name="add-cities",\n        ),\n    ]\n\n\n    # views.py\n\n    from django_google_json_style_api.decorators import process_json_response\n\n    from django.utils.decorators import method_decorator\n    from django.views import View\n\n    from .models import City\n    from .schemas import AddCitiesRequest, CityResponse, CityDataItem\n\n\n    @method_decorator(process_json_response(api_version=\'1.1\'), name="dispatch")\n    class AddCitiesView(View):\n        def post(self, request):\n            cities = AddCitiesRequest.parse_raw(request.body).cities\n            response_items = []\n            for add_city_request in cities:\n                city = City.objects.create(**add_city_request.dict())\n                city_data_item = CityDataItem(\n                    id=city.id,\n                    city_name=city.city_name\n                )\n                response_items.append(city_data_item)\n            return CityResponse.make_from(\n                request,\n                total_items=City.objects.count(),\n                items=response_items,\n            )\n\n    # tests.py\n\n    from django.test import TestCase\n    from django.urls import reverse\n\n\n    class TestCities(TestCase):\n\n        def test_add_cities(self):\n            url = reverse(\'add-cities\')\n            data = {\n                "cities": [\n                    {"cityName": "Tyumen"},\n                    {"cityName": "Moscow"},\n                ]\n            }\n            response = self.client.post(url, data, content_type="application/json")\n            response_json = response.json()\n            self.assertDictEqual(\n                response_json,\n                {\n                    \'apiVersion\': \'1.1\',\n                    "data": {\n                        \'currentItemCount\': 2,\n                        "items": [\n                            {\n                                "id": 1,\n                                "cityName": "Tyumen",\n                            },\n                            {\n                                "id": 2,\n                                "cityName": "Moscow",\n                            },\n                        ],\n                        \'itemsPerPage\': 100,\n                        \'kind\': \'City\',\n                        \'startIndex\': 0,\n                        \'totalItems\': 2,\n                    },\n                }\n            )\n\n\n## TODO:\n\nDocs, tests\n',
    'author': 'Andrey Zevakin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/azevakin/django-google-json-style-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
