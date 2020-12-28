#!/usr/bin/python3
import os
import random
import csv

baseDir = os.getcwd()#current folder
imgDir = os.path.join(baseDir, "mine_imgs")#image folder
dataDir = os.path.join(baseDir, "work_seatData")#seat csv folder

def readSeat(classNum):

    savedClassList=[]

    seatReadFile = open(f'{dataDir}/work_seatData.csv','r',encoding='UTF-8')

    for i in seatReadFile:
        compareData=list(map(str,i.split(",")))
        if compareData[0] == str(classNum):
            savedClassList.append([compareData[1],compareData[2]])
    seatReadFile.close()

    if len(savedClassList) == 0:
        print("No seat")
        return False
    else:
        return savedClassList


def randomSelectSeat(classNum, name, seatLimit):

    savedNumList=[]

    seatReadFile = open(f'{dataDir}/work_seatData.csv','r',encoding='UTF-8')
    for i in seatReadFile:
        compareData=list(map(str,i.split(",")))
        if compareData[0] == str(classNum):
            savedNumList.append(int(compareData[1]))
    seatReadFile.close()

    if seatLimit - len(savedNumList) == 0:
        print("No seat")
        return False
    elif seatLimit > 24:
        print("Over seat limit.")
        return False
    else:
        seatNum = random.randint(1, seatLimit)
        while savedNumList.count(seatNum) != 0 or seatNum == 13:
            seatNum = random.randint(1, seatLimit)

        if savedNumList.count(seatNum) == 0:
            seatAppendFile = open(f'{dataDir}/work_seatData.csv','a',encoding='UTF-8')

            seatAppendFile.write(f"{str(classNum)},{str(seatNum)},{name}\n")
            seatAppendFile.close()

            print(f"Complete -> class: {classNum}, searNumber: {seatNum}, name: {name}")
            return [seatNum,name]
            #return True
def randomDeleteSeat(classNum, name):

    tempList=[]
    count=0

    seatReadFile = open(f'{dataDir}/work_seatData.csv','r',encoding='UTF-8')
    for i in seatReadFile:
        compareData=list(map(str,i.split(",")))
        count+=1
        if compareData[0] == str(classNum) and compareData[2] == name+"\n":
            print("same")
            continue
        else:
            tempList.append(compareData)
    seatReadFile.close()

    if len(tempList) == count:
        return False
    else:
        seatDelFile = open(f'{dataDir}/work_seatData.csv','w',encoding='UTF-8')
        for i in range(len(tempList)):
            seatDelFile.write(f"{str(tempList[i][0])},{str(tempList[i][1])},{tempList[i][2]}")
        seatDelFile.close()
        #return True

def selectSeat(classNum, seatNum, name):

    seatReadFile = open(f'{dataDir}/work_seatData.csv','r',encoding='UTF-8')
    for i in seatReadFile:
        compareData=list(map(str,i.split(",")))
        print(compareData[0],str(classNum),compareData[1],str(seatNum))
        if compareData[0] == str(classNum) and compareData[1] == str(seatNum) :
            print("Occupied. Delete first.")
            return False
    seatReadFile.close()

    seatAppendFile = open(f'{dataDir}/work_seatData.csv','a',encoding='UTF-8')
    seatAppendFile.write(f"{str(classNum)},{str(seatNum)},{name}\n")
    seatAppendFile.close()
    print(f"Complete -> class: {classNum}, seatNumber: {seatNum}, name: {name}")
    #return True

def deleteSeat(classNum, seatNum):

    tempList=[]
    count=0

    seatReadFile = open(f'{dataDir}/work_seatData.csv','r',encoding='UTF-8')
    for i in seatReadFile:
        compareData=list(map(str,i.split(",")))
        count+=1
        if compareData[0] == str(classNum) and compareData[1] == str(seatNum):
            print("same")
            continue
        else:
            tempList.append(compareData)
    seatReadFile.close()

    if len(tempList) == count:
        return False
    else:
        seatDelFile = open(f'{dataDir}/work_seatData.csv','w',encoding='UTF-8')
        for i in range(len(tempList)):
            seatDelFile.write(f"{str(tempList[i][0])},{str(tempList[i][1])},{tempList[i][2]}")
        seatDelFile.close()
        #return True
