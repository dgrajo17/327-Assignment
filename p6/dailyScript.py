import subprocess
import transaction

transaction.transaction(test_id='1a')
transaction.transaction(test_id='1b')
transaction.transaction(test_id='1c')
subprocess.call("python backendSourceCode.py newMAF.txt mergedTSF.txt")