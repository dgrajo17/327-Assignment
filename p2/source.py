#CMPE 327 Assignment Part 2
status = ''

def handleKeyboardInput():
    action = raw_input("What would you like to do?")
    print(action)
    #process input

def createAccount():
    global status
    if status == 'agent':
        valid = isAccNumValid(accNum)
        if valid == 1:
            valid = isAccNameValid(accName)
    else:
        print('Status must be set to AGENT.')

def isAccNumValid(accNum):
    #check valid

def isAccNameValid(accName):
    #check valid



#mainline
while(1):
    handleKeyboardInput()