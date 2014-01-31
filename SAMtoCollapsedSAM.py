'''
Created on 31 Jan 2014

@author: Nejc Haberman
'''        

# tested for bowtie 2!
# input: 
#    fin_sam    - path to .SAM file
#    fin_random_barcode    - path to random barcode file
#    fout_sam   - path for output collapsed .SAM file

# sam_file_to_bed method:
# 
# The method read .SAM file and write collapsed .SAM file where ignores "4" strand and duplicate barcodes. 
#

import sys

#method will remove duplicated reads from SAM file
def sam_file_to_bed (fin_sam, fin_random_barcode, fout_sam):
    random_barcodes = load_random_barcodes(fin_random_barcode)
    fin = open(fin_sam, "rt")
    fout = open(fout_sam, "w")
    sam = fin.readline()
    reads = {}
    while sam[0] == '@':    #header of .SAM
        sam = fin.readline()
        fout.write(sam)
    while sam:
        tokens = sam.rstrip('\n').rstrip('\r').split('\t')
        read_id = tokens[0]
        strand = tokens[1]
        chr = tokens[2]
        position = int(tokens[3])
        
        if strand == "0" or strand == "16": #0 for same strand and 16 for anti strand
            barcode = random_barcodes.get(str(read_id))
            duplicate = False   #we check if the same barcode already exist
            positions = reads.get(chr)
            if positions != None:
                strands = positions.get(position)
                if strands != None:
                    barcodes = strands.get(strand)
                    if barcodes != None:
                        if barcodes.get(barcode) != None:
                            duplicate = True
            if duplicate == False:  #we write only uniq barcodes
                fout.write(sam)
                reads.setdefault(chr, {}).setdefault(position, {}).setdefault(strand,{}).setdefault(barcode,True)
        sam = fin.readline()
        
    fin.close()
    fout.close()


# method will load rabdom barcodes to a dictionary indexed by IDs
def load_random_barcodes(fin_name):
    fin = open(fin_name, "rt")
    rb = fin.readline()
    rand_barcodes = {}
    while rb:
        id = rb.rstrip('\n').rstrip('\r')
        id = id[1:]
        rb = fin.readline()
        if rb:
            barcode = rb.rstrip('\n').rstrip('\r')
            rand_barcodes.setdefault(id,barcode)
    fin.close()
    return rand_barcodes
    
    
# main
 
if sys.argv.__len__() == 4:
    fin_sam = sys.argv[1]
    random_barcodes = sys.argv[2]
    fout_sam = sys.argv[3]
    sam_file_to_bed(fin_sam, random_barcodes, fout_sam)
else:
    print "you need 3 arguments to run the script"
    quit()
 
 
#PATH = "/media/skgthab/storage/UCL/2013.12.10-Branch_point-Jernej/working/iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-working/"
#sam_file_to_bed(PATH + "06.1.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-trimmed.sam",  PATH + "05.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-Barcodes.fa", PATH + "test/07.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-collapsed-TEST-trimmed.sam", PATH + "test/20130808_LUc31_1_hg19_ensembl59_S_notmapped-collapsed-TEST-trimmed.bed")



