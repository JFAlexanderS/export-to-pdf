import csv
import glob
import os
from subprocess import call

# Iterates over every file ending in .csv
path = os.getcwd()
path += "/*.csv"
for filename in glob.glob(path):
    with open(filename, 'rb') as csvfile:
        pdfdata = csv.reader(csvfile, delimiter=' ', quotechar='|')
        iterrows = iter(pdfdata)
        next(iterrows)
        # Sets the first row of the CSV as the "key" whose values it will replace by the user information
        pdfkey = (' '.join(next(iterrows))).split("\",\"")[1:-1]
        user = 1
        for row in iterrows:
            # Pair contains the variables and the values to replaces these variables
            pair = zip(pdfkey, (' '.join(row)).split("\",\"")[1:-1])
            # Iterates over every .tex
            texpath = os.getcwd()
            texpath += "/*.tex"
            for texname in glob.glob(texpath):
                with open(texname, 'rb') as file:
                    # Opens the template tex file
                    filedata = file.read()
                    # Replaces the keys for the values
                    for tuple in pair:
                        if tuple[0].startswith("$") and tuple[0].endswith("$"):
                            filedata =  filedata.replace(tuple[0], tuple[1])
                    # Writes the modified .tex file
                    usertex = texname[:-4] + str(user) + ".tex"
                    with open(usertex, 'w+') as file:
                        file.write(filedata)
                    # Creates a PDF from the tex file
                    call(["pdflatex", usertex])
                
