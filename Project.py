import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv('LawDbWithSeniority1.csv', low_memory=False)
df['avg_seniority'] = pd.to_numeric(df['avg_seniority'],errors='coerce')


def get_seniority_affect_of_overruling():
    count_overruled = 0
    sum_avg_seniority_overruled = 0
    temp_case = "1000002.01"
    for i in range(len(df['ISCD_ID'])):
        if df['legalProcedure'][i] != "High Court of Justice" and df['outcomecourt'][i] == "Accepted":
            if float(df['ISCD_ID'][i]) - float(temp_case) > 0.1:
                temp_case = df['ISCD_ID'][i]
                count_overruled += 1
                sum_avg_seniority_overruled += df["avg_seniority"][i]
    return [sum_avg_seniority_overruled/count_overruled]



print(get_seniority_affect_of_overruling())

# df_grouped = df.groupby(["ISCD_ID"])["avg_seniority"]
#
# print(df_grouped.head(10))
# print(type(df_grouped))

