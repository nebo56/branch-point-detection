#!/bin/bash
#script will count transition ratio on first nucleotide of the read from SAM file

total=$(cat $1 | grep -v @ | wc -l)

#same strand
sameA=$(cat $1 | awk '{if($2=="0") print $18}' | grep 0A | wc -l)
sameC=$(cat $1 | awk '{if($2=="0") print $18}' | grep 0C | wc -l)
sameT=$(cat $1 | awk '{if($2=="0") print $18}' | grep 0T | wc -l)
sameG=$(cat $1 | awk '{if($2=="0") print $18}' | grep 0G | wc -l)

#anti strand
antiA=$(cat $1 | awk '{if($2=="16") print $18}' | grep 0T | wc -l)
antiC=$(cat $1 | awk '{if($2=="16") print $18}' | grep 0G | wc -l)
antiT=$(cat $1 | awk '{if($2=="16") print $18}' | grep 0A | wc -l)
antiG=$(cat $1 | awk '{if($2=="16") print $18}' | grep 0C | wc -l)

#ratio
#let "A=((sameA+antiA)/total)*100"
#let "C=((sameC+antiC)/total)*100"
#let "T=((sameT+antiT)/total)*100"
#let "G=((sameG+antiG)/total)*100"

echo A $((($sameA+$antiA)))
echo C $((($sameC+$antiC)))
echo T $((($sameT+$antiT)))
echo G $((($sameG+$antiG)))

#print out
echo "$A"
echo "$C"
echo "$T"
echo "$G"

