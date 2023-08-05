import json
from .candidate import InsperaCandidate

class InsperaReader:
    def __init__(self, file):
        self.json_data = None
        self.parsed_json = {}
        with open(file, 'r', encoding='utf8') as f:
            self.json_data = json.load(f)

    def candidates(self):
        raw = self.json_data['ext_inspera_candidates']
        return [InsperaCandidate(c['result']) for c in raw]

    def __str__(self):
        return 'Inspera data for the course: {}'.format(self.json_data['ext_inspera_assessmentRunTitle'])
