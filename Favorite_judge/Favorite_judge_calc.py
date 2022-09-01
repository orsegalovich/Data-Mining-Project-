import pandas as pd
from matplotlib import pyplot as plt

plt.rcdefaults()
fig, ax = plt.subplots()

df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCountAndDuration.csv', low_memory=False)

def avg_words_in_verdict_by_judge(judge):
    judge_cases = 0
    judge_total_words = 0
    for i in range(len(df['Name'])):
        if df['Name'][i] == judge and str(df['words_in_verdict'][i]) != "nan":
            #One case which has a broken url and thus can't be calculated.
            judge_cases += 1
            judge_total_words += df['words_in_verdict'][i]
    return judge_total_words/judge_cases

def get_plot_of_all_judges_and_avg_words_in_verdict():
    judges = (pd.unique(df['Name']))
    avg_list = list()
    dict_of_judges = dict()
    for judge in judges:
        avg_list.append(avg_words_in_verdict_by_judge(judge))
        dict_of_judges[judge] = avg_words_in_verdict_by_judge(judge)
    ordered_dict = {k: v for k, v in sorted(dict_of_judges.items(), key=lambda item: item[1])}
    # ax.barh(judges, avg_list, align='center')
    # ax.set_yticks(judges, labels=judges)
    # ax.invert_yaxis()
    # ax.set_xlabel('Performance')
    # ax.set_title('How fast do you want to go today?')
    # plt.show()
    ax.barh(list(ordered_dict.keys()), list(ordered_dict.values()), align='center')
    ax.set_yticks(list(ordered_dict.keys()), labels=list(ordered_dict.keys()))
    ax.invert_yaxis()
    ax.set_xlabel('AVG words in verdict')
    ax.set_title('Judges by AVG words in verdict')
    plt.savefig("./Judges_by_avg_words_in_verdict")
    plt.clf()
    plt.show()
    return

#Get plot of average words by verdict
get_plot_of_all_judges_and_avg_words_in_verdict()

