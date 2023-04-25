import csv
import os
import time
import urllib.request
from dataclasses import dataclass, field

import pandas as pd
from dotenv import load_dotenv
import requests
from pathlib import Path
from app.loaders.toml_loader import TomlLoader
from typing import ClassVar

fec_fields = TomlLoader('fec')

Categories = fec_fields.config['FEC-CATEGORIES']
Candidates = fec_fields.config['CANDIDATE-DETAILS']
FinanceDetails = fec_fields.config['SPENDER-RECIPIENT-DETAILS']

load_dotenv(Path(__file__).parent.parent.parent / '.env')


# FEC Client class with methods for making requests to the FEC API
@dataclass
class FECClient:
    category: str
    category_url: str = field(init=False)
    params: dict = field(init=False)
    pages: int = field(init=False)
    __base_url = fec_fields.config['FEC_API_URL']
    __headers = {
        'Content-Type': 'application/json'
    }

    def fetch(self, params: dict, page: int = None):
        _params = self.params
        _params.update(params)

        _category_url = f"{self.__base_url}/{self.category_url}"
        if page:
            _category_url = f"{_category_url}?page={page}"
        response = requests.get(
            _category_url,
            params={
                **_params
            },
            headers=self.__headers
        )
        return response.json()

    def get_pages(self, response: dict):
        self.pages = response['pagination']['pages']
        return self.pages

    def loop_through_pages(self, response: dict):
        _data = response['results']
        for pg in range(1, self.pages + 1):
            _response = self.fetch(params=self.params, page=pg)
            _data.extend(_response['results'])
        return _data

    def __post_init__(self):
        self.params = {'api_key': os.environ['FEC_API_KEY']}
        self.category_url = Categories[self.category]


@dataclass
class FECCandidate:
    query: str
    name: str = field(init=False)
    _id: str = None
    response: dict = field(init=False)
    filings: dict = field(init=False)
    filing_csvs: list = field(init=False)
    contributions: dict = field(init=False)

    def split_name(self):
        _split = self.query.split(' ')
        if len(_split) == 2:
            self.name = f"{_split[1]}, {_split[0]}"
        else:
            self.name = self.query
        return

    def fetch(self):
        self.split_name()
        _client = FECClient('candidate')
        _client.params.update({'q': self.name})
        self.response = FECClient('candidate').fetch(_client.params)
        return self

    def print_candidate_options(self):
        _results = self.response['results']
        for result in _results:
            if result['office_sought'] == 'H':
                _office = 'US House'
            elif result['office_sought'] == 'S':
                _office = 'US Senate'
            else:
                _office = result['office_sought']

            print(f"""   
    ======= Candidate: {result['name'].title()} =======
        Option: {_results.index(result)}
        ID: {result['id']}
        Office: {_office}
            """)

    def choose_candidate_prompt(self):

        if len(self.response['results']) > 1:
            _choice = input('Choose a candidate: ')
            _result = self.response['results'][int(_choice)]

        else:
            _choice = 0
            _result = self.response['results'][0]

        self._id = _result['id']
        return _choice

    def get_filings(self):
        _client = FECClient('candidate-filings')
        _client.category_url = _client.category_url.format(candidate_id=self._id)
        self.filings = _client.fetch(_client.params)
        return self.filings

    def get_contributions(self):
        _client = FECClient('contributions')
        _client.params.update({'committee_id': self._id})
        self.contributions = _client.fetch(_client.params)
        return self.contributions

    def __post_init__(self):
        self.fetch()
        self.print_candidate_options()
        self.choose_candidate_prompt()
        self.get_filings()
        self.get_contributions()


@dataclass
class FECCommittee:
    _id: FECCandidate._id
    _client = FECClient('committee')

    def __post_init__(self):
        self._client.category_url = self._client.category_url.format(committee_id=self._id)
        self.response = self._client.fetch(self._client.params)


jordan = FECCandidate('James Jordan')
# jordan_committees = FECCommittee(jordan.candidate_id)

client = FECClient('contributions-subid')
client.params.update({'candidate_id': jordan._id,
                      'cycle': 2022})
result = client.fetch(client.params)
pages = client.get_pages(result)
data = client.loop_through_pages(result)

# filing_csvs = []
# for filing in filings:
#     f = requests.get(filing)
#     c = f.iter_lines()
#     _csv = csv.reader(c)
#     filing_csvs.append(_csv)
#     time.sleep(5)

