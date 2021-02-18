# -*- coding: utf-8 -*-
import csv
import os
from Writer import *
from Poll import *
from Student import *
import xlrd
import logging
logging.basicConfig(filename='example.log', level=logging.INFO)

def __readStudentList__(filename):
    wb = xlrd.open_workbook(filename, encoding_override="UTF-8")
    sh = wb.sheet_by_index(0)
    data_list = []
    student_list = []
    for rownum in range(0, sh.nrows):
        data = []
        i = 0
        j = 0
        row_values = sh.row_values(rownum)
        for columnNum in range(0, sh.ncols):
            if (row_values[columnNum] != ''):
                data.insert(i, row_values[columnNum])
                i += 1
        if (len(data) >= 4 and data[1][0] == '1'):
            student_list.insert(j, Student(data[1], data[2], data[3]))
            logging.info("Student : " + data[1] + " " + data[2] + " " + data[3] + " added.")
            j += 1
    return student_list


def __readAnswerFileNames__(filename):
    arr = os.listdir(filename)
    poll_list = []
    for i in arr:
        if os.name == "posix":
            poll_list.append(__readAnswerKeys__(filename + "/" + i))
            logging.info("Answer Key : " + i + " added.")
        elif os.name == "nt":
            poll_list.append(__readAnswerKeys__(filename + "\\" + i))
            logging.info("Answer Key : " + i + " added.")
    return poll_list


def __readAnswerKeys__(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        pollName = ""
        question_answer_list = []
        for row in csv_reader:
            if line_count == 0:
                pollName = row[0]  # poll name dönüyor, array olduğu için column 0. indexi alıyoruz
                pollName = __beautify__(pollName)

                line_count += 1
            else:
                i = 0
                for columns in row:
                    columns.replace(chr(8230), '')
                    arr = columns.split(';')
                    arr[0] = arr[0][1:-1]
                    arr[0] = __beautify__(arr[0])
                    aranswer = ""
                    control = 0
                    for ar in arr :
                        if control == 0:
                            control+=1
                            continue
                        if control == 1:
                            aranswer += ar
                        else :
                            aranswer = aranswer + ";" + ar
                        control+=1
                    aranswer = aranswer[1:-1]
                    aranswer = __beautify__(aranswer)
                    questionanswer = {
                        'Q': arr[0],
                        'A': aranswer,
                        'U': set()
                    }
                    question_answer_list.insert(i, questionanswer)
                    i += 1
                    line_count += 1
        pollNameArr = pollName.split(":")
        pollNameName = "".join(pollNameArr[0])
        print(pollNameName)
        pollObject = Poll(pollNameName, question_answer_list)
        return pollObject


def __readPollFileNames__(filename, students, totalFile):
    arr = os.listdir(filename)
    poll_list = []
    for i in arr:
        if os.name == "posix":
            poll_list.append(__readStudentAnswers__(filename + "/" + i, students,i))
            logging.info("Poll : " + i + " added.")
            totalFile+=1
        elif os.name == "nt":
            poll_list.append(__readStudentAnswers__(filename + "\\" + i, students,i))
            logging.info("Poll : " + i + " added.")
            totalFile+=1
    return poll_list

def __readStudentAnswers__(filename, students, pollName):  # this will chang
    with open(filename, 'r', encoding='utf-8') as file:
        atendeeList=[]
        atendeeListF=[]
        zoomList=[]
        reader = csv.reader(file, delimiter='\t')
        k = 0
        i = -1
        data_arr = []
        columns = ""
        for row in reader:
            if(k == 5):
                if (i == -1):
                    columns = row[0]
                    i += 1
                    continue
                if (row[0][0].isdigit()):
                    data_arr.insert(i, row[0])
                    i += 1
                else:
                    data_arr[i-1] = data_arr[i-1] + row[0]
            else:
                k+=1
        for data in data_arr:
            data = __beautify__(data)
            startIndex = data.index(",") + 1
            if startIndex > 1:
                endIndex = data[startIndex:-1].index(",")
                if endIndex > startIndex:
                    name = __str_lower__(data[startIndex:startIndex + endIndex]).split(" ")
                    try:
                        name.remove("")
                    except:
                        pass
                    selectedStudent = None
                    selectionThreshold = 0
                    for student in students:
                        studentName = __str_lower__(student.firstName + " " + student.lastName).split(" ")
                        tmpThreshold = set(studentName).intersection(set(name)).__len__()
                        if tmpThreshold > selectionThreshold:
                            selectedStudent = student
                            selectionThreshold = tmpThreshold
                        elif tmpThreshold == selectionThreshold:
                            selectedStudent = None
                        if len(name) < 2:
                            if (studentName[1] in name[0]):  # this part is written for hami
                                selectedStudent = student
                                break
                    if (selectedStudent != None):
                        selectedStudent.__initPollAnswer__(data,students)
                        if(data.find("Are you attending this lecture")>0):
                            if selectedStudent not in atendeeList:
                                if atendeeList.__len__()==0:
                                    Student.attendancePoll+=1
                            else:
                                atendeeList.clear()
                                Student.attendancePoll+=1
                            atendeeList.append(selectedStudent)
                        atendeeListF.append(selectedStudent)
                    else:
                        zoomList.append("".join(name))
        writeAbsence(pollName, atendeeListF, students, zoomList)

def __str_lower__(_str):
    return _str.replace("I", "ı").replace("İ", "i").lower().replace("ı", "i").replace("ö", "o").replace("ç","c").replace(
        "ğ", "g").replace("ü", "u").replace("ş", "s")


def __beautify__(_str):
    _str = _str.replace("»¿", '')
    _str = _str.replace("(", '')
    _str = _str.replace(")", '')
    _str = _str.replace("-", '')
    _str = _str.replace("_", '')
    _str = _str.replace("<", '')
    _str = _str.replace(">", '')
    _str = _str.replace(":", '')
    _str = _str.replace("\'", '')
    _str = _str.replace("?", '')
    _str = _str.replace("ï", '')
    _str = _str.replace("\"", '')
    _str = _str.replace(";;", '')
    _str = _str.replace(";;;", '')
    _str = _str.replace("\r", '')
    _str = _str.replace("\n", '')
    _str = _str.replace(".", '')
    _str = _str.replace("..", '')
    _str = _str.replace(chr(8230), '...')
    _str = " ".join(_str.split())
    return _str
