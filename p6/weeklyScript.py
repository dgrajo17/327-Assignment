import subprocess
import transaction

#runs 5 days to simulate a week
for i in range (1,6):
    #run 3 transactions per day
    transaction.transaction(test_id = str(i)+'a')
    transaction.transaction(test_id = str(i)+'b')
    transaction.transaction(test_id = str(i)+'c')
    #run backend at end of day
    subprocess.call("python backendSourceCode.py newMAF.txt mergedTSF.txt")