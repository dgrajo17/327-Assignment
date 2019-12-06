#p4 - 327

#handle the actions that are on the new tsf
import sys

# Main class that implements the back office, takes in 2 files as arguments and outputs 2 files
class BackOffice:
	def __init__(self):
		self.MAF = sys.argv[1] # Master Account File from command line
		self.mergedTSF = sys.argv[2]  #Merged TSF from command line
		self.accountsHash = self.initializeHash()
	
	'''
	def mergeTSF(self):
		print ('hello world')
		tsfLIST = 3
		newTSF = open(str('mergedTSF.txt'),"a")
		newTSF.write('\n')
		newTSF.close()
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
		newTSF.write("EOS 0000000 000 0000000 ***")
		newTSF.close()
	'''

		
	# Goes through merged TSF and performs the updates specified in the lines by calling
	# relevant methods  
	def handleTSF(self):
		tsf = open(self.mergedTSF, 'r')
		lines = tsf.readlines()
		for line in lines:
			tsfLine = line.split(" ", 4)
			action = tsfLine[0]
			accANum = tsfLine[1]
			amount = int(tsfLine[2]) # Convert to int for easier processing
			accBNum = tsfLine[3]
			accName = tsfLine[4].rstrip()
			if action == 'DEP':
				self.deposit(accANum, amount)
			elif action == 'WDR':
				self.withdraw(accANum, amount)
			elif action == 'XFR':
				self.transfer(accANum, amount, accBNum)
			elif action == 'NEW':
				self.create(accANum, accName)
			elif action == 'DEL':
				self.delete(accANum, accName)
				
	# Attempts to deposit an amount to an account 
	def deposit(self,toAccNum, amount):
		if toAccNum in self.accountsHash:
			accountActive = self.accountsHash[toAccNum][2]
		else:
			accountActive = 0
		if accountActive == 1:
			newBal = self.accountsHash[toAccNum][0] + amount
			# If line length of 47 characters not exceeded with addition
			if len(str(toAccNum) + ' ' + str(newBal) + ' ' + str(self.accountsHash[toAccNum][1])) <= 47:
				self.accountsHash[toAccNum] = [newBal, self.accountsHash[toAccNum][1].rstrip(), 1]		
			else:
				print("Failed Constraint: Deposit failed due to amount limit being reached")
		else:
			print("Failed Constraint: Account was deleted")

	# Attempts to withdraw an amount from an account 
	def withdraw(self, fromAccNum, amount):
		if fromAccNum in self.accountsHash:
			accountActive = self.accountsHash[fromAccNum][2]
		else:
			accountActive = 0
		if accountActive == 1:
			newBal = self.accountsHash[fromAccNum][0] - amount
			if newBal >= 0:
				self.accountsHash[fromAccNum] = [newBal, self.accountsHash[fromAccNum][1].rstrip(), 1]
			else:
				print("Failed Constraint: insufficient funds")

		else:
			print("Failed Constraint: Account was deleted")

	# Attempts to transfer an amount between accounts 
	def transfer(self, toAccNum, amount, fromAccNum):
		if toAccNum in self.accountsHash and fromAccNum in self.accountsHash:
			accountInActive = self.accountsHash[toAccNum][2]
			accountOutActive = self.accountsHash[fromAccNum][2]
		else:
			accountInActive = 0
		if (accountInActive == 1) and (accountOutActive == 1):
			newOutBal = self.accountsHash[fromAccNum][0] - amount
			if newOutBal >= 0:
				newInBal = self.accountsHash[toAccNum][0] + amount
				# If line length of 47 characters not exceeded with addition
				if len(str(toAccNum) + ' ' + str(newInBal) + ' ' + str(self.accountsHash[toAccNum][1])) <= 47:
					self.accountsHash[fromAccNum] = [newOutBal, self.accountsHash[fromAccNum][1], 1]
					self.accountsHash[toAccNum] = [newInBal, self.accountsHash[toAccNum][1].rstrip(), 1]
				else:
					print("Failed Constraint: Receiving failed due to amount limit being reached")
			else:
				print("Failed Constraint: Insufficient funds in sending account")

		else:
			print("Failed Constraint: At least one of the accounts was already deleted")
	
	# Creates an account 
	def create(self, accNum, accName):
		#if accNum not in self.accountsHash:
		self.accountsHash[accNum] = [0, accName.rstrip(), 1]
	
	# Deletes an account by setting amount to 0 and valid bit to 0
	def delete(self, accNum, accName):
		if accNum in self.accountsHash:
			if self.accountsHash[accNum][1] == accName:
				# Set the balance of the deleted account to 0
				self.accountsHash[accNum] = [0, self.accountsHash[accNum][1].rstrip(), 0]
			else:
				print("Failed Constraint: Could not delete account due to incorrect name")
		else:
			print("Failed Constraint: Account does not exist")

	# Creates an updated version of the MAF after doing all updates
	def createNewMAF(self):
		# Create new maf 
		newMaf = open('newMAF.txt', 'w+')
		for i in sorted (self.accountsHash) : 
			balance = str(self.accountsHash[i][0])
			# Increase length of the amount to be at least 3 digits like 000
			while len(balance) < 3:
				balance = '0' + balance
			newMaf.write(i + ' ' + balance + ' ' + str(self.accountsHash[i][1]) + '\n')		
			

	# Create new VAF from only valid accounts
	def createNewVAF(self):
		# Create new vaf 
		newVAF = open('newVAF.txt', 'w+')
		for i in sorted (self.accountsHash) : 
			# Only write to new VAF
			if self.accountsHash[i][2] == 1:
				newVAF.write(i + '\n')		

	# Initilize hash table using MAF to dynamically keep track and update account details
	def initializeHash(self):
		accountsHash = {}
		maf = open(self.MAF, "r")
		lines = maf.readlines()
		for line in lines:
			mafLine = line.split(" ", 2)
			mafAccNum = mafLine[0]
			mafAccBal = mafLine[1]
			mafAccName = mafLine[2]
			# Associate account name with account number
			accountsHash[mafAccNum] = [int(mafAccBal), mafAccName,1] # Last digit is valid bit
		maf.close()
		return accountsHash
	

# The main function creates a back office object which takes in the old Master Accounts file
# and the merged TSF, and goes through the tsf and does all updates and creates an updated
# MAF and a new VAF


def main():
	backOfficeObject = BackOffice()
	#backOfficeObject.mergeTSF()
	backOfficeObject.handleTSF()
	backOfficeObject.createNewMAF()
	backOfficeObject.createNewVAF()
	
if __name__ == "__main__":
    main()
