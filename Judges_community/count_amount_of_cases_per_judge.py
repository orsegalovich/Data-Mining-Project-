import pandas as pd

df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCountAndDuration.csv', low_memory=False, na_filter=False)
df2 = pd.read_csv('..\PairOfJudgesAndMutualCaseCount.csv', low_memory=False, na_filter=False)


# def get_judges_dict_with_vals_as_zero():
#     judges_list = df['Name'].to_list()
#     judges_dict = dict()
#     for judge in judges_list:
#         if judge not in judges_dict:
#             judges_dict[judge] = 0
#
#
#     return judges_dict
#
# judges_dict = get_judges_dict_with_vals_as_zero()

judges_dict = dict()
judges_name_by_cases = df['Name'].to_list()

for name in judges_name_by_cases:
    if name not in judges_dict:
        judges_dict[name] = 1
    else:
        judges_dict[name] += 1



for row_ind in df2.index:
    to_add = judges_dict[df2["judge_a"][row_ind]] + judges_dict[df2["judge_b"][row_ind]]
    df2.at[row_ind, 'sum_of_both_individual_appearances'] = to_add
    mutual = df2.loc[row_ind, 'mutual_appearances']
    df2.at[row_ind, 'ratio'] = mutual/to_add




# df2 = pd.read_csv('PairOfJudgesAndMutualCaseCount.csv', encoding="utf-8-sig", index=False)

df2.to_csv('..\PairOfJudgesAndMutualCaseCount.csv', encoding="utf-8-sig", index=False)

print(df2.head())
