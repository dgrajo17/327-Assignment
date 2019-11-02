import pytest
import tempfile
from importlib import reload
import os
import io
import sys
from p3 import SourceCode

# Overall description of changes to the test code

# Pytest was used as the primary testing tool.
# The format is similar to the one provided at https://github.com/CISC-CMPE-327/CI-Python
# The main change is that the package structure is gone for simplicity and less folders and instead there is a main directory with 
# the source code that implements the front end along with the test code that runs the tests
# There are subdirectories for each test 
# All of the subdirectories contain an input command file (with a stream of commands),
# an expected terminal output file, and a valid accounts file.
# For tests that need it, there is also an expected tsf file 
# The test code looks inside these subdirectories and uses the files for a specific test to run the test
# There is no _main_ file as it is contained in SourceCode already
# Blank _init_ file was moved to the main p3 directory
# Test method 1 was adapted as from assignment 1 the format of our tests was in files

# The test cases are tested in a similar manner. Each has a test method that calls one of two helper functions
# and specifies the folder to find all of the files needed for it
# There are two helper methods now, one for tests that do not care about TSF output and ones that do
# init_file is present
# The vaf and tsf files in the main directory are for testing the program though manual commands without pytest
# by running python SourceCode.py vaf.txt tsf.txt in the command line

# Run the code by typing pytest in the command line 

# get path
path = os.path.dirname(os.path.abspath(__file__))


# The following are all test methods that get run when pytest is called
# Some use helperNoTSF, some use helper. All pass their id to the helper
# Naming and general structure preserved from the template 

# def test_r1a(capsys):
#     """Testing 1a. All required information stored in folder 1a. 

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='1a'
#     )

# def test_r1b(capsys):
#     """Testing 1b. All required information stored in folder 1b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='1b'
#     )


# def test_r2a(capsys):
#     """Testing 2a. All required information stored in folder 2a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='2a'
#     )


# def test_r3a(capsys):
#     """Testing 3a. All required information stored in folder 3a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='3a'
#     )


# def test_r3b(capsys):
#     """Testing 3b. All required information stored in folder 3b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='3b'
#     )


# def test_r3c(capsys):
#     """Testing 3c. All required information stored in folder 3c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='3c'
#     )


# def test_r4a(capsys):
#     """Testing 4a. All required information stored in folder 4a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='4a'
#     )


# def test_r4b(capsys):
#     """Testing 4b. All required information stored in folder 4b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='4b'
#     )


# def test_r4c(capsys):
#     """Testing 4c. All required information stored in folder 4c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='4c'
#     )


# def test_r5a(capsys):
#     """Testing 5a. All required information stored in folder 5a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='5a'
#     )


# def test_r5b(capsys):
#     """Testing 5b. All required information stored in folder 5b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='5b'
#     )


# def test_r6a(capsys):
#     """Testing 6a. All required information stored in folder 6a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='6a'
#     )


# def test_r7a(capsys):
#     """Testing 7a. All required information stored in folder 7a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='7a'
#     )


# def test_r7b(capsys):
#     """Testing 7b. All required information stored in folder 7b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='7b'
#     )



# def test_r8a(capsys):
#     """Testing 8a. All required information stored in folder 8a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='8a'
#     )


# def test_r9a(capsys):
#     """Testing 9a. All required information stored in folder 9a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9a'
#     )


# def test_r9b(capsys):
#     """Testing 9b. All required information stored in folder 9b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9b'
#     )


# def test_r9c(capsys):
#     """Testing 9c. All required information stored in folder 9c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9c'
#     )

# def test_r9d(capsys):
#     """Testing 9d. All required information stored in folder 9d.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9d'
#     )

# def test_r9e(capsys):
#     """Testing 9e. All required information stored in folder 9e.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9e'
#     )

# def test_r9f(capsys):
#     """Testing 9f. All required information stored in folder 9f.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='9f'
#     )

# def test_r10a(capsys):
#     """Testing 10a. All required information stored in folder 10a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='10a'
#     )

# def test_r10b(capsys):
#     """Testing 10b. All required information stored in folder 10b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='10b'
#     )

# def test_r10c(capsys):
#     """Testing 10c. All required information stored in folder 10c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='10c'
#     )

# def test_r10e(capsys):
#     """Testing 10e. All required information stored in folder 10e.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='10e'
#     )

# def test_r11a(capsys):
#     """Testing 11a. All required information stored in folder 11a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='11a'
#     )

# def test_r11b(capsys):
#     """Testing 11b. All required information stored in folder 11b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='11b'
#     )

# def test_r12a(capsys):
#     """Testing 12a. All required information stored in folder 12a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='12a'
#     )

# def test_r13a(capsys):
#     """Testing 13a. All required information stored in folder 13a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='13a'
#     )

# def test_r13b(capsys):
#     """Testing 13b. All required information stored in folder 13b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='13b'
#     )

# def test_r14a(capsys):
#     """Testing 14a. All required information stored in folder 14a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='14a'
#     )

# def test_r14b(capsys):
#     """Testing 14b. All required information stored in folder 14b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='14b'
#     )

# def test_r15a(capsys):
    # """Testing 15a. All required information stored in folder 15a.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helper(
        # capsys=capsys,
        # test_id='15a'
    # )

# def test_r15b(capsys):
#     """Testing 15b. All required information stored in folder 15b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='15b'
#     )

# def test_r16a(capsys):
#     """Testing 16a. All required information stored in folder 16a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='16a'
#     )

# def test_r16b(capsys):
#     """Testing 16b. All required information stored in folder 16b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='16b'
#     )

# def test_r17a(capsys):
#     """Testing 17a. All required information stored in folder 17a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='17a'
#     )

# def test_r17b(capsys):
#     """Testing 17b. All required information stored in folder 17b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='17b'
#     )

# def test_r17c(capsys):
#     """Testing 17c. All required information stored in folder 17c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='17c'
#     )

# def test_r18a(capsys):
#     """Testing 18a. All required information stored in folder 18a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='18a'
#     )

# def test_r18b(capsys):
#     """Testing 18b. All required information stored in folder 18b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='18b'
#     )

# def test_r18c(capsys):
#     """Testing 18c. All required information stored in folder 18c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='18c'
#     )

# def test_r19a(capsys):
#     """Testing 19a. All required information stored in folder 19a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='19a'
#     )

# def test_r19b(capsys):
#     """Testing 19b. All required information stored in folder 19b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='19b'
#     )

# def test_r20a(capsys):
#     """Testing 20a. All required information stored in folder 20a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='20a'
#     )

# def test_r20b(capsys):
#     """Testing 20b. All required information stored in folder 20b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='20b'
#     )

# def test_r21a(capsys):
#     """Testing 21a. All required information stored in folder 21a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='21a'
#     )

# def test_r21b(capsys):
#     """Testing 21b. All required information stored in folder 21b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='21b'
#     )

# def test_r21c(capsys):
#     """Testing 21c. All required information stored in folder 21c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='21c'
#     )

# def test_r22a(capsys):
#     """Testing 22a. All required information stored in folder 22a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='22a'
#     )

# def test_r22b(capsys):
#     """Testing 22b. All required information stored in folder 22b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='22b'
#     )

# def test_r22c(capsys):
#     """Testing 22c. All required information stored in folder 22c.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helperNoTSF(
#         capsys=capsys,
#         test_id='22c'
#     )

# def test_r23a(capsys):
#     """Testing 23a. All required information stored in folder 23a.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='23a'
#     )

# def test_r23b(capsys):
#     """Testing 23b. All required information stored in folder 23b.

#     Arguments:
#         capsys -- object created by pytest to capture stdout and stderr
#     """
#     helper(
#         capsys=capsys,
#         test_id='23b'
#     )

# def test_r24a(capsys):
    # """Testing r2. All required information stored in folder r2. 

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='24a'
    # )

# def test_r24b(capsys):
    # """Testing r2. All required information stored in folder r2.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='24b'
    # )
	

	
# def r32a(capsys):
    # """Testing 32a. All required information stored in folder 32a.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='32a'
    # )
	
# def test_r33a(capsys):
    # """Testing 33a. All required information stored in folder 33a.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='33a'
    # )
# def test_r33b(capsys):
    # """Testing 33b. All required information stored in folder 33b.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='33b'
    # )
# def test_r34a(capsys):
    # """Testing 34a. All required information stored in folder 34a.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='34a'
    # )	
# def r34b(capsys):
    # """Testing 34b. All required information stored in folder 34b.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='34b'
    # )
	
# def test_r35a(capsys):
    # """Testing 35a. All required information stored in folder 35a.

    # Arguments:
        # capsys -- object created by pytest to capture stdout and stderr
    # """
    # helperNoTSF(
        # capsys=capsys,
        # test_id='35a'
    # )	
#def test_r35b(capsys):
#    """Testing 35b. All required information stored in folder 35b.
#
#    Arguments:
#        capsys -- object created by pytest to capture stdout and stderr
#    """
#    helperNoTSF(
#        capsys=capsys,
#        test_id='35b'
#    )		

# Helper function for tests with tsf
# Changes from the template are noted at specific points

def helper(
        capsys,
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

    # Change from template: There's no need to clean the package since there is no package 
	
    # locate test case folder:
    case_folder = os.path.join(path, test_id)
    # Change from template: 
	# The following was changed from template since test files follow the format of ex. 1a for input,
	# o1a for expected output, o1a_TSF for tsf 
	# The code generates the file names based on the test name rather than using the same file names for all tests
	# or manually having to enter the name for each test
	
    # concatenate test_id with .txt
    test_id_txt = test_id + ".txt"

    # concatenate test_id_txt with o
    out_test_id_txt = "o" + test_id_txt

    # concatenate test_id with o, _TSF and .txt
    out_tsf_test_id_txt = "o" + test_id + "_TSF.txt"

    # read terminal input:
    with open(
        os.path.join(
            case_folder, test_id_txt)) as rf:  
        terminal_input = rf.read().splitlines()

    # read expected tail portion of the terminal output:
    with open(
        os.path.join(
            case_folder, out_test_id_txt)) as rf: 
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

    # Runs the main function of our program (thats run in _main_). Not called app. 
	
    SourceCode.main()

    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()
    
    # Changes from template:
	# For easier understanding of results, we print the line numbers, and expected and current outputs
	# upon an assertion error to see the results more clearly (gives the complete lines) for easier debugging
	# We also print a label for the expected output so that we know which one is which when doing comparisons
	
    # compare terminal outputs at the end.`
    for i in range(1, len(terminal_output_tail)+1):
        index = i * -1
        print(index)
        print("What we expect")
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

# Functionally identically to the above but lacking the part under compare transactions since there is no tsf for these cases to compare
# Created since not all of our tests use it. 

def helperNoTSF(
        capsys,
        test_id):
    """ a helper function that test requirements for the example app

    Arguments:
        capsys -- object created by pytest to capture stdout and stderr
    """

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
	
    # capture terminal output / errors
    # assuming that in this case we don't use stderr
    out, err = capsys.readouterr()

    # split terminal output in lines
    out_lines = out.splitlines()

    # compare terminal outputs at the end.`
    for i in range(1, len(terminal_output_tail) + 1):
        index = i * -1
        print(index)
        print("What we expect")
        print(terminal_output_tail[index])
        print(out_lines[index])
        assert terminal_output_tail[index] == out_lines[index]

    # clean up
    os.close(temp_fd)
    os.remove(temp_file)
