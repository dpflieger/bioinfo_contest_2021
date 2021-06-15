import time

#input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/sample.txt"
input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/2.txt"
output = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/output2_bis.txt"

t = time.time()

with open(input) as infile, open(output, "w") as outfile:

    # Total test
    number_of_tests = int(infile.readline().strip())

    for test in range(0, number_of_tests):

        # M = n metabolite(s), K = n adduct(s), N = n signal(s)
        M, K, N = infile.readline().strip().split()

        metabolites = [float(s) for s in infile.readline().strip().split()]
        adducts = [float(s) for s in infile.readline().strip().split()]
        signals = [float(s) for s in infile.readline().strip().split()]

        # For each N signals
        for si in signals:
            min_delta, tmp_j, tmp_k = None, None, None
            # The pairs of metabolite mj and adduct ak 
            for j, mj in enumerate(metabolites, start=1):
                for k, ak in enumerate(adducts, start=1):
                    if round(mj + ak, 6) > 0:
                        delta = round(si - mj - ak, 6)
                        if min_delta is None or abs(delta) < min_delta:
                            if si == round(mj + ak + delta, 6):
                                # Get smallest absolute delta
                                min_delta, tmp_j, tmp_k = abs(delta), j, k
                               
            print(tmp_j, tmp_k, file = outfile)

print(time.time() - t)