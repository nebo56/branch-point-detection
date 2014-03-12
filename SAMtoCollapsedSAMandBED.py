'''
Created on 23 Aug 2012

@author: Nejc Haberman
'''        

# tested for bowtie 2!
# input: 
#    fin_sam    - path to .SAM file
#    fin_random_barcode    - path to random barcode file
#    fout_sam   - path for output collapsed .SAM file
#    fout_bed   - path for output collapsed .BED file

# sam_file_to_bed method:
# 
# The method read .SAM file and write collapsed .SAM file where ignores "4" strand and duplicate barcodes. Collapsed data is also written to .BED file
#

import sys

def sam_file_to_bed (fin_sam, fin_random_barcode, fout_sam, fout_bed):
    random_barcodes = load_random_barcodes(fin_random_barcode)
    fin = open(fin_sam, "rt")
    fout = open(fout_sam, "w")
    sam = fin.readline()
    reads = {}
    while sam[0] == '@':    #header of .SAM
        fout.write(sam)
        sam = fin.readline()
    while sam:
        tokens = sam.rstrip('\n').rstrip('\r').split('\t')
        read_id = tokens[0]
        flag = tokens[1]
        chr = tokens[2]
        position = int(tokens[3])
        read_length = tokens[5]
        seq = tokens[9]
        strand = ""
        if flag != "4": #we ignore 4
            len = seq.__len__() #in case if insertions or junctions this won't work
            if read_length.find('I') > 0:   #then it was insertion involved and we need to add that to our length
                I_position = read_length.find('I')
                I = int(read_length[I_position - 1])  #number of insertions
                len += I    #we add number of insertions to seq length
            if flag == "0":
                strand = "+"
                start = position
                end = position + len
                read_position = (start, end)
            if flag == "16":
                strand = "-"
                #len = int(read_length.strip('M'))
                end = position
                start = position + len - 1
                read_position = (end, start)
            barcode = random_barcodes.get(str(read_id))

            duplicate = False   #we check if the same barcode already exist
            positions = reads.get(chr)
            if positions != None:
                strands = positions.get(read_position)
                if strands != None:
                    barcodes = strands.get(strand)
                    if barcodes != None:
                        if barcodes.get(barcode) != None:
                            duplicate = True
            if duplicate == False:  #we write only uniq barcodes
                fout.write(sam)
                reads.setdefault(chr, {}).setdefault(read_position, {}).setdefault(strand,{}).setdefault(barcode,True)
                    
        sam = fin.readline()
    fin.close()
    fout.close()
    
    # .BED file
    fout = open(fout_bed, "w")
    header = [
        "track type=bedGraph name=" + '"' + fin_sam + '"',
        "description=" + '"' + fin_sam + '"',
        "db=hg19 regions="+'"'+'"',
        "mapped_tos=" + '"' + "hg19" + '"',
        "altColor="+'"'+"200,120,59"+'"',
        "color="+'"'+"120,101,172"+'"',
        "exp_ids="+'"'+'"',
        "maxHeightPixels="+'"'+"100:50:0"+'"',
        "visibility=" + '"' + "full" + '"',
        "priority=" + '"' + "20" +'"',
        "grouping_operation=" + '"' + "sum" + '"',
        "mapped_to=" + '"' + "hg19" + '"',
        "detailed_description=" + '"'+'"',
        "group=" + '"' + '"',
        "annot_vers=" + '"' + "" + '"' 
    ]
    fout.write("%s\n" % " ".join(header))
    for chr, chr_reads in reads.items():
        for read_position, pos_reads in chr_reads.items():
            for strand, strand_reads in pos_reads.items():
                start, end = read_position
                if (strand == '+') and (strand_reads.__len__() > 0):
                    fout.write(chr + '\t' + str(start) + '\t' + str(end-1) + '\t' + str(strand_reads.__len__()) + '\t' + "" + '\t' + '+' + '\n')
                if (strand == '-') and (strand_reads.__len__() > 0):
                    fout.write(chr + '\t' + str(start) + '\t' + str(end) + '\t' + str(strand_reads.__len__()) + '\t' + "" + '\t' + '-' + '\n')
    fout.close()
                    


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
    
if sys.argv.__len__() == 5:
    fin_sam = sys.argv[1]
    random_barcodes = sys.argv[2]
    fout_sam = sys.argv[3]
    fout_bed = sys.argv[4]
    sam_file_to_bed(fin_sam, random_barcodes, fout_sam, fout_bed)
else:
    print "you need 4 arguments to run the script"
    quit()
 
#PATH = "/media/skgthab/storage/UCL/2013.12.10-Branch_point-Jernej/working/iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-working/"
#sam_file_to_bed(PATH + "06.1.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-trimmed.sam",  PATH + "05.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-Barcodes.fa", PATH + "test/07.iCLIP_SmB_Cal51_G1_phase_Hs_NNNTTGTNN_20130808_LUc32_2-collapsed-TEST-trimmed.sam", PATH + "test/20130808_LUc31_1_hg19_ensembl59_S_notmapped-collapsed-TEST-trimmed.bed")



