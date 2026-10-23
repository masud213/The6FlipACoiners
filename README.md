# The6FlipACoiners muaad is smth

codon= ['AGC','TTT','TCA','TTC','TGA','CTG','CAA','CGG','GCA','ATA','TGT','CTC','TGA','AGC']
codon.count('AGC')

def codon_frequencies(sequence):
    codonDict = {}
    for startIndex in range(0, len(geneSeq), 3):
        codon = sequence[startIndex] + sequence[startIndex+1] + sequence[startIndex+2]
        if codon not in codonDict:
            codonDict[codon] = 1
        else:
            codonDict[codon] = codonDict[codon] + 1
    sortedCodonDict = dict(sorted(codonDict.items()))
    for k,v in sortedCodonDict.items():
        print(k,v)

print_codon_frequencies(geneSeq)
