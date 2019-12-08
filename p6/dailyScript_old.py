import subprocess
import transaction

#run front end for 3 daily transactions
transaction.transaction(test_id='1a')
transaction.transaction(test_id='1b')
transaction.transaction(test_id='1c')
#run back end to process transactions
subprocess.call("python backendSourceCode.py newMAF.txt mergedTSF.txt")