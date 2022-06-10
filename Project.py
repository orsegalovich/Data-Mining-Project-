import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns


df = pd.read_csv('LawDbWithSeniority1.csv', low_memory=False)
df['avg_seniority'] = pd.to_numeric(df['avg_seniority'],errors='coerce')


def get_seniority_affect_of_overruling():
    count_overruled = 0
    sum_avg_seniority_overruled = 0
    temp_case = 1000002
    for i in range(len(df['ISCD_ID'])):
        if df['legalProcedure'][i] != "High Court of Justice" and df['outcomecourt'][i] == "Accepted":
            case = df['ISCD_ID'][i]
            case = int(case)
            if case != temp_case:
                temp_case = case
                count_overruled += 1
                sum_avg_seniority_overruled += float(df["avg_seniority"][i])
    return sum_avg_seniority_overruled/count_overruled


print("Average seniority of judges in appeal cases overruled: " , get_seniority_affect_of_overruling())
print("Average seniority of judges in all cases: " , df["avg_seniority"].mean())
print("Average seniority of judges in Appeal cases: " , df.where(df['legalProcedure'] != "High Court of Justice")["avg_seniority"].mean())






