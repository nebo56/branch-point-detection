'''
Created on Jan 8, 2014

@author: Nejc Haberman

The script will filter out only fasta sequences that ends with AG
'''


import sys

def filter_branch_point_seq (fin_fasta, fout_fasta):
    finFasta = open(fin_fasta, "rt")
    foutFasta = open(fout_fasta, "w")
    line = finFasta.readline()
    while line:
        if line[0] != '>':
            line = line.rstrip('\n')
            if str(line[-2:]).upper() == "AG":
                foutFasta.write(id)
                foutFasta.write(line + '\n')
        else:
            id = line
        line = finFasta.readline()
    finFasta.close()
    foutFasta.close()
    
if sys.argv.__len__() == 3:
    fin_fasta = sys.argv[1]
    fout_fasta = sys.argv[2]
    filter_branch_point_seq (fin_fasta, fout_fasta)
else:
    print "you need 2 arguments to run the script"
    quit()
