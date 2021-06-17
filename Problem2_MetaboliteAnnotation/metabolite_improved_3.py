import dask
from dask import delayed, compute
from dask.distributed import Client, progress
from joblib import Parallel, delayed
import pandas as pd
import time
from tqdm import tqdm
import itertools
import numpy as np

#input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/sample.txt"
input = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/4.txt"
output = "D:/GitHub/Bioinformatics_contest_2021/Problem2_MetaboliteAnnotation/output4_bis.txt"

t = time.time()

NPROC = 8

def minimum_delta(si, metabolites, adducts):
    min_delta = tmp_j = tmp_k = None
    for j, mj in enumerate(metabolites, start=1):
        if min_delta == 0:
            break
        for k, ak in enumerate(adducts, start=1):
            if round(mj + ak, 6) > 0:
                delta = round(si - mj - ak, 6)
                if min_delta is None or abs(delta) < min_delta:
                    if si == round(mj + ak + delta, 6):
                        min_delta, tmp_j, tmp_k = abs(delta), j, k
                        if min_delta == 0:
                            break

    return(tmp_j, tmp_k)        

def parallelize_search(metabolites, adducts, signals):

    results = Parallel(n_jobs=NPROC)(delayed(minimum_delta)(si, metabolites, adducts) for si in tqdm(signals))
    return(results)

# Total test
with open(input) as infile:

    number_of_tests = int(infile.readline().strip())
    print("Number of tests:", number_of_tests)

    lazy_results = []

    for test in range(number_of_tests):

        # M = n metabolite(s), K = n adduct(s), N = n signal(s)
        M, K, N = infile.readline().strip().split()

        print(f"Total computations for test {test}: {M} * {K} * {N} = {int(M) * int(K) * int(N)}")

        metabolites = [float(s) for s in infile.readline().strip().split()]
        adducts = [float(s) for s in infile.readline().strip().split()]
        signals = (float(s) for s in infile.readline().strip().split())

        
        for signal in signals:
            # to_search = round(signal/2, 6)
            # if to_search in np.intersect1d(adducts, metabolites):
            #     print(adducts.index(to_search) + 1, metabolites.index(to_search) + 1)
            #     break
            for j, mj in enumerate(metabolites, start=1):
                   for k, ak in enumerate(adducts, start=1):
                        if round(mj + ak, 6) > 0:
                            if signal - round(mj + ak) == 0:
                                print("yes")


        #lazy_results.extend(parallelize_search(metabolites, adducts, signals))
    
        ## Using Dask on top of joblib doesn't improve the speed on my computer :( 
        ## TODO try Dask on slurm in cluster mode

        #lazy_result = dask.delayed(parallelize_search)(metabolites, adducts, signals)
        #lazy_results.append(lazy_result)

    #results = dask.compute(*lazy_results, scheduler = "threading")
    
    #print(lazy_results)
    #df = pd.DataFrame(lazy_results)
    #df.to_csv(output, header=None, index=None, sep=' ')

print(time.time() - t)