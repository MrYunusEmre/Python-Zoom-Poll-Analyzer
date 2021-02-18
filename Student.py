class Student:
    attendancePoll=0
   
    def __init__(self, studentNo, firstName, lastName):
        self.ix = 0
        self.poll = []
        self.index = 1
        self.pollDict = {}
        self.totalAttendance = 0
        self.pollAnswers = []
        self.studentNo = studentNo
        self.firstName = firstName
        self.lastName = lastName

    def __initPollAnswer__(self, pollAnswers,students):
        maxIndex = self.index+1
        for student in students:
            if student.index > maxIndex :
                maxIndex = student.index
        self.index = maxIndex-1
        self.pollAnswers = pollAnswers
        self.pollDict[self.index] = self.pollAnswers
        self.index += 1

    def __initPollNameAndQuestionAndAnswer__(self, Poll):
        if Poll.pollName is not None:
            self.poll.insert(self.ix,Poll)
            self.ix += 1
