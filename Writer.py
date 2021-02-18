import xlwt
import xlrd
import os
from xlutils.copy import copy as copyWb
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.platypus import SimpleDocTemplate, Paragraph
from Student import *
import json

def writeAbsence(pollName,atendeeList,students,zoomlist):
    absenceList = []
    anomalieList = []
    for student in students:
        studentControl = 0
        for atendee in atendeeList:
            if student.studentNo == atendee.studentNo:
                studentControl = 1
                break
        if studentControl == 0:
            absenceList.append(student)
    with open(pollName[8:16]+"_absence_list.json", 'w', encoding="UTF-8") as outfile:
        json.dump("zoom poll report name:"+pollName,outfile,ensure_ascii=False)
        outfile.write('\n')
        json.dump("Students in BYS list but don't exist in this poll report (Absence) :",outfile,ensure_ascii=False)
        outfile.write('\n')
        for student in absenceList:
            outfile.write('\n')
            json.dump("{student no:"+student.studentNo+", student name: "+student.firstName+" "+student.lastName+"}",outfile,ensure_ascii=False)
        outfile.write('\n')
        outfile.write('\n')
        json.dump("Students in this poll report but don't exist in BYS Student List (Anomalies) :",outfile)
        for studentZoom in zoomlist:
            outfile.write('\n')
            json.dump("{"+studentZoom+"}",outfile)

def iif(a,_true,_false):
    if a:return _true
    else:return _false

def writeNames(ws,students):
    vertCenterHorizCenter=xlwt.easyxf("align: vert center, horiz center")
    ws.col(0).width = 256 * 12
    ws.col(1).width = 256 * 30
    ws.col(2).width = 256 * 20
    ws.write_merge(0,1,0,0,"Student Id",vertCenterHorizCenter)
    ws.write_merge(0,1,1,1,"Name",vertCenterHorizCenter)
    ws.write_merge(0,1,2,2,"Surname",vertCenterHorizCenter)
    line=2
    for student in reversed(students):
        ws.write(line,0,student.studentNo)
        ws.write(line,1,student.firstName)
        ws.write(line,2,student.lastName)
        line+=1

def getQuestions(poll):
    questions=[]
    for q in range(1,poll.QuestionAndAnswers.__len__()+1):
        questions.append(poll.QuestionAndAnswers[q-1].get("Q"))
    return questions

def getRecurring(poll,students):
    recurring=0
    for student in students:
        for pollN in student.poll:
            if type(pollN.pollName) is not int:
                if pollN.pollName.replace("§","")==poll.pollName:
                    recurring=max(recurring,pollN.pollName.count("§"))
    return recurring

def writePollHeaders(ws,poll,q,itsRecurrringnumber=-1,offset=3):
    horizCenter=xlwt.easyxf("align: horiz center")
    ws.write_merge(0,0,offset,q+2+offset,poll.pollName+iif(itsRecurrringnumber>-1,"-"+str(itsRecurrringnumber+1),""),horizCenter)
    for _ in range(1,q+1):
        ws.write(1,offset-1+_,"Q"+str(_),horizCenter)
    ws.write(1,offset-1+q+1,"number of questions",horizCenter)
    ws.col(offset-1+q+1).width = 256 * 20
    ws.write(1,offset-1+q+2,"success rate",horizCenter)
    ws.col(offset-1+q+2).width = 256 * 20
    ws.write(1,offset-1+q+3,"success percentage",horizCenter)
    ws.col(offset-1+q+3).width = 256 * 20

def writeFormulasforStatisticBasedOnPollforeachStudent(ws,line,q,offset=3):
    ws.write(line,offset-1+q+1,xlwt.Formula("COUNTA("+xlwt.Utils.rowcol_to_cell(line,offset)+":"+xlwt.Utils.rowcol_to_cell(line,offset+q-1)+")"))
    ws.write(line,offset-1+q+2,xlwt.Formula("COUNTIF("+xlwt.Utils.rowcol_to_cell(line,offset)+":"+xlwt.Utils.rowcol_to_cell(line,offset+q-1)+";1)"))
    ws.write(line,offset-1+q+3,xlwt.Formula(xlwt.Utils.rowcol_to_cell(line,offset+q+1)+"*100/"+str(q)+";0)"))
    
def createGraphs(poll,q,iR):

    doc = SimpleDocTemplate("Exports\\" + poll.pollName + '-' + str(iR+1) + '.pdf')
    answerKey = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    elements = []
    styles = getSampleStyleSheet()
    # creating custom stylesheet
    styles.add(ParagraphStyle(name='Content',fontSize=10,textColor=colors.HexColor("#008000")))
    styles.add(ParagraphStyle(name='Content2',fontSize=10,textColor=colors.HexColor("#ffffff")))
    for questionAndAnswer in poll.QuestionAndAnswers :
        ptext = Paragraph("Question : "+questionAndAnswer.get('Q'), styles["Normal"])
        ptextnewline = Paragraph('.', styles["Content2"])
        elements.append(ptext)
        elements.append(ptextnewline)
        data = []
        answers = []
        counts = []
        data_index = 1
        for keys in questionAndAnswer:
            if keys.find('U') != -1:
                if 'U'+('§'*iR) == keys:
                    for answersAndCounts in questionAndAnswer.get(keys):
                        for answer in answersAndCounts:
                            if questionAndAnswer.get('A').find(answer) != -1 :
                                elements.append(Paragraph(answerKey[data_index-1]+':'+answer+"  -  "+str(answersAndCounts.get(answer)), styles["Content"]))
                            else :
                               elements.append(Paragraph(answerKey[data_index-1]+':'+answer+"  -  "+str(answersAndCounts.get(answer)), styles["Normal"]))
                            answers.insert(data_index,'A'+str(data_index))
                            counts.insert(data_index,answersAndCounts.get(answer))
                            data_index+=1
        data.insert(0,answers)
        data.insert(1,counts)

        chart = pie_chart_with_legend(data[1],answerKey)
        chart2 = make_drawing(data[1],answerKey)
        elements.append(ptextnewline)
        elements.append(chart)
        for newline in range(0,15):
            elements.append(ptextnewline)
        elements.append(chart2)
    try:
        doc.build(elements)
    except:
        print(".")

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)

def make_drawing(d,answerKey):
    drawing = Drawing(400, 200)
    maxData = 0
    for count in d :
        if count > maxData:
            maxData = count
    data = [tuple(d),]
    names = answerKey
    bc = VerticalBarChart()
    bc.x = 20
    bc.y = 50
    bc.height = 180
    bc.width = 400
    bc.data = data
    bc.strokeColor = colors.white
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = maxData
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = -10
    bc.categoryAxis.labels.fontName = 'Helvetica'
    bc.categoryAxis.categoryNames = names

    drawing.add(bc)
    return drawing

def pie_chart_with_legend(data,answerKey):
    drawing = Drawing(width=400, height=200)
    my_title = String(170, 40, 'Pie', fontSize=12)
    pie = Pie()
    pie.sideLabels = True
    pie.x = 150
    pie.y = 65
    pie.data = data
    pie.labels = [letter for letter in answerKey]
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data)
    return drawing

def __export__(students,polls):
    vertCenterHorizCenter=xlwt.easyxf("align: vert center, horiz center")
    horizCenter=xlwt.easyxf("align: horiz center")
    for poll in polls:
        recurring=getRecurring(poll,students)
        questions=getQuestions(poll)
        q=questions.__len__()
        for iR in range(0,recurring+1):
            wb=xlwt.Workbook()
            ws=wb.add_sheet("Sheet 1")
            writeNames(ws,students)
            writePollHeaders(ws,poll,q,iif(recurring>0,iR,-1))
            line=2
            for student in reversed(students):
                studentPoll=None
                for stPoll in student.poll:
                    if (stPoll.pollName)==poll.pollName+('§'*iR):
                        studentPoll=stPoll
                if studentPoll!=None:
                    for i in range(1,q+1):
                        for studentQuestionAndAnswer in studentPoll.QuestionAndAnswers:
                            if studentQuestionAndAnswer.get("Q")==questions[i-1]:
                                ws.write(line,2+i,studentQuestionAndAnswer.get("C"))
                                break
                writeFormulasforStatisticBasedOnPollforeachStudent(ws,line,q)
                line+=1
            try:
                wb.save(os.getcwd()+"\\Exports\\"+poll.pollName+iif(recurring>0,"-"+str(iR+1),"")+".xls")
            except FileNotFoundError:
                os.mkdir(os.getcwd()+"\\Exports\\")
                wb.save(os.getcwd()+"\\Exports\\"+poll.pollName+iif(recurring>0,"-"+str(iR+1),"")+".xls")
            if(q!=0 and iR!=0):
                createGraphs(poll, q, iR)

def __globalFile__(students,polls):
    wb=ws=studentsOnGlobalFile=None
    pollsOnGlobalFile=[]
    yOffset=3
    try:
        studentsOnGlobalFile=[]
        wb = xlrd.open_workbook(os.getcwd()+"\\Exports\\(AllPolls).xls",formatting_info=True)
        ws = wb.sheet_by_index(0)
        for i in range(2,ws.nrows):
            for student in reversed(students):
                if student.studentNo==ws.cell_value(i,0):
                    studentsOnGlobalFile.insert(0,student)
                    break
        for i in range(3,ws.ncols):
            if ws.cell_value(0,i)!="":
                cellValue=ws.cell_value(0,i)
                value=cellValue.split("-")
                if value.__len__()>1:
                    try:
                        factor=int(value[value.__len__()-1])
                        if factor<1 or not cellValue.endswith("-"+str(factor)):
                            raise Exception()
                        pollsOnGlobalFile.append(cellValue[:cellValue.rfind("-")]+"§"*(factor-1))
                    except:
                        pass
                else:
                    pollsOnGlobalFile.append(cellValue)
        yOffset=ws.ncols
        wb=copyWb(wb)
        ws=wb.get_sheet(0)
    except FileNotFoundError:
        studentsOnGlobalFile=students
        wb = xlwt.Workbook()
        ws=wb.add_sheet("Sheet 1")
        writeNames(ws,students)
    for poll in polls:
        recurring=getRecurring(poll,students)
        questions=getQuestions(poll)
        q=questions.__len__()
        for iR in range(0,recurring+1):
            pollnameTemp=poll.pollName+"§"*iR
            if pollnameTemp not in pollsOnGlobalFile:
                writePollHeaders(ws,poll,q,iif(recurring>0,iR,-1),yOffset)
                line=2
                for student in reversed(studentsOnGlobalFile):
                    studentPoll=None
                    for stPoll in student.poll:
                        if (stPoll.pollName)==pollnameTemp:
                            studentPoll=stPoll
                    if studentPoll!=None:
                        for i in range(1,q+1):
                            for studentQuestionAndAnswer in studentPoll.QuestionAndAnswers:
                                if studentQuestionAndAnswer.get("Q")==questions[i-1]:
                                    ws.write(line,yOffset-1+i,studentQuestionAndAnswer.get("C"))
                                    break
                    writeFormulasforStatisticBasedOnPollforeachStudent(ws,line,q,yOffset)
                    line+=1
                yOffset+=q+3
    wb.save(os.getcwd()+"\\Exports\\(AllPolls).xls")

def __Attendance__(students,polls):
    horizCenter=xlwt.easyxf("align: horiz center")
    wb = xlwt.Workbook()
    ws=wb.add_sheet("Sheet 1")
    writeNames(ws,students)
    ws.write_merge(0,0,3,5,"Attendance Polls",horizCenter)
    ws.write(1,3,"Attended",horizCenter)
    ws.write(1,4,"Total",horizCenter)
    ws.write(1,5,"Percentage",horizCenter)  
    ws.write_merge(0,0,6,8,"Other Polls",horizCenter)
    ws.write(1,6,"Attended",horizCenter)
    ws.write(1,7,"Total",horizCenter)
    ws.write(1,8,"Percentage",horizCenter) 
    ws.write_merge(0,0,9,11,"All",horizCenter)
    ws.write(1,9,"Attended",horizCenter)
    ws.write(1,10,"Total",horizCenter)
    ws.write(1,11,"Percentage",horizCenter)
    totalPoll=0
    for poll in polls:
        totalPoll+=getRecurring(poll,students)+1
    line=2
    for student in reversed(students):
        ws.write(line,3,student.totalAttendance)
        ws.write(line,4,Student.attendancePoll)
        tempVal=0
        if Student.attendancePoll>0:
            tempVal=student.totalAttendance*100/Student.attendancePoll
        ws.write(line,5,tempVal)
        ws.write(line,6,student.poll.__len__())
        ws.write(line,7,totalPoll)
        tempVal=0
        if totalPoll>0:
            tempVal=student.poll.__len__()*100/totalPoll
        ws.write(line,8,tempVal)
        ws.write(line,9,student.totalAttendance+student.poll.__len__())
        ws.write(line,10,Student.attendancePoll+totalPoll)
        tempVal=0
        if Student.attendancePoll+totalPoll>0:
            tempVal=(student.totalAttendance+student.poll.__len__())*100/(Student.attendancePoll+totalPoll)
        ws.write(line,11,tempVal)
        line+=1
    wb.save(os.getcwd()+"\\Exports\\Attendance.xls")
