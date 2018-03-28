import csv
import Process as prcs
import math
import re
import uuid
data = []
import multiprocessing as mp
ls1=[]
ls2=[]
ls3=[]
ls4=[]
ls5=[]
ls6=[]

# def PrepareData(waDict):
#     workAllocationAttribute = WorkAllocationAttribute()
#     if type(waDict)==dict:
#         workAllocationAttribute.subject = waDict['subject']
#         workAllocationAttribute.mailsFetched = waDict['mailsFetched']
#         workAllocationAttribute.messageId = waDict['messageId']
#         workAllocationAttribute.folderPath = waDict['folderPath']
#         workAllocationAttribute.status = waDict['status']
#         workAllocationAttribute.EOP = waDict['EOP']
#         workAllocationAttribute.fetchDate = waDict['fetchDate']
#         workAllocationAttribute.fetchTime = waDict['fetchTime']
#         workAllocationAttribute.moveDate = waDict['moveDate']
#         workAllocationAttribute.moveTime = waDict['moveTime']

def collectResult(workAllocation):
    workAllocation[0][0].mailList.extend(workAllocation[1])
    data.extend(workAllocation[0])

def error(workAllocationError):
    print(workAllocationError)

def splitFile(content):
    pool = mp.Pool(processes=4)
    results =None
    masterList =[]
    a = True
    logIterator = iter(content)
    counter = 0
    linesPerLogList = math.ceil(logIterator.__length_hint__() / 5)
    countPerLogList = 0
    while (logIterator.__length_hint__() > 0):
        if 'Fetching mails start'.upper() in logIterator.__next__().upper():
            countPerLogList = countPerLogList + 1
            a = True
            while(a):
                currentLog = logIterator.__next__().upper()
                if 'RefreshTimer_Elapsed thread finished'.upper() not in currentLog :
                    masterList.append(currentLog)
                else:
                    masterList.append(currentLog)
                    counter = counter + 1
                    insertInToBucket(linesPerLogList,masterList)
                    #results = pool.apply_async(processLog,args =[masterList],callback = collectResult,error_callback=error)
                    #processLog(masterList)
                    masterList = []
                    a = False

    for i in [ls1,ls2,ls3,ls4,ls5,ls6]:
        if i:
            r = pool.apply_async(prcs.processLog, args=[i], callback=collectResult, error_callback=error)
            r.get()
    writeToExcel()

def writeToExcel():
    with open('C:/Users/ABC/Desktop/Nishikant/WACSV.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Subject','Message Id','Folder Path','Status','Work Allocaion','Fetch Time','Fetch Date','Move Date','Move Time','Mails Fetched'])
        if data:
            for wa in data:
                if wa.mailList:
                    for mail in wa.mailList:
                        wr.writerow([mail.subject, mail.messageId, mail.folderPath,
                                     getMailStatus(wa,mail), mail.isWorkAllocation,mail.fetchTime,
                                     mail.fetchDate,mail.moveDate,mail.moveTime,wa.mailsFetched if mail.isWorkAllocation else None])

def getMailStatus(wa,mail):
    status=None
    if wa.status != None:
        status =wa.status
    elif mail.status != None:
        status = mail.status
    else:
        status = 'Success'
    return status

def insertInToBucket(linesPerLogList,masterList):
    if len(ls1)<linesPerLogList:
        ls1.extend(masterList)
    elif len(ls2)<linesPerLogList:
        ls2.extend(masterList)
    elif len(ls3)<linesPerLogList:
        ls3.extend(masterList)
    elif len(ls4)<linesPerLogList:
        ls4.extend(masterList)
    elif len(ls5)<linesPerLogList:
        ls5.extend(masterList)
    elif len(ls6)<linesPerLogList:
        ls6.extend(masterList)


def main():
    with open("C:/Users/ABC/Desktop/Nishikant/WA.txt", 'r') as ins:
        content = [x.strip() for x in ins]
        splitFile(content)
        # for i in ins:
        #     processLog(i)


if __name__ =='__main__':
    main()


