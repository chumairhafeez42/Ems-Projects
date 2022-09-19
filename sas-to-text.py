# import pandas as pd
# sas_file = "/home/amir/Downloads/spm_2019_pu.dta"
# filename = sas_file.split("/")[-1].split(".")[0]
# writePath = f"/home/amir/Downloads/Datasets/{filename}.txt"
# # print(writePath)
# df = pd.read_sas(sas_file)
# # print(df.head())
#
# dfAsString = df.to_csv(writePath, header=True, index=False, sep='\t', mode='w+')



#CSV to TXT
# import pandas as pd
# df = pd.read_csv('/home/amir/Desktop/All Pdfs/06-06-22/EuroSat Dataset/EuroSAT/validation.csv', encoding='utf-8')
# # df = df[df["Reputation_Score"] > 30]
# df.to_csv("/home/amir/Desktop/All Pdfs/06-06-22/EuroSat Dataset/EuroSAT/validation.txt", header=False, index=False, encoding='utf-8')
import os
parent_path = '/home/umair/Downloads/Kaglle/archive (1)'
filenames = next(
            os.walk(parent_path), (None, None, [])
        )[2]
print(len(filenames))
for file in filenames:
    if ".csv" not in file:
        continue
    CHUNK_SZ = 1024 * 1024

    FS = "'~'"
    RS = '#@#@#'

    # With chars repeated in the separators, check most specific (least ambiguous)
    # to least specific (most ambiguous) to definitively catch a partial with the
    # fewest number of checks
    PARTIAL_RSES = ['#@#@', '#@#', '#@', '#']
    PARTIAL_FSES = ["'~", "'"]
    ALL_PARTIALS =  PARTIAL_FSES + PARTIAL_RSES

    f_out = open(f'{parent_path}/{file.replace(".csv",".txt")}', 'w')
    # f_out.write('a,b,c,d\n')

    f_in = open(f'{parent_path}/{file}')
    line = ''
    while True:
        # Read chunks till no more, then break out
        chunk = f_in.read(CHUNK_SZ)
        if not chunk:
            break

        # Any previous partial separator, plus new chunk
        line += chunk

        # Check end-of-line for a partial FS or RS; only when separators are more than one char
        final_partial = ''

        if line.endswith(FS) or line.endswith(RS):
            pass  # Write-out will replace complete FS or RS
        else:
            for partial in ALL_PARTIALS:
                if line.endswith(partial):
                    final_partial = partial
                    line = line[:-len(partial)]
                    break

        # Process/write chunk
        f_out.write(line
                    .replace(FS, ',')
                    .replace(RS, '\n'))

        # Add partial back, to be completed next chunk
        line = final_partial

    os.remove(f'{parent_path}/{file}')
    # Clean up
    f_in.close()
    f_out.close()

# Convert Images
# import os
# parent_path = '/home/amir/Desktop/Requests-Images/share/images'
# filenames = next(os.walk(parent_path), (None, None, []))[2]
# for file in filenames:
#     os.rename(os.path.join(parent_path, file), os.path.join(parent_path, file.split(".")[0]+".TIFF"))

# #Convert Images of All Subfolders
# import os

# traverse root directory, and list directories as dirs and files as files
# parent_path = "/home/amir/Desktop/Requests-Images/share/skin cancer"
# for root, dirs, files in os.walk(parent_path):
#     path = root.split(os.sep)
#     full_path = "/".join(path)
#     # print("/".join(path)
#     # print((len(path) - 1) * '---', os.path.basename(root))
#     for file in files:
#         os.rename(os.path.join(full_path, file), os.path.join(full_path, file.split(".")[0] + ".TIFF"))
#         # print(len(path) * 'File---', (file))

#Convert TIFF to jpeg
# import os
# import pandas as pd
# parent_path = "/home/amir/Desktop/finde-data-images/images"
# for root, dirs, files in os.walk(parent_path):
#     path = root.split(os.sep)
#     full_path = "/".join(path)
#     # print("/".join(path)
#     # print((len(path) - 1) * '---', os.path.basename(root))
#     for file in files:
#         try:
#             # df = pd.read_csv(os.path.join(full_path, file), encoding='utf-8')
#             # df = df[df["Reputation_Score"] > 30]
#             # df.to_csv(os.path.join(full_path, file.split(".")[0] + ".txt"), header=False, index=False, encoding='utf-8')
#             os.rename(os.path.join(full_path, file), os.path.join(full_path, file.rsplit('.', 1)[0] + ".TIFF"))
#             os.remove(os.path.join(full_path, file))
#             # print(len(path) * 'File---', (file))
#         except:
#             continue
