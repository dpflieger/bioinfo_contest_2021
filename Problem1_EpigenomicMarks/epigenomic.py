#infile = "D:/GitHub/Bioinformatics_contest_2021/Problem1_EpigenomicMarks/tests/sample.txt"

input = "D:/GitHub/Bioinformatics_contest_2021/Problem1_EpigenomicMarks/tests/2.txt"
output = "D:/GitHub/Bioinformatics_contest_2021/Problem1_EpigenomicMarks/tests/output2.txt"

with open(input) as infile, open(output, "w") as outfile:

    # Number of tests
    number_of_tests = int(infile.readline().strip())

    for test in range(0, number_of_tests):
        
        # n = number of sequences and t = their length
        n, l = next(infile).strip().split()
        matrix = []
        for sequence in range(0, int(n)): 
            matrix.append(next(infile).strip())

        motifs = []
        result = []

        for i in range(0, int(l)):
            motif = "".join([sequence[i] for sequence in matrix])
            if motif in motifs:
                result.append(str(motifs.index(motif) + 1))
            else:
                motifs.append(motif)
                result.append(str(motifs.index(motif) + 1))

        print(len(motifs), file = outfile)
        print(" ".join(result), file = outfile)

