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



amino_acid_codons = {
    "F": ["TTT", "TTC"],
    "L":       ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "I":    ["ATT", "ATC", "ATA"],
    "M":    ["ATG"],
    "V":        ["GTT", "GTC", "GTA", "GTG"],
    "S":        ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "P":       ["CCT", "CCC", "CCA", "CCG"],
    "T":     ["ACT", "ACC", "ACA", "ACG"],
    "A":       ["GCT", "GCC", "GCA", "GCG"],
    "Y":      ["TAT", "TAC"],
    "H":     ["CAT", "CAC"],
    "Q":     ["CAA", "CAG"],
    "N":    ["AAT", "AAC"],
    "K":        ["AAA", "AAG"],
    "D": ["GAT", "GAC"],
    "E`": ["GAA", "GAG"],
    "C":      ["TGT", "TGC"],
    "W":    ["TGG"],
    "R":      ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "G":       ["GGT", "GGC", "GGA", "GGG"],
    "STOP":          ["TAA", "TAG", "TGA"],
}

most_frequent_codon = {}

for amino_acid in amino_acid_codons:
    best_codon = ""
    best_count = 0

    for codon in amino_acid_codons[amino_acid]:
        count = codon_counts.get(codon, 0)
        if count > best_count:
            best_codon = codon
            best_count = count

    most_frequent_codon[amino_acid] = best_codon
    print(amino_acid, best_codon, best_count)

# Most frequent codon for each amino acid (from the CDS-based counts)
most_frequent_codon = {
    "F": "TTT", "L": "CTG", "I": "ATT", "M": "ATG", "V": "GTG",
    "S": "AGC", "P": "CCG", "T": "ACC", "A": "GCG", "Y": "TAT",
    "H": "CAT", "Q": "CAG", "N": "AAC", "K": "AAA", "D": "GAT",
    "E": "GAA", "C": "TGC", "W": "TGG", "R": "CGC", "G": "GGC",
    "STOP": "TAA",
}

protein = """MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAED
LQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"""

# Remove the line break and any spaces
protein = protein.replace("\n", "").replace(" ", "").upper()

dna = ""
for amino_acid in protein:
    dna += most_frequent_codon[amino_acid]

# Add a stop codon at the end
dna += most_frequent_codon["STOP"]

print(dna)
print(len(protein), "amino acids ->", len(dna), "bases")