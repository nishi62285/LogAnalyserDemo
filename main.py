import re
import uuid
data = []
workAllocationAttr = None

class WorkAllocationAttribute(object):
    mailsFetched = None
    subject = None
    messageId = None
    folderPath = None
    status = None
    fetchDate = None
    fetchTime = None
    moveDate = None
    moveTime = None
    def __init__(self):
        self.id =uuid.uuid4()

def getworkAllocationAttr(workAllocationAttr,id):
    if id == workAllocationAttr.id:
        return True

def setworkAllocationAttr(workAllocationAttr,id,workAllocationAttrToBeSet):
    if id == workAllocationAttr.id:
        workAllocationAttr = workAllocationAttrToBeSet

def processLog(logMessage):
    #workAllocationAttr = None
    workAlocationDict ={}
    if logMessage:
        if 'mails fetched'.upper() in logMessage.upper():
            #workAllocationAttr = WorkAllocationAttribute()
            a = logMessage.split('[')
            #workAllocationAttr.mailsFetched = a[a.__len__() - 1][0]
            #data.append(a[a.__len__() - 1][0])
            workAlocationDict['mailsFetched'] = a[a.__len__() - 1][0]
            workAlocationDict['fetchDate'] = re.findall(r"\d{4}-\d{2}-\d{2}",logMessage)
            workAlocationDict['fetchTime'] = re.findall(r"\d{2}:\d{2}:\d{2}",logMessage)
            return
        if 'processing mail subject'.upper() in logMessage.upper():
            #workAllocationAttr = WorkAllocationAttribute()
            #filter((lambda x:getworkAllocationAttr(x,id)),data).__next__()
            a = logMessage.split('[')
            b = a[a.__len__() - 1]
            # workAllocationAttr.subject = b[b.index('subject'):b.index('MessageId')]
            # workAllocationAttr.messageId = b[b.index('MessageId'):b.index(']')]
            # workAllocationAttr.mailsFetched = mailsFetched

            # data.append(b[b.index('subject'):b.index('MessageId')])
            # data.append(b[b.index('MessageId'):b.index(']')])

            workAlocationDict['subject'] = b[b.index('subject'):b.index('MessageId')]
            workAlocationDict['messageId'] = b[b.index('MessageId'):b.index(']')]

            #data.append(workAllocationAttr)
            #map((lambda x : setworkAllocationAttr(x,id,workAllocationAttr)),data)
            return
        if 'will be moved to'.upper() in logMessage.upper():
            #workAllocationAttr = filter((lambda x: getworkAllocationAttr(x, id)), data).__next__()
            a = logMessage.split('[')
            b = a[a.__len__() - 1][0]
            c = b.split(':')
            #workAllocationAttr.folderPath = c[c.__len__()-1].strip().replace(']','')
            #data.append(c[c.__len__()-1].strip().replace(']',''))
            workAlocationDict['folderPath'] = c[c.__len__()-1].strip().replace(']','')
            #map((lambda x: setworkAllocationAttr(x, id, workAllocationAttr)), data)
            return
        if 'mails to folder'.upper() in logMessage.upper() or 'moving batch of'.upper() in logMessage.upper():
            workAlocationDict['moveDate'] = re.findall(r"\d{4}-\d{2}-\d{2}", logMessage)
            workAlocationDict['moveTime'] = re.findall(r"\d{2}:\d{2}:\d{2}", logMessage)
            return
        if 'did not any work allocation'.upper() in logMessage.upper():
            #workAllocationAttr.status = 'Match Not Found'
            #data.append('Match Not Found')
            workAlocationDict['status'] = 'Match Not Found'
            return
        if 'ERROR'.upper() in logMessage.upper():
            #workAllocationAttr.status = 'Error'
            #data.append('Error')
            workAlocationDict['status'] = 'Error'
            return
        if 'RefreshTimer_Elapsed thread finished'.upper() in logMessage.upper():
            #data.append('End')
            workAlocationDict['EOP'] = 'End'
            PrepareData(workAlocationDict)


def PrepareData(waDict):
    workAllocationAttribute = WorkAllocationAttribute()
    if type(waDict)==dict:
        workAllocationAttribute.subject = waDict['subject']
        workAllocationAttribute.mailsFetched = waDict['mailsFetched']
        workAllocationAttribute.messageId = waDict['messageId']
        workAllocationAttribute.folderPath = waDict['folderPath']
        workAllocationAttribute.status = waDict['status']
        workAllocationAttribute.EOP = waDict['EOP']
        workAllocationAttribute.fetchDate = waDict['fetchDate']
        workAllocationAttribute.fetchTime = waDict['fetchTime']
        workAllocationAttribute.moveDate = waDict['moveDate']
        workAllocationAttribute.moveTime = waDict['moveTime']
        data.append(workAllocationAttribute)

def main():
    with open("C:/Users/ABC/Desktop/Nishikant/WorkAllocationLog.txt", 'r') as ins:
        for i in ins:
            processLog(i)


if __name__ =='__main__':
    main()
    a=2
