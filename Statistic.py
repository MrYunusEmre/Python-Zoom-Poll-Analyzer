def __answerCounts__(students,polls):
    for poll in polls:
        for questionAndAnswer in poll.QuestionAndAnswers :
            for keys in questionAndAnswer.copy() :
                if keys.find('U') != -1:
                    j = 0
                    answerArray = []
                    for i in questionAndAnswer.get(keys):
                        i_dict = { i : 0 }
                        answerArray.insert(j,i_dict)
                        j+=1
                    del questionAndAnswer[keys]
                    questionAndAnswer[keys] = answerArray

    for poll in polls:
        for questionAndAnswer in poll.QuestionAndAnswers:
            for keys in questionAndAnswer:
                if keys.find('U') != -1:
                    sectionSignCountAnswer = len(keys)-1
                    for student in students:
                        for stdPollArr in student.poll:
                            for stdPoll in stdPollArr.QuestionAndAnswers:
                                for stdPollKey in stdPoll:
                                    if stdPollKey == 'A':
                                        sectionSignCountQuestion = 1
                                        while stdPollArr.pollName[-sectionSignCountQuestion]=='§' :
                                            sectionSignCountQuestion+=1
                                        if stdPollArr.pollName.find(poll.pollName)!=-1 and sectionSignCountAnswer==sectionSignCountQuestion-1:
                                            if questionAndAnswer.get('Q') == stdPoll.get('Q'):
                                                for arrPoll in questionAndAnswer.get(keys):
                                                    for arrStu in stdPoll.get(stdPollKey):
                                                        for arrPollKey in arrPoll:
                                                            if arrPollKey==arrStu :
                                                                arrPoll[arrPollKey] = arrPoll.get(arrPollKey)+1
