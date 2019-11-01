import pytest
import tempfile
from importlib import reload
import os
import io
import sys
from p3 import SourceCode


path = os.path.dirname(os.path.abspath(__file__))


def test_r1a(capsys):
    """Testing r2. All required information stored in folder r2. 

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helperNoTSF(
        capsys=capsys,
        test_id='1a'
    )

def test_r1b(capsys):
    """Testing r2. All required information stored in folder r2.

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helperNoTSF(
        capsys=capsys,
        test_id='1b'
    )


def test_r2a(capsys):
    """Testing r2. All required information stored in folder r2.

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helperNoTSF(
        capsys=capsys,
        test_id='2a'
    )


def test_r3a(capsys):
    """Testing r2. All required information stored in folder r2.

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helperNoTSF(
        capsys=capsys,
        test_id='3a'
    )


def test_r3b(capsys):
    """Testing r2. All required information stored in folder r2.

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """
    helper(
        capsys=capsys,
        test_id='3b'
    )

def helper(
        capsys,
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # cleanup package
    #reload(app)

    # locate test case folder:
    case_folder = os.path.join(path, test_id)

    # concatenate test_id with .txt
    test_id_txt = test_id + ".txt"

    # concatenate test_id_txt with o
    out_test_id_txt = "o" + test_id_txt

    # concatenate test_id with o, _TSF and .txt
    out_tsf_test_id_txt = "o" + test_id + "_TSF.txt"

    # read terminal input:
    with open(
        os.path.join(
            case_folder, test_id_txt)) as rf:  # REPLACE NAME HERE
        terminal_input = rf.read().splitlines()

    # read expected tail portion of the terminal output:
    with open(
        os.path.join(
            case_folder, out_test_id_txt)) as rf:  #REPLACE NAME HERE
        terminal_output_tail = rf.read().splitlines()

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # prepare program parameters
    sys.argv = ['SourceCode.py',
        os.path.join(case_folder, 'vaf.txt'),
        transaction_summary_file]

    # set terminal input
    sys.stdin = io.StringIO(
        '\n'.join(terminal_input))

    # run the program
    #app.main()
	
    SourceCode.main()
    #os.system("python ImprovedCodeWithClasses.py " + sys.argv[1] + " "+ sys.argv[2])
    #subprocess.run("python ImprovedCodeWithClasses.py " + sys.argv[1] + " "+ sys.argv[2])
    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()
    
    # compare terminal outputs at the end.`
    for i in range(1, len(terminal_output_tail)+1):
        index = i * -1
        print(index)
        print(terminal_output_tail[index])
        print(out_lines[index])
        assert terminal_output_tail[index] == out_lines[index]

    # compare transactions:
    with open(transaction_summary_file, 'r') as of:
        content = of.read()
        with open(os.path.join(case_folder, out_tsf_test_id_txt), 'r') as exp_file_of:
            expected_content = exp_file_of.read()
            print("Content")
            print(content)
            print("expected")
            print(expected_content)
            assert content == expected_content

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)


def helperNoTSF(
        capsys,
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # cleanup package
    # reload(app)

    # locate test case folder:
    case_folder = os.path.join(path, test_id)

    # concatenate test_id with .txt
    test_id_txt = test_id + ".txt"

    # concatenate test_id_txt with o
    out_test_id_txt = "o" + test_id_txt

    # read terminal input:
    with open(
            os.path.join(
                case_folder, test_id_txt)) as rf:  # REPLACE NAME HERE
        terminal_input = rf.read().splitlines()

    # read expected tail portion of the terminal output:
    with open(
            os.path.join(
                case_folder, out_test_id_txt)) as rf:  # REPLACE NAME HERE
        terminal_output_tail = rf.read().splitlines()

    # create a temporary file in the system to store output transactions
    temp_fd, temp_file = tempfile.mkstemp()
    transaction_summary_file = temp_file

    # prepare program parameters
    sys.argv = ['SourceCode.py',
                os.path.join(case_folder, 'vaf.txt'),
                transaction_summary_file]

    # set terminal input
    sys.stdin = io.StringIO(
        '\n'.join(terminal_input))

    # run the program
    # app.main()

    SourceCode.main()
    # os.system("python ImprovedCodeWithClasses.py " + sys.argv[1] + " "+ sys.argv[2])
    # subprocess.run("python ImprovedCodeWithClasses.py " + sys.argv[1] + " "+ sys.argv[2])
    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs at the end.`
    for i in range(1, len(terminal_output_tail) + 1):
        index = i * -1
        assert terminal_output_tail[index] == out_lines[index]

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)