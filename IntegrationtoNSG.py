import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from csv import writer
from csv import reader

df = pd.read_csv('LawDbWithSeniority1.csv', low_memory=False)
df_NSG = pd.read_csv('NormalizedEnglish.csv', low_memory=False)
INCUNCLUSIVE = 'Incunclusive'

def dict_of_names():
    names_dict = dict()
    for row_ind in df_NSG.index:
        cur_name = df_NSG['Name'][row_ind]
        cur_sector = df_NSG['Sector'][row_ind]
        if cur_name not in names_dict:
            names_dict[cur_name] = cur_sector
            continue
        elif cur_sector == INCUNCLUSIVE:
            continue
        elif names_dict[cur_name] != cur_sector:
            names_dict[cur_name] = INCUNCLUSIVE
    return names_dict


name_dict = dict_of_names()


def dict_of_genders():
    gender_dict = dict()
    for row_ind in df_NSG.index:
        cur_name = df_NSG['Name'][row_ind]
        cur_gender = df_NSG['Gender'][row_ind]
        if cur_name not in gender_dict:
            gender_dict[cur_name] = cur_gender
            continue
        elif cur_gender == INCUNCLUSIVE:
            continue
        elif gender_dict[cur_name] != cur_gender:
            gender_dict[cur_name] = INCUNCLUSIVE
    return gender_dict


gender_dict = dict_of_genders()


def get_lawyer_sector(col):
    sector_lst = []
    len(df[col])
    for i in range(len(df[col])):
        sector = "Unknown"
        if type(df[col][i]) == str:
            name = df[col][i]
            name = name.split()
            name = name[-1]
            if name in name_dict:
                sector = name_dict[name]
        sector_lst.append(sector)
    return sector_lst


def get_lawyer_gender(col):
    gender_lst = []
    len(df[col])
    for i in range(len(df[col])):
        gender = "Unknown"
        if type(df[col][i]) == str:
            name = df[col][i]
            name = name.split()
            name = name[-1]
            if name in gender_dict:
                gender = gender_dict[name]
        gender_lst.append(gender)
    return gender_lst


sector_P_lst1 = get_lawyer_sector('lawyerP1')
sector_P_lst2 = get_lawyer_sector('lawyerP2')
sector_P_lst3 = get_lawyer_sector('lawyerP3')

sector_R_lst1 = get_lawyer_sector('lawyerR1')
sector_R_lst2 = get_lawyer_sector('lawyerR2')
sector_R_lst3 = get_lawyer_sector('lawyerR3')


gender_P_lst1 = get_lawyer_gender('lawyerP1')
gender_P_lst2 = get_lawyer_gender('lawyerP2')
gender_P_lst3 = get_lawyer_gender('lawyerP3')

gender_R_lst1 = get_lawyer_gender('lawyerR1')
gender_R_lst2 = get_lawyer_gender('lawyerR2')
gender_R_lst3 = get_lawyer_gender('lawyerR3')


def add_col_to_df(lst, col):
    for row_ind in df.index:
        df.at[row_ind, col] = lst[row_ind]


add_col_to_df(sector_P_lst1, "lawyerP1Sector")
add_col_to_df(sector_P_lst2, "lawyerP2Sector")
add_col_to_df(sector_P_lst3, "lawyerP3Sector")

add_col_to_df(sector_R_lst1, "lawyerR1Sector")
add_col_to_df(sector_R_lst2, "lawyerR2Sector")
add_col_to_df(sector_R_lst3, "lawyerR3Sector")


add_col_to_df(gender_P_lst1, "lawyerP1Gender")
add_col_to_df(gender_P_lst2, "lawyerP2Gender")
add_col_to_df(gender_P_lst3, "lawyerP3Gender")

add_col_to_df(gender_R_lst1, "lawyerR1Gender")
add_col_to_df(gender_R_lst2, "lawyerR2Gender")
add_col_to_df(gender_R_lst3, "lawyerR3Gender")

df.to_csv('layers_sector_gender.csv', encoding="utf-8-sig", index=False)