#p4 - 327

def clearMasterTSF():
	open('masterTSF.txt', 'w').close()
	
def mergeTSF():
	for i in (tsfLIST):
		tsf = open(str(tsfLIST+i),"r")
		lines = tsf.readlines()
		for line in lines:
			newtsf = open(str('masterTSF.txt'),"a")
			if line != '':
				if line[:3] != 'EOS':
					newtsf.write(line)
			newtsf.close()
		tsf.close()

def handleTSF():
	tsf = open('masterTSF.txt', 'r')
	lines = tsf.readlines()
	for line in lines:
		action = line[:3]
		if action == 'DEP':
            deposit()
		elif action == 'WDR':
			withdraw()
		elif action == 'XFR':
			transfer()
		elif action == 'NEW':
			create()
		elif action == 'DEL':
			delete()
		
#mainline
clearMasterTSF()
mergeTSF()
handleTSF()