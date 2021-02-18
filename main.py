import Reader
import os
import Writer
import Analyzer
import Statistic

def main():
    totalFile = 0
    students = Reader.__readStudentList__("CES3063_Fall2020_rptSinifListesi.XLS")
    if os.name == "posix":
        polls = Reader.__readAnswerFileNames__(os.getcwd() + "/Answers")
        Reader.__readPollFileNames__(os.getcwd() + "/Polls", students,totalFile)  # we will read student answers with this func
    elif os.name == "nt":
        polls = Reader.__readAnswerFileNames__(os.getcwd() + "\Answers")
        Reader.__readPollFileNames__(os.getcwd() + "\Polls", students,totalFile)  # we will read student answers with this func

    Analyzer.__findAttendancePolls__(students, "Are you attending this lecture")

    Analyzer.__findPollsAndChangeKey__(students, polls)

    Analyzer.__findStudentAnswers__(students, polls)



    Statistic.__answerCounts__(students, polls)
    Writer.__export__(students, polls)
    Writer.__globalFile__(students,polls)
    Writer.__Attendance__(students,polls)

if __name__ == "__main__":
    main()
