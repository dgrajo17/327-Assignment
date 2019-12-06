import subprocess
import transaction

for i in range (1,6):
    transaction.transaction(test_id = str(i)+'a')
    transaction.transaction(test_id = str(i)+'b')
    transaction.transaction(test_id = str(i)+'c')
    subprocess.call("python backendSourceCode.py newMAF.txt mergedTSF.txt")