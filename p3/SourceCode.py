# 327 QUINTERAC Front End Rapid Prototype (Assignment 2)
# The Xtreme Team
# Oct 18, 2019

import re
import sys
import os


# Contains useful functions of processing the validity and presence of account numbers and names and holds and updates account information
class Accounts:

    def accNumDecOnly(self, string):
        restricted = re.compile(r'[^0-9]')
        string = restricted.search(string)
        return not bool(string)

    # check if account num is valid
    def accNumValid(self, accNum, error):
        if len(accNum) == 7:  # length must be 7
            # print("7")
            if accNum[0] != "0":  # must not begin with zero
                # print("8")
                if self.accNumDecOnly(accNum) == True:
                    # print("9")
                    return 1
                else:
                    error.errorMsg("Account number must be decimals only")
                    return 0
            else:
                error.errorMsg("Account number must not begin with a 0")
                return 0
        else:
            error.errorMsg("Account number must be 7 decimals long")
            return 0

    # see if account number exists in vaf file using constant time search
    def accNumExists(self, accNum, accountsList):
        exists = 0
        # Constant time check in dictionairy for account number
        if accNum in accountsList:
            exists = 1
        return exists

    # get account balance and daily transaction information an account
    # Transaction type 1= deposit, 2 = withdraw, 3 = transfer
    def getAccBalance(self, accNum, transactionType, backendDict):
        dailyAmount = []
        amount = backendDict[accNum].amount
        dailyAmount.append(backendDict[accNum].dailyAmountDeposit)
        dailyAmount.append(backendDict[accNum].dailyAmountWithdraw)
        dailyAmount.append(backendDict[accNum].dailyAmountTransfer)
        return amount, dailyAmount[transactionType - 1]

    # Update the amount you have put in or withdraw after a transaction for a specific account
    # And update the daily amount you have used for each type of transaction
    def updateDailyAmount(self, accNum, amount, transactionType, backendDict):
        backendDict[accNum].amount += amount
        if transactionType == 1:
            backendDict[accNum].dailyAmountDeposit += amount
        elif transactionType == 2:
            backendDict[accNum].dailyAmountWithdraw += amount
        else:
            backendDict[accNum].dailyAmountTransfer += amount

    # see if account name contains only alphanumeric characters
    def accNameAlphaNum(self, string):
        restricted = re.compile(r'[^a-zA-Z0-9" "]')
        string = restricted.search(string)
        return not bool(string)

    # see if account name is valid
    def accNameValid(self, accName, error):
        if len(accName) >= 3 and len(accName) <= 30:  # make sure name is correct length
            # print("10")
            if (accName[0] != " ") and (accName[-1] != " "):  # must start and end with acceptable characters
                # print("11")
                if self.accNameAlphaNum(accName) == True:
                    return 1
                else:
                    error.errorMsg("Alphanumeric characters only for account name")
                    return 0
            else:
                error.errorMsg("Account name cannot start or end with a space/blank character")
                return 0
        else:
            error.errorMsg("Account name should be 3-30 alphanumeric characters long")
            return 0


# Prints error messages
class Error:
    # ERROR MESSAGES
    def invalidInputA(self):
        print("Invalid input")

    # ERROR MESSAGES
    def invalidInputB(self, inputAction):
        print("Invalid input: " + inputAction)

    # ERROR MESSAGES
    def errorMsg(self, error):
        print(error)


# Class takes user inputs and handles actions like loggining in and depositing
# It keeps the state of the program for the day (mode, valid accounts list, transaction message to write)
#  and ensures only valid inputs and state transitions are allowed
class Actions:
    def __init__(self):
        self.accountsList = dict()  # Use hashtable so that finding account number is constant time
        self.toWrite = []  # Transaction file statements to write after logout statement is executed
        self.backendDict = dict()  # temporary backend dictionary only for testing frontend
        self.status = "logout"  # Current status of the program
        self.error = Error()  # Error object for printing error messages
        self.account = Accounts()  # Accounts object for processing account names and numbers
        self.vafFileName = sys.argv[1]  # First command line argument, name of vaf file
        self.tsfFileName = sys.argv[2]  # Second command line argument, name of tsf file

    # handle input from user
    def handleKeyboardInput(self):
        #action = input("Enter command: ")
        action = input()
        # take input, pass to action handler
        valid = self.actionHandler(action)
        if valid == 0:
            self.error.invalidInputB(action)

    # login at beginning of session and initialize accounts and balances for the day
    def login(self):
        # set status to login
        self.status = "login"
        print("Status: " + self.status)
        # Read the valid accounts file -> replace demofile.txt with valid accounts file
        global vaf
        vaf = open(self.vafFileName, "r")
        self.toWrite.clear()  # Clear statements to write to tsf
        # Clear and initialize new hashtable/dictionairy
        # This ensures that only accounts present at login will allow transactions even if new ones are added
        self.accountsList.clear()
        self.backendDict.clear()
        vaf.seek(0)
        for x in vaf:
            self.accountsList[x.strip()] = 0
            self.backendDict[x.strip()] = Backend()

    # logout method, logs out and writes all of the days transactions to the TSF
    def logout(self):
        # set status to logout and write to tsf
        self.status = "logout"
        #print("Status: " + self.status)
        vaf.close()
        tsf = open(str(self.tsfFileName), "w+")  # Using "a" will append, "w" will overwrite
        for entry in self.toWrite:
            tsf.write(entry)
        tsf.write(
            "EOS " + "0000000" + " " + "000" + " " + "0000000" + " " + "***\n")  # end the tsf with an EOS transaction code (append to end)
        # Print TSF
        tsf.seek(0)
        #for line in tsf:
        #    print(line)
        # Close TSF
        tsf.close()
        #print("\nWelcome")
        print("Please Login to Begin Transactions")  # Added to ensure user knows that they should login

    # set status to ATM when specified
    def setatm(self):
        self.status = "atm"
        print("Status: " + self.status)

    # set status to AGENT when specified
    def setagent(self):
        self.status = "agent"
        print("Status: " + self.status)

    # create a new account
    def createAccount(self, action):
        inputCommand = action.split(" ", 2);
        # Make sure length is 3 to avoid crashes (createacc, num, name)
        if len(inputCommand) == 3:
            accNum = inputCommand[1]
            accName = inputCommand[2]
            if self.account.accNumValid(accNum,
                                        self.error) == 1:  # see if proposed account number meets all restrictions
                if self.account.accNumExists(accNum,
                                             self.accountsList) == 0:  # see if proposed account name meets all restrictions
                    if self.account.accNameValid(accName, self.error) == 1:
                        #print("12")
                        # write new account to VAF
                        vaf1 = open(str(self.vafFileName), "r")  # "a" will append, "w" will overwrite
                        lines = vaf1.readlines()
                        vaf1.close()
                        vaf1 = open(str(self.vafFileName), "w")
                        for line in lines:
                            if line.strip(
                                    "\n") != "0000000":  # temporarily update VAF without using backend, will be removed when back end is programmed
                                vaf1.write(line)
                        vaf1.close()
                        vaf1 = open(str(self.vafFileName), "a")
                        vaf1.write(accNum)
                        vaf1.write("\n" + "0000000")
                        vaf1.close()
                        # Save to tsf file
                        self.toWrite.append("NEW " + accNum + " " + "000" + " " + "0000000" + " " + accName + "\n")
                        print("Transaction Complete (Create Account)")
                        #print("Account " + accNum + " created successfully.")
                        return 1
                    else:
                        return 0
                else:
                    self.error.errorMsg("Account number exists")
                    return 0
            else:
                return 0
        else:
            self.error.errorMsg("Not enough arguments. Please follow the format: createAccount 1234567 AccountName")
            return 0

    # delete an existing account
    def deleteAccount(self, action):
        inputCommand = action.split(" ", 2);
        # Make sure length is 3 to avoid crashes (del, num, name)
        if len(inputCommand) == 3:
            accNum = inputCommand[1]
            accName = inputCommand[2]
            if self.account.accNumValid(accNum, self.error) == 1:  # make sure account number is valid
                if self.account.accNumExists(accNum, self.accountsList) == 1:  # make sure account name is valid
                    if self.account.accNameValid(accName, self.error) == 1:
                        # print("12")
                        # delete the account successfully, write to VAF
                        vaf1 = open(str(self.vafFileName), "r")  # "a" will append, "w" will overwrite
                        lines = vaf1.readlines()
                        vaf1.close()
                        vaf1 = open(str(self.vafFileName), "w")
                        for line in lines:
                            if line.strip("\n") != str(
                                    accNum):  # temporarily update VAF without using backend, will be changed
                                vaf1.write(line)
                        vaf1.close()
                        # Save to tsf file
                        self.toWrite.append("DEL " + accNum + " " + "000" + " " + "0000000" + " " + accName + "\n")
                        del self.accountsList[
                            accNum]  # Delete account from valid accounts list so that you can't do transactions on it
                        #print("Account " + accNum + " deleted successfully.")
                        print("Transaction Complete (Delete Account)")
                        return 1
                    else:
                        return 0
                else:
                    self.error.errorMsg("Account number does not exist")
                    return 0
            else:
                return 0
        else:
            self.error.errorMsg("Not enough arguments. Please follow the format: deleteAccount 1234567 AccountName")
            return 0

    # deposit to an existing account
    def deposit(self, action):
        if self.status == "atm":
            limit = 200000  # from assignment requirements
        elif self.status == "agent":
            limit = 99999999  # from assignment requirements
        else:
            return 0
        inputCommand = action.split(" ", 2);
        # Make sure length is 3 to avoid crashes (dep, num, amount)
        if len(inputCommand) == 3:
            accNum = inputCommand[1]
            amount = inputCommand[2]
            if self.account.accNumValid(accNum,
                                        self.error) == 1:  # make sure account number is valid ... i don't think we need this one, all it changes is error message
                if self.account.accNumExists(accNum, self.accountsList) == 1:  # make sure account actually exists
                    if self.account.accNumDecOnly(amount) == True:  # make sure amount is valid
                        currentAmount, dailyAmount = self.account.getAccBalance(accNum, 1, self.backendDict)
                        if int(amount) <= min(limit, currentAmount, (500000 - dailyAmount)):
                            self.toWrite.append(
                                "DEP " + accNum + " " + amount + " " + "0000000" + " " + "***" + "\n")
                            self.account.updateDailyAmount(accNum, int(amount), 1, self.backendDict)
                            print("Transaction Complete (Deposit)")
                        else:
                            self.error.errorMsg("Amount exceeds the deposit limit")
                            return 0
                    else:
                        self.error.errorMsg("Amount should be decimals only")
                        return 0
                else:
                    self.error.errorMsg("Account number does not exist")
                    return 0
            else:
                return 0
        else:
            self.error.errorMsg("Not enough arguments. Please follow the format: deposit accountNumber amount")
            return 0

    def withdraw(self, action):
        if self.status == "atm":
            limit = 100000  # from assignment requirements
        elif self.status == "agent":
            limit = 99999999  # from assignment requirements
        else:
            return 0
        inputCommand = action.split(" ", 2);
        # Make sure length is 3 to avoid crashes
        if len(inputCommand) == 3:  # (wdr, accnum, amount)
            accNum = inputCommand[1]
            amount = inputCommand[2]
            if self.account.accNumValid(accNum, self.error) == 1:  # not sure we need this, see deposit
                if self.account.accNumExists(accNum,
                                             self.accountsList) == 1:  # make sure acc number exists THIS IS THE IMPORTANT CHECK
                    if self.account.accNumDecOnly(amount) == True:  # make sure amount is decimal
                        currentAmount, dailyAmount = self.account.getAccBalance(accNum, 2, self.backendDict)
                        if int(amount) <= min(limit, currentAmount,
                                              (500000 - dailyAmount)):  # check all restrictions
                            self.toWrite.append(
                                "WDR " + accNum + " " + amount + " " + "0000000" + " " + "***" + "\n")
                            self.account.updateDailyAmount(accNum, int(amount), 2, self.backendDict)
                            print("Transaction Complete (Withdraw)")
                        else:
                            self.error.errorMsg("Amount exceeds the withdrawal limit.")
                            return 0
                    else:
                        self.error.errorMsg("Amount should be decimals only")
                        return 0
                else:
                    self.error.errorMsg("Account number does not exist")
                    return 0
            else:
                return 0
        else:
            self.error.errorMsg("Not enough arguments. Please follow the format: withdraw accountNumber amount")
            return 0

    def transfer(self, action):
        if self.status == "atm":
            limit = 1000000  # from assignment requirements
        elif self.status == "agent":
            limit = 99999999  # from assignment requirements
        else:
            return 0
        inputCommand = action.split(" ", 3);
        # Make sure length is 3 to avoid crashes
        if len(inputCommand) == 4:  # (xfr, accnumout, accnumin, amount)
            accNumOut = inputCommand[1]
            accNumIn = inputCommand[2]
            amount = inputCommand[3]
            if self.account.accNumValid(accNumOut,
                                        self.error) == 1:  # make sure all account numbers exist and are valid - may not need all these, see deposit
                if self.account.accNumExists(accNumOut, self.accountsList) == 1:
                    if self.account.accNumValid(accNumIn, self.error) == 1:
                        if self.account.accNumExists(accNumIn, self.accountsList) == 1:
                            if accNumOut != accNumIn:
                                if self.account.accNumDecOnly(amount) == True:
                                    if len(amount) >= 3 and len(
                                            amount) <= 8:  # are these supposed to be <= or just < ???
                                        currentAmount, dailyAmount = self.account.getAccBalance(accNumOut, 3,
                                                                                                self.backendDict)  # get account information
                                        if int(amount) <= min(limit, currentAmount, (
                                                1000000 - dailyAmount)):  # check all restrictions to make sure account has money to withdraw
                                            self.toWrite.append(
                                                "XFR " + accNumIn + " " + amount + " " + accNumOut + " " + "***" + "\n")
                                            self.account.updateDailyAmount(accNumOut, int(amount), 3, self.backendDict)
                                            print("Transaction Complete (Transfer)")

                                        else:
                                            self.error.errorMsg("Amount exceeds the withdrawal limit.")
                                            return 0
                                    else:
                                        self.error.errorMsg("Amount should be between 3 and 8 decimal digits")
                                        return 0
                                else:
                                    self.error.errorMsg("Amount should be decimals only")
                                    return 0
                            else:
                                self.error.errorMsg("Account numbers shouldn't be the same")
                                return 0
                        else:
                            self.error.errorMsg("First account number does not exist")
                            return 0
                    else:
                        return 0
                else:
                    self.error.errorMsg("Account number does not exist")
                    return 0
            else:
                return 0
        else:
            self.error.errorMsg(
                "Not enough arguments. Please follow the format: transfer accountNumberFrom accountNumberTo amount")
            return 0


    def exit(self, action):
        #sys.exit()
        self.status = "exit"

    # Handle action after it is inputted and processed through keyboard input, make sure action is valid given restrictions
    def actionHandler(self, action):
        if action == "whereami":
            print("Action Handler")
            return 1
        if action == "exit":
            self.exit(action)
        if self.status == "logout":
            if action == "login":  # can only login after logout
                self.login()
                return 1
            else:
                return 0
        elif self.status == "login":
            if action == "login":
                return 0
            elif action == "logout":
                self.logout()
                return 1
            elif action == "atm":  # set to ATM mode
                self.setatm()
                return 1
            elif action == "agent":  # set to AGENT mode
                self.setagent()
                return 1
            else:
                return 0
        elif self.status == "atm":
            if action == "logout":
                self.logout()
                return 1
            elif action == "atm":  # can't do this in ATM
                return 0
            elif action == "agent":  # can't do this in ATM
                return 0
            elif "createAccount" in action:  # can't do this in ATM
                return 0
            elif "deleteAccount" in action:  # can't do this in ATM
                return 0
            elif "deposit" in action:
                self.deposit(action)
                return 1
            elif "withdraw" in action:
                self.withdraw(action)
                return 1
            elif "transfer" in action:
                self.transfer(action)
                return 1
            else:
                return 0
        elif self.status == "agent":
            if action == "logout":
                self.logout()
                return 1
            elif action == "atm":  # can't do this in AGENT
                return 0
            elif action == "agent":  # can't do this in AGENT
                return 0
            elif "createAccount" in action:  # can't do this in AGENT
                self.createAccount(action)
                return 1
            elif "deleteAccount" in action:  # can't do this in AGENT
                self.deleteAccount(action)
                return 1
            elif "deposit" in action:  # can't do this in AGENT
                self.deposit(action)
                return 1
            elif "withdraw" in action:  # can't do this in AGENT
                self.withdraw(action)
                return 1
            elif "transfer" in action:  # can't do this in AGENT
                self.transfer(action)
                return 1
            else:
                return 0


# Backend class holds the amount each account has and how much
# of the daily limit they have remaining for each transaction type
class Backend:
    def __init__(self):
        self.amount = 10000
        self.dailyAmountDeposit = 0
        self.dailyAmountWithdraw = 0
        self.dailyAmountTransfer = 0


# Main Function, runs continuously 

#           Main Description :
# The overall intention of the program is to implement all of the features of the front end
# and to provide a way to interact with the front end through a command line interface and 
# conduct full testing. Certain back end reliant features were simplified and replaced so that
# the front end could seamlessly work. Main program continuously processes user keyboard input 
# does programmed behaviour
# 1 input file vaf.txt containing a valid accounts file with any number of accounts is required in the working directory
# Accounts are added and removed from the file since backend is not coded yet
# 1 output file tsf.txt is required that is written by the program  on logout with the transaction from the day

# Run the program by typing "python SourceCode.py" along with the names of the two files mentioned above in the command line terminal 
# vaf file should be first, tsf second, no quotations needed. Should be present in the working directory 
# Shell scripts can be run on top of this program to feed  a sequence of commands into the program and to trigger running the script


def main():
    status = "logout"
    print("Welcome")
    print("Please Login to Begin Transactions")
    mainClass = Actions()  # Create object to be able to begin processing front end actions
    while 1:
        mainClass.handleKeyboardInput()
        if (mainClass.status == "exit"):
            break


if __name__ == "__main__":
    main()

