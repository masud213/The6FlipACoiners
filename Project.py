# The6FlipACoiners muaad is smth

codon= ['AGC','TTT','TCA','TTC','TGA','CTG','CAA','CGG','GCA','ATA','TGT','CTC','TGA','AGC']
#creates list of codons
codon.count('AGC')
#count the number of times AGC codon appears in the list
def codon_frequencies(sequence): 
#defines function, sequence is the DNA sequence passed into function
    codonDict = {} 
#creates an empty dictionary to store each codon and its count
    for startIndex in range(0, len(sequence) - 2, 3): 
#range: starts at index 0 and increases by 3 each time
#len(sequence): gives length of gene sequence
#startIndex: represents the start of each codon: 0, 3, 6, 9, etc.
#the loop will run until end of sequence reached
        codon = sequence[startIndex:startIndex + 3]
#This takes three consecutive DNA bases and joins them together to form a codon
        codonDict[codon] = codonDict.get(codon, 0) + 1
#Counts each codon occurrence in the dictionary.

    return dict(sorted(codonDict.items()))

with open("NC_000913_full_sequence.txt") as f:
    dna = f.read().strip()

codon_counts = codon_frequencies(dna)

print(codon_counts)

amino_acid_codons = {
    "Phenylalanine": ["TTT", "TTC"],
    "Leucine":       ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "Isoleucine":    ["ATT", "ATC", "ATA"],
    "Methionine":    ["ATG"],
    "Valine":        ["GTT", "GTC", "GTA", "GTG"],
    "Serine":        ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "Proline":       ["CCT", "CCC", "CCA", "CCG"],
    "Threonine":     ["ACT", "ACC", "ACA", "ACG"],
    "Alanine":       ["GCT", "GCC", "GCA", "GCG"],
    "Tyrosine":      ["TAT", "TAC"],
    "Histidine":     ["CAT", "CAC"],
    "Glutamine":     ["CAA", "CAG"],
    "Asparagine":    ["AAT", "AAC"],
    "Lysine":        ["AAA", "AAG"],
    "Aspartic acid": ["GAT", "GAC"],
    "Glutamic acid": ["GAA", "GAG"],
    "Cysteine":      ["TGT", "TGC"],
    "Tryptophan":    ["TGG"],
    "Arginine":      ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "Glycine":       ["GGT", "GGC", "GGA", "GGG"],
    "STOP":          ["TAA", "TAG", "TGA"],
}

# codon_counts is the dictionary returned by codon_frequencies(dna)
most_frequent_codon = {}

for amino_acid, codons in amino_acid_codons.items():
    best_codon = max(codons, key=lambda c: codon_counts.get(c, 0))
    most_frequent_codon[amino_acid] = (best_codon, codon_counts.get(best_codon, 0))

for amino_acid, (codon, count) in most_frequent_codon.items():
    print(amino_acid, codon, count)
