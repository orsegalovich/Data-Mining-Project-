import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('layers_sector_gender.csv', low_memory=False)

cols_gender = ['lawyerP1Gender', 'lawyerP2Gender', 'lawyerP3Gender', 'lawyerR1Gender', 'lawyerR2Gender', 'lawyerR3Gender']
cols_sector = ['lawyerP1Sector', 'lawyerP2Sector', 'lawyerP3Sector', 'lawyerR1Sector', 'lawyerR2Sector', 'lawyerR3Sector']

def get_binary_variable_of_gender_lawyer_cases(cols):
    binary_gender = list()
    temp_case = 0
    for col in cols:
        for i in range(len(df['ISCD_ID'])):
            case = df['ISCD_ID'][i]
            case = int(case)
            if case != temp_case:
                temp_case = case
                if df[col][i] == 'Female':
                    binary_gender.append('Female')
                elif df[col][i] == 'Male':
                    binary_gender.append('Male')
                else:
                    binary_gender.append(2)
    return binary_gender

#To get a binary variable of
def get_binary_variable_of_sector_lawyer_cases(cols):
    binary_sector = list()
    temp_case = 0
    for col in cols:
        for i in range(len(df['ISCD_ID'])):
            case = df['ISCD_ID'][i]
            case = int(case)
            if case != temp_case:
                temp_case = case
                if df[col][i] == 'Jew':
                    binary_sector.append('Jew')
                elif df[col][i] == 'Arab':
                    binary_sector.append('Arab')
                else:
                    binary_sector.append(2)
    return binary_sector

#male_lawyer, female_lawyer
gender_lst = get_binary_variable_of_gender_lawyer_cases(cols_gender)

#jew_lawyer, arab_lawyer
sector_lst = get_binary_variable_of_sector_lawyer_cases(cols_sector)

#Save as DataFrame
data = {'Gender': gender_lst, 'Sector': sector_lst}
df_new = pd.DataFrame(data)
df_new = df_new[df_new['Gender'] != 2]
df_new = df_new[df_new['Sector'] != 2]

# data_to_plot1 = pd.crosstab(df_new["Gender"], df_new["Sector"], margins=True)
# data_to_plot2 = pd.crosstab(df_new["Gender"], df_new["Sector"], normalize=True)
#
# print(data_to_plot1.head())
# print(data_to_plot2.head())


def get_countplot(data, title, x_lab, y_lab):
    plot = sns.countplot(x="Sector", hue="Gender", data=data)
    plot.set(title = title, xlabel = x_lab , ylabel = y_lab)
    plt.savefig('Lawyers_divided_by_gender_and_sector.png')

# Get the plot
get_countplot(df_new, 'Lawyers divided by gender and sector', 'Division by background', 'Count')

