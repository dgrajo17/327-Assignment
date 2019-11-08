#p4 - 327
# REMINDER - AMOUNTS AND THEIR LIMITS ARE IN DECIMALS - BE SURE TO ADD TWO EXTRA ZEROS
# WE USE A DICTIONARY (HASHMAP IN PYTHON) TO STORE DAILY TRANSAC LIMITS


def clearMasterTSF():
	open('mergedTSF.txt', 'w').close()
	
def mergeTSF():
	for i in (tsfLIST):
		tsf = open(str(tsfLIST+i),"r")
		lines = tsf.readlines()
		for line in lines:
			newTSF = open(str('mergedTSF.txt'),"a")
			if line != '':
				if line[:3] != 'EOS':
					newTSF.write(line)
			newTSF.close()
		tsf.close()

def handleTSF():
	tsf = open('mergedTSF.txt', 'r')
	lines = tsf.readlines()
    # Use dictionaries as hashmaps to store the transac limi
    dailyDepLimit = {}
    dailyWithLimit = {}
    dailyTransfLimit = {}
	for line in lines:
        tsfLine = line.split(" ", 5)
		action = line[0]
        accANum = line[1]
        amount = line[2]
        accBNum = line[3]
        accName = line[4]
		#action = line[:3]
		if action == 'DEP':
			deposit(accANum, amount)
		elif action == 'WDR':
			withdraw(accANum, amount)
		elif action == 'XFR':
			transfer(accANum, amount, accBNum)
		elif action == 'NEW':
			create()
		elif action == 'DEL':
			delete()

def deposit(toAccNum, amount):
    if amount <= 200000:
        checkLimit = dailyDepLimit[toAccNum] + amount
        if checkLimit <= 500000:
            maf = open('MAF.txt', 'w')
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
            maf = open('MAF.txt', 'w')
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
        else:
            print("Exceeded daily withdraw limit")
    else:
        print("Exceeded single withdraw limit")


def transfer(toAccNum, amount, fromAccNum):
    if amount <= 1000000:
        # Note: there is only a limit for transferring OUT of an account
        checkLimit = dailyTransfLimit[fromAccNum] + amount
        if checkLimit <= 1000000:
            maf = open('MAF.txt', 'w')
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
        else:
            print("Exceeded daily transfer limit")
    else:
        print("Exceeded single transfer limit")




def createMAF():

	#maf = open('MAF.txt', 'w')


#mainline
clearMasterTSF()
mergeTSF()
handleTSF()