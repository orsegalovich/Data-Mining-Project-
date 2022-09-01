import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np




df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCountAndDuration.csv', low_memory=False)
df['case_duration'] = pd.to_numeric(df['case_duration'],errors='coerce')
df['numHearings'] = pd.to_numeric(df['numHearings'],errors='coerce')


x = list()
y = list()
x_y = list()
for row_ind in range(len(df.index)):
    if df["case_duration"][row_ind] >= 0:
        x_y.append([df["numHearings"][row_ind], df["case_duration"][row_ind]])

x_y.sort(key=lambda x: x[0],reverse=True)

for i in range(len(x_y)):
    x.append(x_y[i][0])
    y.append(x_y[i][1])

df2 = df[['numHearings', 'case_duration']]
# plt.matshow(df2.corr())
# plt.show()


# sns.set(style="ticks", color_codes=True)
# g = sns.pairplot(df2)
# plt.show()
def create_correlation():
    sns.regplot(x=x, y=y)
    plt.show()

create_correlation()
# piv = pd.pivot_table(df2["case_duration"] ,index=["numHearings"], columns=["case_duration"], fill_value=0)
# ax = sns.heatmap(piv, square=True)
# plt.setp( ax.xaxis.get_majorticklabels(), rotation=90 )
# plt.tight_layout()
# plt.show()


# x_axis = np.appray(x)
# y_axis = np.array(y)
# combined = np.vstack((x_axis, y_axis)).T

# a = np.vstack((x, y)).T
# print(a)


max_duration = df["case_duration"].max()
max_duration = 365
print(max_duration)
hearings_duration_hit_lst = list()
for her_ind in range(12):
    hearings_duration_hit_lst.append([])
    for dur_ind in range(int(max_duration//10 +1)):
        hearings_duration_hit_lst[her_ind].append(0)
print(hearings_duration_hit_lst)
count = 0
for i in range(len(x_y)):
    count+=1
    #Todo: make this less messy
    try:
        x_as_ind = int(x[i])
        y_as_ind = int(y[i]//10)
        if int(y[i]) <=max_duration:
            hearings_duration_hit_lst[x_as_ind][y_as_ind] += 1
    except ValueError:
        print("value error")
print(hearings_duration_hit_lst)
print(count)
c = np.array(hearings_duration_hit_lst)
ax = sns.heatmap(c, linewidth=0.5)
plt.show()


# List 1 with 11 items
# Each item will contain MaxDuration/100 for said num of Hearing
