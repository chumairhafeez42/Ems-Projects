import pandas as pd
sas_file = "/home/amir/Downloads/spm_pu_2019.sas7bdat"
filename = sas_file.split("/")[-1].split(".")[0]
writePath = f"/home/amir/Downloads/Datasets/{filename}.txt"
df = pd.read_sas(sas_file)
print(df.head())

with open(writePath, 'a') as f:
    dfAsString = df.to_string(header=True, index=False)
    f.write(dfAsString)