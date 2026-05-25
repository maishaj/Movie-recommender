import pickle
import bz2

print("Reading raw similarity.pkl...")
with open("similarity.pkl", "rb") as f:
    matrix = pickle.load(f)

print("Compressing into similarity.pbz2...")
with bz2.BZ2File("similarity.pbz2", "w") as f:
    pickle.dump(matrix, f)

print("Successfully created similarity.pbz2!")