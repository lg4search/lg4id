# lg4id
#G4 kissing

The algorithm checks for "GGG" and "CCC" sequences in 1500 bp sliding windows. Each "G" and "C" may only contibute to one match. For example "GGGGGG" is counted as two "GGG", not four. Bins with 121 or more GGG or CCC (not the sum of GGG and CCC in the bin) are valid LG4. Contiguous valid LG4 are merged into longer segments which are returned to the user. You can access the user interface here http://omnisearch.soc.southalabama.edu:8080/g4search.

The 'driver' method in quadsearch_modified.py needs to be called to obtain the desired result. 

To run the "quadSearch_modified.py" as a standalone script, below are the instructions, with each instruction followed by the steps.

1. Install Python 3.7 and make sure you add it to your system path.

Steps: 
i. Python programming language is free and open-source. To download, please visit the following link: https://www.python.org/downloads/. The version we will be using is the latest version available in the link above. At the time of this writing its, 3.74. For operating systems other than windows, try to get at least version 3.5 or above (Usually, apt get install python version should work or you should
compile it from the source).
ii. After the installation, to make sure it is installed correctly, open the command prompt→ enter “python” and click Enter.
Then you should see the Python console in your command prompt. If you get an error
“python” is not recognized as an internal command, add the path to the python
executable into the System Path.
Linux users: https://realpython.com/installing-python/ Follow this article if you
have any questions.
Mac Users: https://docs.python-guide.org/starting/install3/osx/ Follow this if you
get any unexpected errors.

2. Install the required modules to run the program in your computer.

Steps: 
i. We can’t even imagine Python without its enormous number of modules or simple packages. Its actually quite easy to install modules in python. With Python, comes its amazing module installer, the “pip”. Open a new command prompt window without the python console, and enter “pip”. Windows users shouldn’t get any error. But Linux users might because they need to install the pip separately.
Follow this link if you have errors with the pip command:
https://www.makeuseof.com/tag/install-pip-for-python/.

ii. The modules we will be installing are: 1. re 2. bitarray 3. itertools
Go ahead and enter the following commands in a command prompt to install each of the above modules
a) pip install re
b) pip install bitarray
c) pip install itertools

With pip, python installed correctly, no errors should be encountered.

3. Now download the python code, "quadSearch_modified.py" and "input_filenames.txt" and place these files in a fresh folder in your computer (So that the newly created files are not mixed up with your existing files)

4. Open the input_filenames.txt and add the filenames to be analyzed one in each line along with the extension. All the files must be FASTA formatted i.e., each sequence in a file need to be preceded by a header starting with the symbol ">". Each file can have any number of Fasta formatted sequences and Any number of files can be inputted using the input_filenames.txt. We took care that your computer doesn't get out of memory even too many files are inputted (We only process one file and one seq at any moment). 

File name examples (What can be entered into input_filenames.txt).

Path/to/Homo_sapiens.GRCh38.dna.chromosome.22.fa
Path/to/Homo_sapiens.GRCh38.dna.chromosome.21.fa

If the input files are in the same folder as the python script, the path can be skipped as shown below. But each file MUST have an extension such as .fa or .txt or .fasta etc.

 Homo_sapiens.GRCh38.dna.chromosome.22.fa/
 Homo_sapiens.GRCh38.dna.chromosome.21.fa/

5. Now since the input to the program is ready, Open a command prompt window and navigate to the folder with the python script in the command prompt. (Can be done using the command "cd path/to/folder").

6. Once you are in the folder, enter the command "python quadSearch_modified.py" and click enter to run the program.

7. The results will be directly written into files (one for each input) and are saved in the same folder as the python script.

Please contact us if you were to face any issues @ lg4search@gmail.com. Thank you for your time!!


