import os
import pickle

def string_to_rvalue(s: str) -> float:
    s = s.strip()
    if 'k' in s:
        return float(s.replace('k', '')) * 1_000
    elif 'M' in s:
        return float(s.replace('M', '')) * 1_000_000
    else:
        return float(s)
    
print("Current working directory:", os.getcwd())
with open("resistor-values.txt", "r") as file:
    r_values = file.readlines()
r_values_float = [string_to_rvalue(line) for line in r_values if line.strip()]

r_values_float.sort()
print(r_values_float)
pickle.dump(r_values_float, open("r_values.pkl", "wb"))