from .question import InsperaQuestion

class InsperaCandidate:
    def __init__(self, data):
        self.data = data  # ext_inspera_candidates -> idx -> result

    def score(self):
        return self.data['score']
    
    def id(self):
        return self.data['ext_inspera_candidateId']

    def start_end(self):
        start = self.data['ext_inspera_startTime']
        end = self.data['ext_inspera_endTime']
        return '{}-{}'.format(start, end)

    def questions(self):
        return [InsperaQuestion(q) for q in self.data['ext_inspera_questions']]
