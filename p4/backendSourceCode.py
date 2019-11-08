#p4 - 327
# REMINDER - AMOUNTS AND THEIR LIMITS ARE IN DECIMALS - BE SURE TO ADD TWO EXTRA ZEROS
# WE USE A DICTIONARY (HASHMAP IN PYTHON) TO STORE DAILY TRANSAC LIMITS

# the slides say "A newly created account must have a new unused account number"
# Does that mean not being currently used or never used at all?
# If never used at all, we have to use a hashmap to store all account numbers that were used
# We currently use a hashmap following the above assumption
# Store all accounts that were ever used, alongside their name
accountsHash = {}


def clearMasterTSF():
    open('mergedTSF.txt', 'w').close()

def mergeTSF():
    tsfLIST = 3
    for i in range(1,tsfLIST):
        tsf = open(str("tsf"+str(i)+".txt"),"r")
        lines = tsf.readlines()
        for line in lines:
            newTSF = open(str('mergedTSF.txt'),"a")
            if line != '':
                if line[:3] != 'EOS':
                    newTSF.write(line)
            newTSF.close()
        newTSF = open(str('mergedTSF.txt'), "a")
        #newTSF.write("EOS 0000000 000 0000000 ***") #i don't think we want EOS in the master TSF, we can't do anything with it
        newTSF.close()



def handleTSF():
    tsf = open('mergedTSF.txt', 'r')
    lines = tsf.readlines()
    # Use dictionaries as hashmaps to store the transac limi
    dailyDepLimit = {}
    dailyWithLimit = {}
    dailyTransfLimit = {}
    for line in lines:
        #tsfLine = line.split(' ')
        action = line[:3]
        accANum = line[4:11]
        iNEW = line.index(' ', 12)
        amount = int(line[12:iNEW])
        iNEW2 = line.index(' ', iNEW+1)
        accBNum = line[iNEW+1: iNEW2]
        accName = line[iNEW2+1:]
        if action == 'DEP':
            print ('deposit')
            #deposit(accANum, amount)
        elif action == 'WDR':
            print ('withdraw')
            #withdraw(accANum, amount)
        elif action == 'XFR':
            print ('transfer')
            #transfer(accANum, amount, accBNum)
        elif action == 'NEW':
            print ('create')
            #create(accANum, accName)
        elif action == 'DEL':
            print ('delete')
            #delete()

def deposit(toAccNum, amount):
    if amount <= 200000:
        checkLimit = dailyDepLimit[toAccNum] + amount
        if checkLimit <= 500000:
            maf = open("MAF.txt", "w")
            lines = maf.readlines()
            for line in lines:
                mafAccNum = line[:7]
                if mafAccNum == toAccNum:
                    mafLine = line.split(" ", 2)
                    mafAccName = mafLine[2]
                    mafAmountBalance = mafLine[1] + amount
                    maf.write(mafAccNum + " " + mafAmountBalance + " " + mafAccName)
                    dailyDepLimit[toAccNum] = dailyDepLimit[toAccNum] + amount
                    break
            maf.close()
        else:
            print("Exceeded daily deposit limit")
    else:
        print("Exceeded single deposit limit")



def withdraw(fromAccNum, amount):
    if amount <= 100000:
        checkLimit = dailyWithLimit[fromAccNum] + amount
        if checkLimit <= 500000:
            maf = open("MAF.txt", "w")
            lines = maf.readlines()
            for line in lines:
                mafAccNum = line[:7]
                if mafAccNum == fromAccNum:
                    mafLine = line.split(" ", 2)
                    mafAccName = mafLine[2]
                    mafAmountBalance = mafLine[1] - amount
                    if mafAmountBalance >= 0:
                        maf.write(mafAccNum + " " + mafAmountBalance + " " + mafAccName)
                        dailyWithLimit[fromAccNum] = dailyWithLimit[fromAccNum] + amount
                    else:
                        print("Error - insufficient funds")
                    break
            maf.close()
        else:
            print("Exceeded daily withdraw limit")
    else:
        print("Exceeded single withdraw limit")


def transfer(toAccNum, amount, fromAccNum):
    if amount <= 1000000:
        # Note: there is only a limit for transferring OUT of an account
        checkLimit = dailyTransfLimit[fromAccNum] + amount
        if checkLimit <= 1000000:
            maf = open("MAF.txt", "w")
            lines = maf.readlines()
            for line in lines:
                mafAccNum = line[:7]
                if mafAccNum == fromAccNum:
                    mafLine = line.split(" ", 2)
                    mafAccName = mafLine[2]
                    mafAmountbalance = mafLine[1] - amount
                    if mafAmountbalance >= 0:
                        maf.write(mafAccNum + " " + mafAmountbalance + " " + mafAccName)
                        dailyTransfLimit[fromAccNum] = dailyTransfLimit[fromAccNum] + amount
                    else:
                        print("Error - insufficient funds")
                    break
            for line in lines:
                mafAccNum = line[:7]
                if mafAccNum == toAccNum:
                    mafLine = line.split(" ", 2)
                    mafAccName = mafLine[2]
                    mafAmountbalance = mafLine[1] + amount
                    maf.write(mafAccNum + " " + mafAmountBalance + " " + mafAccName)
                    # I include the line below to remind y'all that we do NOT need a daily limit for the TO account
                    #dailyDepLimit[toAccNum] = dailyDepLimit[toAccNum] + amount
            maf.close()
        else:
            print("Exceeded daily transfer limit")
    else:
        print("Exceeded single transfer limit")

def updateAccountsHash():
    maf = open("MAF.txt", "r")
    lines = maf.readlines()
    for line in lines:
        mafLine = line.split(" ", 2)
        mafAccNum = mafLine[0]
        mafAccName = mafLine[2]
        # Associate account name with account number
        accountsHash[mafAccNum] = mafAccName

# Use this function if deleted account numbers can be used for create
def create(accNum, accName):
    if 'accNum' in accountsHash:
        maf = open("MAF.txt", "a")
        maf.write(accNum + " " + "000" + " " + accName)
        maf.close()

#def createNewMAF():
#    oldMaf = open('MAF.txt', 'w')


    #maf = open('MAF.txt', 'w')


#mainline

clearMasterTSF()
mergeTSF()
handleTSF()
print ('done')