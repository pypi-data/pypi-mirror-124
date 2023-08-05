from .cleaner import clean_all

class InsperaQuestion:
    def __init__(self, question):
        # question path: src->idx->result->ext_inspera_questions->idx
        self.q = question

    def responses(self):
        return self.q['ext_inspera_candidateResponses']
        
    def clean_response(self):
        responses = [res['ext_inspera_response'] for res in self.responses() if res['ext_inspera_response'] != None]
        return clean_all(' '.join(responses))

    def manual_scores(self, field):
        scores = self.q['ext_inspera_manualScores']
        if scores is None:
            return None
        scores = [score['ext_inspera_' + field] for score in scores]
        if len(scores) != 1:
            scores = ','.join(scores)
        else:
            scores = scores[0]
        return scores

    def grading(self):
        return self.manual_scores('manualScore')

    def grader(self):
        return self.manual_scores('gradingTeacherName')

    def question_title(self):
        return self.q['ext_inspera_questionTitle']

    def question_num(self):
        return self.q['ext_inspera_questionNumber']

    def max_score(self):
        return self.q['ext_inspera_maxQuestionScore']

    def duration(self):
        return self.q['ext_inspera_durationSeconds']
        
    def make_row(self):
        return [
            self.question_num(),
            self.question_title(),
            self.responses(),
            self.clean_response(),
            self.grading(),
            self.grader(),
            self.max_score(),
            self.duration()
        ]

    def __str__(self):
        q_id, res, grade, max_score, dur = self.make_row()
        grade_detailed = '{} (max score/weight: {})'.format(grade, max_score)
        
        return 'Question:\t{}\nAnswer:\t{}\nGrading:\t{}\nDuration:\t{}'.format(
            q_id,
            res,
            grade_detailed,
            dur
        )