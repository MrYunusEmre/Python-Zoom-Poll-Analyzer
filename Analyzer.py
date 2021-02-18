from Poll import *

def __findAttendancePolls__(students, question):  # answer is not important, if student is answered
    for student in students:  # attendance poll, increment attendances.
        for key in student.pollDict.copy():
            print(student.pollDict.get(key))
            if student.pollDict.get(key).find(question) != -1:
                print("sa")
                student.pollDict.pop(key)
                student.totalAttendance += 1

def __changeAllKeys__(oldkey,newkey,students):
    for student in students:
        for key in student.pollDict.copy():
            if key == oldkey:
                student.pollDict[newkey] = student.pollDict[oldkey]
                del student.pollDict[oldkey]

def __findPollsAndChangeKey__(students, polls):

    for poll in polls:
        print(poll.pollName)


    global questionCount, pollName
    for student in students:  # get students one by one
        for studentPoll in student.pollDict.copy():  # get this students polls ans answers
            for poll in polls:                          # get all polls one by one
                pollName = poll.pollName
                if type(studentPoll) is not int :
                    continue
                questionCount = len(poll.QuestionAndAnswers)
                count = 0
                for questionAndAnswers in poll.QuestionAndAnswers:  # get all questions in that poll one by one
                    if student.pollDict.get(studentPoll).find(f'{questionAndAnswers.get("Q")}') != -1:
                        count += 1
                if count == questionCount:
                    U = 'U§'
                    for key in student.pollDict:
                        if key == pollName:
                            for i in poll.QuestionAndAnswers:
                                i[U] = i['U']
                            pollName += '§'
                            U += '§'
                    __changeAllKeys__(studentPoll,pollName,students)
                    break

def __findStudentAnswers__(students, polls):
    global firstQuestion , answer , answerStartIndex , answerFinishIndex
    for student in students:
        for stdPoll in student.pollDict:                        # POLL1 POLL1* POLL3
            QuestionAndAnswer = []
            index = 0
            tempPollName = stdPoll
            if type(tempPollName) is int :
                tempPollName = "UNNAMED"
            while tempPollName[len(tempPollName) - 1] == '§':
                tempPollName = tempPollName[0:len(tempPollName) - 1]
            for poll in polls:                                  # POLL1 POLL3
                if poll.pollName == tempPollName :
                    allText = student.pollDict.get(stdPoll)
                    questions_arr = list(reversed(poll.QuestionAndAnswers))
                    i=0
                    while i < len(questions_arr) :
                        if allText.find(questions_arr[i].get('Q')) != -1 :                         # ilk soruyu buldu
                            firstQuestion=questions_arr[i].get('Q')
                            answerStartIndex = allText.find(questions_arr[i].get('Q')) + len(questions_arr[i].get('Q')) + 1
                            j = i + 1
                            isfind = 0
                            while j < len(questions_arr) :
                                if allText.find(questions_arr[j].get('Q')) != -1 :
                                    isfind = 1
                                    answerFinishIndex = allText.find(questions_arr[j].get('Q')) - 1
                                    answer = allText[answerStartIndex:answerFinishIndex]
                                    break
                                else :
                                    j+=1
                            if isfind == 0 :
                                answer = allText[answerStartIndex:-1]
                            isCorrect = 0
                            if answer == questions_arr[i].get('A'):
                                isCorrect = 1
                            answer_arr = answer.split(";")
                            for ans in answer_arr:
                                poll.__addAllAnswers__(firstQuestion, ans)
                            questionanswer = {
                                'Q': firstQuestion,
                                'A': answer_arr,
                                'C': isCorrect
                            }
                            QuestionAndAnswer.insert(index,questionanswer)
                            index += 1
                        i+=1
            newPoll = Poll(stdPoll, QuestionAndAnswer)
            student.__initPollNameAndQuestionAndAnswer__(newPoll)
