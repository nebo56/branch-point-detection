'''
Created on Nov 28, 2013

@author: Nejc Haberman


The script will read fasta file and remove random barcode and experimental barcode from fasta. Random barcode will be saved to a new fasta file
'''


import sys

def swap_barcodes(fin_fasta, fout_fasta, fout_randomBarcodes):
    finFasta = open(fin_fasta, "rt")
    foutFasta = open(fout_fasta, "w")
    foutRandomBarcode = open(fout_randomBarcodes, "w")
    line = finFasta.readline()
    while line:
        if line[0] != '>':
            randomBarcode = line[0:3] + line[7:9]
            experimentBarcode = line[3:7]
            seqRead = line[9:]
            
            if str(seqRead).__len__() > 17: #17 nt is a minimum read length
                foutFasta.write(id)
                foutRandomBarcode.write(id)
                foutFasta.write(seqRead)
                foutRandomBarcode.write(randomBarcode + '\n')
        else:   #write ID
            col = line.rstrip('\n').rsplit(' ')    #id is in the first column
            id = col[0] + '\n'    
        line = finFasta.readline()
    finFasta.close()
    foutFasta.close()
    foutRandomBarcode.close()
    
if sys.argv.__len__() == 4:
    fin_fasta = sys.argv[1]
    fout_fasta = sys.argv[2]
    fout_randomBarcodes = sys.argv[3]
    swap_barcodes(fin_fasta, fout_fasta, fout_randomBarcodes)
else:
    print "you need 2 arguments to run the script"
    quit()
