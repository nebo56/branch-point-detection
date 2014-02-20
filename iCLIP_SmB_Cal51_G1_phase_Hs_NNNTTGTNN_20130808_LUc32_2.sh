#!/bin/bash -l
#$ -l h_vmem=16G
#$ -l tmem=16G
#$ -l h_rt=32:0:0
#$ -j y
#$ -S /bin/bash

PYTHONPATH=/home/skgthab/programs/Python-2.7.5/bin
PERL5LIB=/home/skgthab/programs/ActivePerl-5.16.3.1603-x86_64-linux-glibc-2.3.5-296746/perl/bin
export PATH=$PYTHONPATH:$PATH
export PATH=$PERL5LIB:$PATH
export PATH=/home/skgthab/programs/tophat-2.0.9.Linux_x86_64:$PATH
export PATH=/home/skgthab/programs/bowtie2-2.1.0:$PATH
export PATH=/home/skgthab/programs/samtools-0.1.19:$PATH
export PATH=/home/skgthab/programs/fastx_toolkit0.0.13:$PATH
export PATH=/home/skgthab/programs/bedtools-2.17.0/bin:$PATH

data=iCLIP_SmB_Cal51_G1_phase_Hs_NNNCAATNN_20130808_LUc32_3
path=/home/skgthab/Jernej-Mapping/test/branch-point-detection-master/
introns=hg19-introns.bed

# clip the adapter and discard non-clipped sequences and discard the sequences that are shorter then 17 nt + 5 random barcode + 4 experimental barcode
fastx_clipper -Q 33 -a AGATCGGAAG -c -n -l 26 -i  ${path}${data}.fq -o  ${path}01.${data}-clipped.fq

# fastq to fasta
fastq_to_fasta -Q 33 -n -i ${path}01.${data}-clipped.fq -o ${path}02.${data}-clipped.fa
rm ${path}01.${data}-clipped.fq

# keep only reads that ends with AG
python ${path}get_branch_point_candidates.py ${path}02.${data}-clipped.fa ${path}03.${data}-filtered.fa
rm ${path}02.${data}-clipped.fa

# remove the barcode and reads that are shorter then 17 nts
python ${path}swap_barcodes.py ${path}03.${data}-filtered.fa ${path}04.${data}-noBarcodes.fa ${path}05.${data}-Barcodes.fa
rm ${path}03.${data}-filtered.fa

# map on genome
bowtie2-align -x ~/bowtie-indexes/hg19/hg19 -f ${path}04.${data}-noBarcodes.fa -S ${path}06.${data}.sam
rm ${path}04.${data}-noBarcodes.fa

# trim SAM reads which starts with A mutation on genome
python ${path}trimSAM.py ${path}06.${data}.sam ${path}06.1.${data}-trimmed.sam

# SAM to BED with collapsed read count by random barcodes
python ${path}SAMtoCollapsedSAMandBED.py ${path}06.1.${data}-trimmed.sam ${path}05.${data}-Barcodes.fa ${path}07.${data}-collapsed.sam ${path}08.${data}.bed
#python ${path}SAMtoCollapsedSAMandBED.py ${path}06.${data}.sam ${path}05.${data}-Barcodes.fa ${path}07.${data}-collapsed.sam ${path}08.${data}.bed
rm ${path}06.${data}.sam
#rm ${path}07.${data}-collapsed.sam
rm ${path}05.${data}-Barcodes.fa

# we need to split bed by strand because bedtools intersect -s is not working properly
awk '{if($6=="+") print}' ${path}${introns} > ${path}${introns}-same.bed
awk '{if($6=="-") print}' ${path}${introns} > ${path}${introns}-anti.bed
awk '{if($5=="+") print}' ${path}08.${data}.bed > ${path}09.${data}-same.bed
awk '{if($5=="-") print}' ${path}08.${data}.bed > ${path}09.${data}-anti.bed
rm ${path}08.${data}.bed

# report reads which overlaps 100% with introns (intron .bed is from UCSC bed introns only)
bedtools intersect -f 1.00 -a ${path}09.${data}-same.bed -b ${path}${introns}-same.bed | uniq > ${path}10.${data}-same-introns.bed
bedtools intersect -f 1.00 -a ${path}09.${data}-anti.bed -b ${path}${introns}-anti.bed | uniq > ${path}10.${data}-anti-introns.bed
rm ${path}09.${data}-same.bed
rm ${path}09.${data}-anti.bed
rm ${path}${introns}-same.bed
rm ${path}${introns}-anti.bed

# flank intron border on the same and anti strand
python ${path}flankBEDpositions.py ${path}${introns} ${path}${introns}-flanked-same.bed 0 -2
python ${path}flankBEDpositions.py ${path}${introns} ${path}${introns}-flanked-anti.bed 2 0

# remove all reads that are 100% in flanked introns which means they are not next to the exon position
bedtools intersect -v -f 1.00 -a ${path}10.${data}-same-introns.bed -b ${path}${introns}-flanked-same.bed | uniq > ${path}11.${data}-selected_reads-same.bed
bedtools intersect -v -f 1.00 -a ${path}10.${data}-anti-introns.bed -b ${path}${introns}-flanked-anti.bed | uniq > ${path}11.${data}-selected_reads-anti.bed
rm ${path}10.${data}-same-introns.bed
rm ${path}10.${data}-anti-introns.bed
rm ${path}${introns}-flanked-same.bed
rm ${path}${introns}-flanked-anti.bed

#merge both strands together
cat ${path}11.${data}-selected_reads-same.bed ${path}11.${data}-selected_reads-anti.bed > ${path}12.${data}-selected_reads.bed

# set end positions of the read
python ${path}set_branch_point_position.py ${path}12.${data}-selected_reads.bed ${path}${data}-branch_points.bed
rm ${path}12.${data}-selected_reads.bed

# SAM to BAM and BAI
samtools view -Sb ${path}07.${data}-collapsed.sam > ${path}07.${data}-collapsed.bam
rm ${path}07.${data}-collapsed.sam
samtools sort ${path}07.${data}-collapsed.bam ${path}07.${data}-collapsed-sorted
rm ${path}07.${data}-collapsed.bam
samtools index ${path}07.${data}-collapsed-sorted.bam ${path}07.${data}-collapsed-sorted.bam.bai



