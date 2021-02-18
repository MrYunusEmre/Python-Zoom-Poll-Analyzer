class Poll:
    def __init__(self, pollName, QuestionAndAnswers):
        self.pollName = pollName
        self.QuestionAndAnswers = QuestionAndAnswers

    def __addAllAnswers__(self,Question,Answer):
        for questionAndAnswer in self.QuestionAndAnswers:
            if questionAndAnswer.get("Q").find(Question) != -1:
                if len(Answer)>0:
                    if Answer[len(Answer)-1]==',':
                        Answer = Answer[0:-1]
                    questionAndAnswer.get("U").add(Answer)
