# The6FlipACoiners muaad is smth

codon= ['AGC','TTT','TCA','TTC','TGA','CTG','CAA','CGG','GCA','ATA','TGT','CTC','TGA','AGC']
codon.count('AGC')

def codon_frequencies(sequence):
    codonDict = {}
    for startIndex in range(0, len(sequence) - 2, 3):
        codon = sequence[startIndex:startIndex + 3]
        codonDict[codon] = codonDict.get(codon, 0) + 1

    return dict(sorted(codonDict.items()))

with open("NC_000913_full_sequence.txt") as f:
    dna = f.read().strip()

codon_counts = codon_frequencies(dna)

print(codon_counts)
