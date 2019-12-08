import subprocess
import transaction

# If you just want to run the test script for 1 day by dailyScript.py
def singleRun():
	open('mergedTSF.txt', 'w').close()
	#run front end for 3 daily transactions
	transaction.transaction(test_id='1a')
	transaction.transaction(test_id='1b')
	transaction.transaction(test_id='1c')
	mTSF = open('mergedTSF.txt', 'a')
	mTSF.write("EOS " + "0000000" + " " + "000" + " " + "0000000" + " " + "***\n") # extra final EOS line after concat based on backend requirements
	mTSF.close()
	#run back end to process transactions
	subprocess.call("python backendSourceCode.py newMAF.txt mergedTSF.txt")

# runs weekly script code
def dailyScript(dayNumber, numberSessions):
	open('mergedTSF.txt', 'w').close()
	if dayNumber <= 5:
		#run 3 transactions per day
		transaction.transaction(test_id = str(dayNumber)+'a')
		transaction.transaction(test_id = str(dayNumber)+'b')
		transaction.transaction(test_id = str(dayNumber)+'c')
		if int(numberSessions) >3: # run any extra transactions dynamically based on user input
			for i in range(0,int(numberSessions)-3):
				print("Starting new session...")
				subprocess.call("python frontendSourceCodeSingleDay.py " + "newVAF.txt " + "TTSF" + str(dayNumber)+ chr(ord('a') + i + int(numberSessions) - 1) + ".txt")

	else:
		print("Error! cannot run for more than 5 days")

	mTSF = open('mergedTSF.txt', 'a')
	mTSF.write("EOS " + "0000000" + " " + "000" + " " + "0000000" + " " + "***\n") # extra final EOS line after concat based on backend requirements
	mTSF.close()
	#run backend at end of day
	subprocess.call("python backendSourceCodeSingleDay.py " + "newMAF" + "day" + str(dayNumber-1) + ".txt mergedTSF.txt " + str(dayNumber))

# runs once
if __name__== "__main__":
	singleRun()
