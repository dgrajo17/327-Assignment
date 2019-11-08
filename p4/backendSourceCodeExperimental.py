#p4 - 327
# REMINDER - AMOUNTS AND THEIR LIMITS ARE IN DECIMALS - BE SURE TO ADD TWO EXTRA ZEROS
# WE USE A DICTIONARY (HASHMAP IN PYTHON) TO STORE DAILY TRANSAC LIMITS

# the slides say "A newly created account must have a new unused account number"
# Does that mean not being currently used or never used at all?
# If never used at all, we have to use a hashmap to store all account numbers that were used
# We currently use a hashmap following the above assumption
# Store all accounts that were ever used, alongside their balance, name, and whether or not they are activated
# accountsHash["1234567"] = 100000, John, 1
accountsHash = {}

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
        newTSF = open(str('mergedTSF.txt'), "a")
        newTSF.write("EOS 0000000 000 0000000 ***")
        newTSF.close()

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
            create(accANum, accName)
        elif action == 'DEL':
            delete()

def deposit(toAccNum, amount):
    accountActive = accountsHash[toAccNum][2]
    if accountActive == 1:
        if amount <= 200000:
            checkLimit = dailyDepLimit[toAccNum] + amount
            if checkLimit <= 500000:
                newBal = accountsHash[toAccNum][0] + amount
                accountsHash[toAccNum] = newBal, accountsHash[toAccNum][1], 1
                dailyDepLimit[toAccNum] = dailyDepLimit[toAccNum] + amount
            else:
                print("Exceeded daily deposit limit")
        else:
            print("Exceeded single deposit limit")
    else:
        print("Account(s) do not exist")


def withdraw(fromAccNum, amount):
    accountActive = accountsHash[fromAccNum][2]
    if accountActive == 1:
        if amount <= 100000:
            checkLimit = dailyWithLimit[fromAccNum] + amount
            if checkLimit <= 500000:
                newBal = accountsHash[fromAccNum][0] - amount
                if newBal >= 0:
                    accountsHash[fromAccNum] = newBal, accountsHash[fromAccNum][1], 1
                    dailyWithLimit[fromAccNum] = dailyDepLimit[fromAccNum] + amount
                else:
                    print("Error - insufficient funds")
            else:
                print("Exceeded daily withdraw limit")
        else:
            print("Exceeded single withdraw limit")
    else:
        print("Account(s) do not exist")


def transfer(toAccNum, amount, fromAccNum):
    accountInActive = accountsHash[toAccNum][2]
    accountOutActive = accountsHash[fromAccNum][2]
    if accountInActive == 1 and accountOutActive == 1:
        if amount <= 1000000:
            # Note: there is only a limit for transferring OUT of an account
            checkLimit = dailyTransfLimit[fromAccNum] + amount
            if checkLimit <= 1000000:
                newOutBal = accountsHash[fromAccNum][0] - amount
                if newOutBal >= 0:
                    accountsHash[fromAccNum] = newOutBal, accountsHash[fromAccNum][1], 1
                    dailyTransfLimit[fromAccNum] = dailyTransfLimit[fromAccNum] + amount
                else:
                    print("Error - insufficient funds")
                newInBal = accountsHash[toAccNum][0] + amount
                accountsHash[toAccNum] = newInBal, accountsHash[toAccNum][1], 1
            else:
                print("Exceeded daily transfer limit")
        else:
            print("Exceeded single transfer limit")
    else:
        print("Account(s) do not exist")

def initializeHash()
    maf = open("MAF.txt", "r")
    lines = maf.readlines()
    for line in lines:
        mafLine = line.split(" ", 2)
        mafAccNum = mafLine[0]
        mafAccBal = mafLine[1]
        mafAccName = mafLine[2]
        # Associate account name with account number
        accountsHash[mafAccNum] = mafAccBal, mafAccName, 1
    maf.close()

def create(accNum, accName):
    if accNum not in accountsHash:
        accountsHash[accNum] = 000, accName, 1

def delete(accNum, accName):
    if accNum in accountsHash:
        if accountsHash[accNum][1] == accName:
            # Set the balance of the deleted account to 0
            accountsHash[accNum] = 000, accountsHash[accNum][1], 0

#mainline
clearMasterTSF()
mergeTSF()
handleTSF()

def main():
    initializeHash()



if __name__ == "__main__":
    main()
