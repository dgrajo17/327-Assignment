import tempfile
import pytest
from importlib import reload
import os
import io
import sys
import backendSourceCode
import frontendSourceCode
#from subprocess import Popen, PIPE
import subprocess

path = os.path.dirname(os.path.abspath(__file__))

#subprocess.call(["frontendSourceCode.py", "vaf.txt"])
#subprocess.call(["python", "frontendSourceCode.py vaf.txt TTSF.txt"])


def transaction(
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # locate test case folder:
    case_folder = os.path.join(path, test_id)

    # concatenate test_id with .txt
    test_id_txt = test_id + ".txt"

    # read terminal input:
    with open(
            os.path.join(
                case_folder, test_id_txt)) as rf:  # REPLACE NAME HERE
        terminal_input = rf.read().splitlines()

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # prepare program parameters

    vaf = open('newVAF.txt', 'r')
    lines = vaf.readlines()
    tempvaf = open('tempVAF.txt', 'w+')
    for line in lines:
        tempvaf.write(line)
    tempvaf.close()
    vaf.close()

    sys.argv = ['frontendSourceCode.py',
                'tempVAF.txt',
                'TTSF' + test_id + '.txt']

    # set terminal input
    temp = sys.stdin
    sys.stdin = io.StringIO(
        '\n'.join(terminal_input))


    # run the program
    # app.main()
    frontendSourceCode.main()
    sys.stdin = temp
    tempTSF = open('TTSF' + test_id + '.txt', 'r')
    lines = tempTSF.readlines()
    tempTSF.close()
    mTSF = open('mergedTSF.txt', 'a')
    for line in lines:
        mTSF.write(line)
    mTSF.close()
    # clean up
    os.close(temp_fd)
    os.remove(temp_file)