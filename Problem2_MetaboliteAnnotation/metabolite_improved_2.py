import dask
from dask import delayed, compute
from dask.distributed import Client, progress
from joblib import Parallel, delayed
import pandas as pd
import time
from tqdm import tqdm
import itertools

#input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/sample.txt"
input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/2.txt"
output = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/output2_bis.txt"

t = time.time()

def search(metabolites, adducts, signals):

    res = []
    # For each N signals
    for i, si in tqdm(enumerate(signals, start=1)):
        min_delta, tmp_j, tmp_k = None, None, None
        for j, mj in enumerate(metabolites, start=1):
            for k, ak in enumerate(adducts, start=1):
                if round(mj + ak, 6) > 0:
                    delta = round(si - mj - ak, 6)
                    if min_delta is None or abs(delta) < min_delta:
                        if si == round(mj + ak + delta, 6):
                            min_delta, tmp_j, tmp_k = abs(delta), j, k                 
        res.append([tmp_j, tmp_k])
    
    return(res)

# Total test
with open(input) as infile:

    number_of_tests = int(infile.readline().strip())

    lazy_results = []

    print("Number of tests:", number_of_tests)

    for test in range(0, number_of_tests):

        # M = n metabolite(s), K = n adduct(s), N = n signal(s)
        M, K, N = infile.readline().strip().split()

        print(f"Total computations for test {test}: {M} * {K} * {N} = {int(M) * int(K) * int(N)}")

        metabolites = [float(s) for s in infile.readline().strip().split()]
        adducts = [float(s) for s in infile.readline().strip().split()]
        signals = (float(s) for s in infile.readline().strip().split())

        #lazy_result = dask.delayed(search)(metabolites, adducts, signals)
        #lazy_results.append(lazy_result)
        results = search(metabolites, adducts, signals)
    
    #results = dask.compute(*lazy_results)
    
        df = pd.DataFrame(results)
        df.to_csv(output, header=None, index=None, sep=' ', mode = 'a')

print(time.time() - t)