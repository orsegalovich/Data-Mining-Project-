import pandas as pd
from datetime import datetime


date_format = "%m/%d/%Y"
df = pd.read_csv('LawDbWithSeniorityAndVerdictCount.csv', low_memory=False)



case_id_list = df['ISCD_ID'].to_list()
case_start_date_list = df['dateOpen'].to_list()
case_end_date_list = df['dateFinalDecision'].to_list()


case_id_to_duration_dict = dict()
for i,url in enumerate(case_id_list):
    # if i <= 3000:
    #     continue
    if i%1000==0:
        df.to_csv('LawDbWithSeniorityAndVerdictCountAndDuration.csv', encoding="utf-8-sig", index=False)
        df = pd.read_csv('LawDbWithSeniorityAndVerdictCountAndDuration.csv', low_memory=False)

    if case_id_list[i] in case_id_to_duration_dict:
        df.loc[i, 'case_duration'] = case_id_to_duration_dict[case_id_list[i]]
        continue


    start_date = datetime.strptime(case_start_date_list[i], date_format)
    end_date = datetime.strptime(case_end_date_list[i], date_format)
    duration = end_date-start_date

    df.loc[i , 'case_duration'] = duration.days
    case_id_to_duration_dict[case_id_list[i]] = duration.days
    print(i)



df.to_csv('LawDbWithSeniorityAndVerdictCount.csv', encoding="utf-8-sig", index=False)
