import re
from functools import singledispatch
import tmp as t
class Mail(object):
    subject = None
    messageId = None
    folderPath = None
    status = None
    fetchDate = None
    fetchTime = None
    moveDate=None
    moveTime=None
    isWorkAllocation = False

    def __init__(self):
       pass

class WorkAllocationAttribute(object):
    status = None
    mailsFetched = None
    fetchDate = None
    fetchTime = None
    moveDate = None
    moveTime = None
    mailList = []

    def __init__(self):
       pass

def getMailFromFolderPath(mail,folderPath):
    if mail.folderPath != None:
        folderPath = folderPath.replace('/','\\')
        if folderPath == mail.folderPath:
            return True

def setMailFromFolderPath(mail,folderPath,mailToBeSet):
    if mail.folderPath != None:
        folderPath = folderPath.replace('/', '\\')
        if folderPath == mail.folderPath:
            mail = mailToBeSet

def processLog(logMessages):
    tempData =[]
    mailList=[]
    mail = None
    workAllocationAttr = WorkAllocationAttribute()
    try:
        for logMessage in logMessages:
            if logMessage:
                if 'mails fetched'.upper() in logMessage.upper():
                    a = logMessage.split('[')
                    workAllocationAttr.mailsFetched = a[a.__len__() - 1][0]
                    workAllocationAttr.fetchDate = re.findall(r"\d{4}-\d{2}-\d{2}",logMessage)
                    workAllocationAttr.fetchTime = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
                if 'processing mail subject'.upper() in logMessage.upper():
                    mail = Mail()
                    a = logMessage.split('[')
                    b = a[a.__len__() - 1]
                    # workAllocationAttr.mailsFetched = mailsFetched
                    # workAllocationAttr.fetchTime = fetchTime
                    # workAllocationAttr.fetchDate = fetchDate
                    mail.subject = b[b.index('subject'.upper()):b.index('MessageId'.upper())]
                    mail.messageId = b[b.index('MessageId'.upper()):b.index(']')]
                if 'work allocation mail'.upper() in logMessage.upper():
                    mail = Mail()
                    mail.isWorkAllocation = True
                    mail.subject ='Work Allocation'
                    mail.fetchTime = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
                    mail.fetchDate = re.findall(r"\d{4}-\d{2}-\d{2}", logMessage)
                    #mail.fetchTime = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
                    #mail.fetchDate = re.findall(r"\d{4}-\d{2}-\d{2}", logMessage)
                    workAllocationAttr.mailList.append(mail)
                    mailList.append(mail)
                    #tempData.append(workAllocationAttr)
                if 'will be moved to'.upper() in logMessage.upper():
                    a = logMessage.split('[')
                    b = a[a.__len__() - 1]
                    c = b.split(':')
                    mail.folderPath = c[c.__len__()-1].strip().replace(']','')
                    workAllocationAttr.mailList.append(mail)
                    mailList.append(mail)
                    #tempData.append(workAllocationAttr)
                if 'mails to folder'.upper() in logMessage.upper() or 'moving batch of'.upper() in logMessage.upper():
                    workAllocationAttr.moveDate = re.findall(r"\d{4}-\d{2}-\d{2}", logMessage)
                    workAllocationAttr.moveTime = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
                    a = logMessage.split('[')
                    b= a[a.__len__()-1].split(':')
                    c = b[b.__len__()-1].replace(']','').strip()
                    mailIter = filter((lambda x: getMailFromFolderPath(x,c)),mailList)
                    mail = next(mailIter)
                    if mail:
                        mail.moveDate = re.findall(r"\d{4}-\d{2}-\d{2}", logMessage)
                        mail.moveTime = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
                    # for i in map((lambda x:setMailFromFolderPath(x,c,mail)),mailList):
                    #    pass
                if 'did not any work allocation'.upper() in logMessage.upper():
                    mail.status = 'Match Not Found'
                    workAllocationAttr.mailList.append(mail)
                    mailList.append(mail)
                    #tempData.append(workAllocationAttr)
                if 'ERROR'.upper() in logMessage.upper():
                    #workAllocationAttr.mailList.append(mail)
                    workAllocationAttr.status = 'Error'
                    #tempData.append(workAllocationAttr)
                if 'RefreshTimer_Elapsed thread finished'.upper() in logMessage.upper():
                    tempData.append(workAllocationAttr)
                    #t.data.append(workAllocationAttr)
    except RuntimeError:
        pass
    return (tempData,mailList)