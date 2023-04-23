import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
import requests
from pathlib import Path
from app.loaders.toml_loader import TomlLoader

fec_fields = TomlLoader('fec')

Categories = fec_fields.config['FEC-CATEGORIES']
Candidates = fec_fields.config['CANDIDATE-DETAILS']
FinanceDetails = fec_fields.config['SPENDER-RECIPIENT-DETAILS']

load_dotenv(Path(__file__).parent.parent.parent / '.env')


# FEC Client class with methods for making requests to the FEC API
@dataclass
class FECClient:
    category: str
    __base_url = fec_fields.config['FEC_API_URL']
    __headers = {
        'Content-Type': 'application/json'
    }

    def get_response(self, query):
        # Value in fec_fields.config if key == category
        try:
            _category = Categories[self.category]
        except KeyError:
            raise KeyError(f"Category must be one of {Categories.keys()}")

        response = requests.get(
            f"\
            {self.__base_url}/{_category}/?api_key={os.environ['FEC_API_KEY']}&q={query}",
            headers=self.__headers
        )
        return response.json()


@dataclass
class FECCandidate:
    query: str
    name: str = field(init=False)
    response: dict = field(init=False)
    committee_id: str = field(init=False)

    def split_name(self):
        _split = self.query.split(' ')
        if len(_split) == 2:
            self.name = f"{_split[1]}, {_split[0]}"
        else:
            self.name = self.query
        return

    def fetch(self):
        self.split_name()
        self.response = FECClient('candidate').get_response(f"{self.name}")
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

        self.committee_id = _result['id']
        return _choice

    def fetch_contributions(self):
        _response = FECClient('schedules/schedule_a').get_response(f"{self.committee_id}")
        return _response

    def __post_init__(self):
        self.fetch()
        self.print_candidate_options()
        self.choose_candidate_prompt()


jordan = FECCandidate('James Jordan')
