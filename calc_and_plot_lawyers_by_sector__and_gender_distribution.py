import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pylab as pylab
import seaborn as sns
import numpy as np
import math

LAWYERS_INDEX_LIST = ["P1","P2","P3","R1", "R2","R3"]
SECTOR = "Sector"
GENDER = "Gender"
UNKNOWN = "Unknown"

LAWYER = "lawyer"
INCONCLUSIVE_G = "Inconclusive gender"
INCONCLUSIVE_S = "Inconclusive sector"

df = pd.read_csv('cases_with_sector.csv', low_memory=False)

genders_and_sectors_counter ={"Unknown": 0, "Male": 0, "Jew": 0, "Arab": 0, INCONCLUSIVE_G: 0, INCONCLUSIVE_S: 0, "Female": 0}
subgroups_dict_counter ={"Arab&Female": 0, "Arab&Male": 0, "Jew&Female": 0, "Jew&Male": 0}\

def calculate_appearances_of_sectors_and_genders():
    #Iterate on every case
    for row_ind in df.index:
        # Create dict to avoid counting same lawyer twice in the same case
        current_row_dict = dict()
        for lawyer_ind in LAWYERS_INDEX_LIST:
            column_name = LAWYER + lawyer_ind
            lawyer_name = df[column_name][row_ind]
            # validate lawyer_name exists (and is not NAN)
            # print(lawyer_name)
            if not lawyer_name or lawyer_name != lawyer_name:
                # print(1)
                continue
            # validate no lawyer is counted twice in the same case
            if lawyer_name in current_row_dict.keys():
                # print(2)
                continue
            current_row_dict[lawyer_name] = True
            # Get lawyer sector and gender
            lawyer_sector_lst = df[column_name+SECTOR]
            lawyer_gender_lst = df[column_name+GENDER]
            lawyer_sector = lawyer_sector_lst[row_ind]
            lawyer_gender = lawyer_gender_lst[row_ind]
            # print(lawyer_gender ,lawyer_name)
            # Count sector and gender
            if lawyer_sector == "Unregistered" or lawyer_gender == "Unregistered":
                continue
            if lawyer_sector == UNKNOWN or lawyer_gender == UNKNOWN:
                genders_and_sectors_counter[UNKNOWN] +=1
                continue
            genders_and_sectors_counter[lawyer_sector] += 1
            genders_and_sectors_counter[lawyer_gender] += 1
            if lawyer_sector != UNKNOWN and lawyer_sector != INCONCLUSIVE_S\
                and lawyer_gender != UNKNOWN and lawyer_gender != INCONCLUSIVE_G:
                subgroups_dict_counter[f"{lawyer_sector}&{lawyer_gender}"] +=1

def plot_data_function(title, yaxis_title, file_name, label_size):

    pylab.rcParams.update({'xtick.labelsize': label_size})
    df_values = pd.DataFrame.from_dict(genders_and_sectors_counter, orient='index')
    sorted_appearances = df_values.sort_values(by=0)
    sorted_appearances.plot(kind="bar")
    # plt.set(title="Genders and Sectors Distribution", xlabel="categories", ylabel="amount of cases")
    plt.xticks(rotation=45, ha='right')
    plt.title(title, fontsize=16)
    # plt.xlabel("categories", fontsize=10)
    plt.ylabel(yaxis_title, fontsize=10)
    plt.savefig(f"./sectors_visualization/{file_name}")
    plt.clf()


# Update dictionaries to amount of groups appearing in each case
calculate_appearances_of_sectors_and_genders()

# Plot genders and sectors distribution
plot_data_function("Genders and Sectors Distribution", "amount of cases", 'genders_and_sectors_distribution.png', '4')

# Plot subgroups distribution
plot_data_function("Subgroups of Genders and Sectors", "amount of cases", 'subgroups_of_genders_and_sectors_distribution.png', '5')

