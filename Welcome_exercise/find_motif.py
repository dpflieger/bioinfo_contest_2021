from zipfile import ZipFile
import regex as regex

file = "test-B.zip"

# with ZipFile(file) as zf:
#     with zf.open('input.txt', 'rt') as infile:
#         for line in infile.readlines():
#             print(line)


with open("input.txt") as infile, open("output.txt", "w") as outfile:

    # Total test
    n = infile.readline().strip()

    # Dict key=motif and value=sequence
    query_dict = {next(infile).strip():line.strip() for line in infile}

    for motif, sequence in query_dict.items():
        res = regex.finditer(motif, sequence, overlapped=True)
        all_starts = [str(i.start()+1) for i in res]
        print(" ".join(all_starts), file = outfile)

