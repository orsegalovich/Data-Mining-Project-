import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pylab as pylab
import seaborn as sns
import numpy as np
import math

PETITIONERS_INDEX_LIST = ["P1","P2","P3"]
RESPONDENT_INDEX_LIST = ["R1", "R2","R3"]
SECTOR = "Sector"
GENDER = "Gender"
UNKNOWN = "Unknown"
UNDECIDABLE = "Undecidable"
LAWYER = "lawyer"
INCONCLUSIVE_G = "Inconclusive gender"
INCONCLUSIVE_S = "Inconclusive sector"
JEW = "Jew"
ARAB = "Arab"
MIXED = "Mixed"
WINNER_COURT = "winnercourt"
BOTH = "Both"
RESPONDENT = "Respondent"
PETITIONER = "Petitioner"
WINS = "Wins"
LOSSES = "Losses"
TOTAL = "Total"
df = pd.read_csv('..\cases_with_sector.csv', low_memory=False)


teams_counter = {JEW: 0, "Arab": 0, "Mixed": 0, "Undecidable": 0}
winning_teams_counter = {JEW: {"Both": 0, "Wins": 0, "Unknown": 0, "Losses": 0, "Total": 0},
                         "Arab": {"Both": 0, "Wins": 0, "Unknown": 0, "Losses": 0, "Total": 0},
                         "Mixed": {"Both": 0, "Wins": 0, "Unknown": 0, "Losses": 0, "Total": 0},
                         "Undecidable": {"Both": 0, "Wins": 0, "Unknown": 0, "Losses": 0, "Total": 0}}

winning_teams_counter_by_sides = \
                        {"Jew_p": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Arab_p": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Mixed_p": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Undecidable_p": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Jew_r": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Arab_r": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Mixed_r": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0},
                         "Undecidable_r": {"Both": 0, "Respondent": 0, "Unknown": 0, "Petitioner": 0, "Total": 0}}

P1_SECTOR_LST = df[LAWYER + PETITIONERS_INDEX_LIST[0] + SECTOR]
P2_SECTOR_LST = df[LAWYER + PETITIONERS_INDEX_LIST[1] + SECTOR]
P3_SECTOR_LST = df[LAWYER + PETITIONERS_INDEX_LIST[2] + SECTOR]
R1_SECTOR_LST = df[LAWYER + RESPONDENT_INDEX_LIST[0] + SECTOR]
R2_SECTOR_LST = df[LAWYER + RESPONDENT_INDEX_LIST[1] + SECTOR]
R3_SECTOR_LST = df[LAWYER + RESPONDENT_INDEX_LIST[2] + SECTOR]


def get_valid_sector_list(index, is_petitioner=True):
    if is_petitioner:
        if index == 0:
            return P1_SECTOR_LST
        elif index == 1:
            return P2_SECTOR_LST
        else:
            return P3_SECTOR_LST
    else:
        if index == 0:
            return R1_SECTOR_LST
        elif index == 1:
            return R2_SECTOR_LST
        else:
            return R3_SECTOR_LST


def get_team_sector_from_counter(lawyers_sector_dict):

    if lawyers_sector_dict[JEW] > 0 and lawyers_sector_dict[ARAB] > 0:
        return MIXED
    elif lawyers_sector_dict[JEW] > 0:
        return JEW
    elif lawyers_sector_dict[ARAB] > 0:
        return ARAB
    else:
        return UNDECIDABLE

def get_team_of_lawyers_sector(lawyers_list, row_ind, is_petitioner=True):
    team_of_lawyers_names_dict = dict()
    team_of_lawyers_gender_counter = {"Jew": 0, "Arab": 0, "Mixed": 0, "Undecidable": 0}
    if row_ind == 14219:
        d ="f"

    for index, column_header in enumerate(lawyers_list):
        column_name = LAWYER + column_header
        lawyer_name = df[column_name][row_ind]

        # validate lawyer_name exists (and is not NAN)
        if not lawyer_name or lawyer_name != lawyer_name:
            continue

        # validate no lawyer is counted twice in the same case
        if lawyer_name in team_of_lawyers_names_dict.keys():
            continue

        # remember name
        team_of_lawyers_names_dict[lawyer_name] = True

        lawyer_sector = get_valid_sector_list(index, is_petitioner)[row_ind]

        if lawyer_sector == "Unregistered" or lawyer_sector == UNKNOWN or lawyer_sector == INCONCLUSIVE_S:
            team_of_lawyers_gender_counter["Undecidable"] += 1
            continue

        team_of_lawyers_gender_counter[lawyer_sector] += 1
    return get_team_sector_from_counter(team_of_lawyers_gender_counter)

def calc_if_case_was_successful(case_result, is_petitioner=True):
    if case_result == BOTH:
        return BOTH
    elif case_result == UNKNOWN:
        return UNKNOWN
    elif is_petitioner:
        if case_result == PETITIONER:
            return WINS
        else:
            return LOSSES
    else:
        if case_result == PETITIONER:
            return LOSSES
        else:
            return WINS

def calculate_sector_appearances_and_victories_by_teams():
    all_cases_result = df[WINNER_COURT]

    #Iterate on every case
    for row_ind in df.index:
        # Get sectors of petitioners and respondents
        case_petitioners_sector = get_team_of_lawyers_sector(PETITIONERS_INDEX_LIST, row_ind, True)
        case_respondents_sector = get_team_of_lawyers_sector(RESPONDENT_INDEX_LIST, row_ind , False)
        # Get case Result
        case_result = all_cases_result[row_ind]
        # Count team sector
        teams_counter[case_petitioners_sector] += 1
        teams_counter[case_respondents_sector] += 1

        winning_teams_counter_by_sides[case_petitioners_sector + "_p"][case_result] += 1
        winning_teams_counter_by_sides[case_petitioners_sector + "_p"][TOTAL] += 1
        winning_teams_counter_by_sides[case_respondents_sector + "_r"][case_result] += 1
        winning_teams_counter_by_sides[case_respondents_sector + "_r"][TOTAL] += 1

        winning_teams_counter[case_petitioners_sector][calc_if_case_was_successful(case_result, True)] += 1
        winning_teams_counter[case_petitioners_sector][TOTAL] += 1
        winning_teams_counter[case_respondents_sector][calc_if_case_was_successful(case_result, False)] += 1
        winning_teams_counter[case_respondents_sector][TOTAL] += 1







calculate_sector_appearances_and_victories_by_teams()


def plot_data_function(title, yaxis_title, file_name, dict, label_size):

    pylab.rcParams.update({'xtick.labelsize': label_size})
    df_values = pd.DataFrame.from_dict(dict, orient='index')
    sorted_appearances = df_values.sort_values(by=0)
    sorted_appearances.plot(kind="bar")
    # plt.set(title="Genders and Sectors Distribution", xlabel="categories", ylabel="amount of cases")
    plt.xticks(rotation=45, ha='right')
    plt.title(title, fontsize=16)
    # plt.xlabel("categories", fontsize=10)
    plt.ylabel(yaxis_title, fontsize=12)
    plt.savefig(f"./sectors_visualization/{file_name}")
    #plt.show()
    plt.clf()
    plt.close()



def plot_pie(title, dict, file_name, flag=True):
    if flag:
        del dict[TOTAL]
    plt.pie(dict.values(),
            labels=dict.keys(),
            startangle=90, autopct='%.1f%%')
    plt.title(title)
    #plt.show()
    plt.savefig(f"./sectors_visualization/{file_name}")
    plt.clf()
    plt.close()



def create_noemalized_lst_of_total_case_results():
    case_results_total_dict = df[WINNER_COURT].value_counts().to_dict()
    total_results_lst = list()
    total_results_lst.append(int(case_results_total_dict[BOTH]))
    total_results_lst.append(int(case_results_total_dict[RESPONDENT]))
    total_results_lst.append(int(case_results_total_dict[UNKNOWN]))
    total_results_lst.append(int(case_results_total_dict[PETITIONER]))
    total_results_sum = sum(total_results_lst)
    total_results_normalized_lst = [int(val)/total_results_sum for val in total_results_lst]
    return (total_results_normalized_lst)



def create_hisotgram_of_noramilzed_petitioner_case_results():

    # calc normalized arab lst
    arab_petitioner_lst = list(winning_teams_counter_by_sides['Arab_p'].values())
    normalized_arab_petitioner_lst = [int(val)/int(arab_petitioner_lst[-1]) for val in arab_petitioner_lst][:-1]

    # calc normalized jewish lst
    jew_petitioner_lst = list(winning_teams_counter_by_sides['Jew_p'].values())
    normalized_jew_petitioner_lst = [int(val)/int(jew_petitioner_lst[-1]) for val in jew_petitioner_lst][:-1]
    # get label lst
    labels_lst = list(winning_teams_counter_by_sides['Jew_p'].keys())
    # get normalized list of all cases
    normalized_list_of_all_cases = create_noemalized_lst_of_total_case_results()
    # Save as DataFrame
    data = {"Case Results": labels_lst[:-1], 'Jew_petitioner': normalized_jew_petitioner_lst,
            'Arab_petitioner': normalized_arab_petitioner_lst, "Total": normalized_list_of_all_cases}
    df_new = pd.DataFrame(data)

    # Settings 0f labes size
    pylab.rcParams.update({'xtick.labelsize': '7'})

    # plot data
    df_new.plot(x="Case Results", kind="bar")
    plt.xticks(rotation=45, ha='right')

    plt.title("Normalized case results of Jewish and Arab petitions with total db distribution", fontsize=11)
    plt.savefig("./sectors_visualization/normalized_case_results_of_jewish_and_arab_petition")
    #plt.show()
    plt.clf()
    plt.close()



def create_hisotgram_of_noramilzed_respondent_case_results():
    # calc normalized arab lst
    arab_respondent_lst = list(winning_teams_counter_by_sides['Arab_r'].values())
    normalized_arab_respondent_lst = [int(val) / int(arab_respondent_lst[-1]) for val in arab_respondent_lst][:-1]

    # calc normalized jewish lst
    jew_respondent_lst = list(winning_teams_counter_by_sides['Jew_r'].values())
    normalized_jew_respondent_lst = [int(val) / int(jew_respondent_lst[-1]) for val in jew_respondent_lst][:-1]
    # get label lst
    labels_lst = list(winning_teams_counter_by_sides['Jew_r'].keys())
    # get normalized list of all cases
    normalized_list_of_all_cases = create_noemalized_lst_of_total_case_results()
    # Save as DataFrame
    data = {"Case Results": labels_lst[:-1], 'Jew_respondent': normalized_jew_respondent_lst,
            'Arab_respondent': normalized_arab_respondent_lst, "Total": normalized_list_of_all_cases}
    df_new = pd.DataFrame(data)

    # Settings 0f labes size
    pylab.rcParams.update({'xtick.labelsize': '7'})

    # plot data
    df_new.plot(x="Case Results", kind="bar")
    plt.xticks(rotation=45, ha='right')

    plt.title("Normalized case results of Jewish and Arab respondent with total db distribution", fontsize=11)
    plt.savefig("./sectors_visualization/normalized_case_results_of_jewish_and_arab_respondents")
    #plt.show()
    plt.clf()
    plt.close()


def create_histogram_for_normalized_petition_and_respondent_for_jews_and_arabs():

    jew_petition_and_respondents_lst_normalized = [
        (int(winning_teams_counter_by_sides["Jew_p"][TOTAL]) / int(teams_counter[JEW])),
        (int(winning_teams_counter_by_sides["Jew_r"][TOTAL]) / int(teams_counter[JEW]))]

    arab_petition_and_respondents_lst_normalized = [
        (int(winning_teams_counter_by_sides["Arab_p"][TOTAL])/ int(teams_counter[ARAB])),
        (int(winning_teams_counter_by_sides["Arab_r"][TOTAL])/ int(teams_counter[ARAB]))]

    total_dict = df[WINNER_COURT].value_counts().to_dict()
    total_cases = df[WINNER_COURT].count()

    total_petition_and_respondents_lst_normalized = [
        int(total_dict[PETITIONER])/ int(total_cases),
        int(total_dict[RESPONDENT])/ int(total_cases)]

    labels = [PETITIONER, RESPONDENT]

    data = {"Cases distribution": labels,
            'Jews distribution of petitions and respondents': jew_petition_and_respondents_lst_normalized,
            'Arabs distribution of petitions and respondents': arab_petition_and_respondents_lst_normalized,
            "Total distribution of petitions and respondents": total_petition_and_respondents_lst_normalized}

    df_new = pd.DataFrame(data)

    # Settings 0f labes size
    pylab.rcParams.update({'xtick.labelsize': '9'})

    # plot data
    df_new.plot(x="Cases distribution", kind="bar")
    plt.xticks(rotation=45, ha='right')

    plt.title("Normalized petitions and respondents of Jewish, Arab and total  distribution", fontsize=11)
    plt.savefig("./sectors_visualization/normalized_petitions_and_respondents_of_jewish_and_Arab_and_total_and_distribution")
    #plt.show()
    plt.clf()
    plt.close()

plot_data_function("Identified case teams by sectors", "sectors", "Identified_case_teams_by_sectors.png", teams_counter, 7)


plot_pie("SC case results for Jewish lawyers", winning_teams_counter[JEW], "case_results_for_Jewish_lawyers")
plot_pie("SC case results for Arab lawyers", winning_teams_counter[ARAB], "case_results_for_Arab_lawyers")
plot_pie("SC case results for Undecidable lawyers", winning_teams_counter[UNDECIDABLE], "case_results_for_Undecidable_lawyers")


case_results_total_dict = df[WINNER_COURT].value_counts().to_dict()
plot_pie("SC results of all cases", case_results_total_dict, "results_of_all_cases", False)


create_hisotgram_of_noramilzed_petitioner_case_results()
create_hisotgram_of_noramilzed_respondent_case_results()

create_histogram_for_normalized_petition_and_respondent_for_jews_and_arabs()

