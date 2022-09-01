import pandas as pd

df = pd.read_csv('..\iscd_cases_2018-12-05.csv', low_memory=False, na_filter=False)


def get_judges_lst():
    judges_list = df['justice1'].to_list()
    judges_dict = dict()
    for judge in judges_list:
        if judge not in judges_dict:
            judges_dict[judge] = None

    judges_list = [key for key in judges_dict.keys()]
    return judges_list

def get_judges_pairs():
    judges_list = get_judges_lst()
    pair_of_judges_lst = []

    for ind, judge in enumerate(judges_list):
        for j in range(ind+1,len(judges_list)):
            pair = set()
            pair.add(judge)
            pair.add(judges_list[j])
            pair_of_judges_lst.append(pair)

    # print(len(pair_of_judges_lst))
    # print(pair_of_judges_lst)
    return pair_of_judges_lst

judges_by_cases = df[['justice1','justice2','justice3','justice4','justice5','justice6','justice7','justice8','justice9']]



pair_of_judges_lst = get_judges_pairs()





data = {'judge_a': [list(pair_of_judges_lst[i])[0] for i in range(len(pair_of_judges_lst))], 'judge_b': [list(pair_of_judges_lst[i])[1] for i in range(len(pair_of_judges_lst))],\
        'appearances': [0 for i in range(len(pair_of_judges_lst))], 'caseid': [0 for i in range(len(pair_of_judges_lst))]}




judges_pair_df = pd.DataFrame(data)
print(judges_pair_df)

NINE = 9
for row_ind in range(len(df.index)):
    print(row_ind)
    for j1_ind in range(NINE):
        judge1 = judges_by_cases.iloc[row_ind, j1_ind]
        if not judge1:
            continue
        for j2_ind in range(j1_ind+1, NINE):
            judge2 = judges_by_cases.iloc[row_ind, j2_ind]
            if not judge2:
                continue

            if ((judges_pair_df['judge_a'] == judge1) & (judges_pair_df['judge_b'] == judge2)).any():
                judges_pair_df.loc[(judges_pair_df['judge_a'] == judge1) & (judges_pair_df['judge_b'] == judge2), 'appearances']+=1
                # judges_pair_df.loc[(judges_pair_df['judge_a'] == judge1) & (judges_pair_df['judge_b'] == judge2), 'caseid'] = df.loc[row_ind, 'caseId']

            elif ((judges_pair_df['judge_a'] == judge2) & (judges_pair_df['judge_b'] == judge1)).any():
                judges_pair_df.loc[(judges_pair_df['judge_a'] == judge2) & (judges_pair_df['judge_b'] == judge1), 'appearances']+=1
                # judges_pair_df.loc[(judges_pair_df['judge_a'] == judge1) & (judges_pair_df['judge_b'] == judge2), 'caseid'] = df.loc[row_ind, 'caseId']
                # print(df2.loc[df['judge_a']==judge2 & df2['judge_b']==judge1])


j = judges_pair_df.sort_values(by=['appearances'], ascending=False)
j.to_csv('..\PairOfJudgesAndMutualCaseCount.csv', encoding="utf-8-sig", index=False)

print(judges_pair_df)

