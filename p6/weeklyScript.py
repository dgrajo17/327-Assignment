import subprocess
import transaction
import dailyScript

#runs 5 days to simulate a week
open('newVAF.txt', 'w').close() # empty VAF
open('newMAFday0.txt', 'w').close() # empty MAF 

automatic = input("Input 1 to automatically run script or 0 to be able to input commands\n")
if int(automatic) == 1:
	for i in range (1,6):
		dailyScript.dailyScript(i, 3)
else:
	for i in range (1,6):
		val = input("How many sessions do you want? 3 Minimum. First 3 will be automatic: ")
		if int(val) >3:
			dailyScript.dailyScript(i, val)
		else:
			print("Input too small, 3 automatic sessions ran")
			dailyScript.dailyScript(i, 3)