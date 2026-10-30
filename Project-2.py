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
#sorts codons alphabetically and returns the dictionary.
with open("NC_000913_full_sequence.txt") as f:
#opens the DNA sequence file (complete genome of E coli) and reads its contents.
    dna = f.read().strip()
#reads the sequence and removes surrounding whitespace.
codon_counts = codon_frequencies(dna)
#calculates the frequency of each codon.


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
    "E": ["GAA", "GAG"],
    "C":      ["TGT", "TGC"],
    "W":    ["TGG"],
    "R":      ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "G":       ["GGT", "GGC", "GGA", "GGG"],
    "STOP":          ["TAA", "TAG", "TGA"],
}
#stores each amino acid and its possible DNA codons.

#codon_counts is the dictionary returned by codon_frequencies(dna)
most_frequent_codon = {}
#stores the most frequent codon for each amino acid.

for amino_acid in amino_acid_codons:
#goes through each amino acid in the dictionary
    best_codon = ""
    #start with an empty string to store the most frequent codon
    best_count = 0
    #start the highest codon count at 0

    for codon in amino_acid_codons[amino_acid]:
    #goes through each codon that codes for this amino acid
        count = codon_counts.get(codon, 0)
        #get the number of times this codon appears, if codon not in dictionary, use 0
        if count > best_count:
        #check if this codon appears more often than the current best
            best_codon = codon
            #if it does, save this codon as the most frequent one
            best_count = count
            #update the highest count to this codon's count

    most_frequent_codon[amino_acid] = best_codon
    #store the most frequent codon for this amino acid in the most_frequent_codon dictionary
    print(amino_acid, best_codon, best_count)
    #print the amino acid, its most frequent codon, and how many times that codon appears

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
#store the insulin protein sequence as a string

#remove line breaks and spaces, then convert to uppercase
protein = protein.replace("\n", "").replace(" ", "").upper()

dna = ""
#create an empty string to store the DNA sequence
for amino_acid in protein:
    dna += most_frequent_codon[amino_acid]
#convert each amino acid into its most frequent DNA codon

dna += most_frequent_codon["STOP"]
#add a stop codon to signal the end of protein translation

print(dna)
#print the completed DNA sequence
print(len(protein), "amino acids ->", len(dna), "bases")
#display the number of amino acids and DNA bases
