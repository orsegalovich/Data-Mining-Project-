import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Read from db
df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCountAndDuration.csv', low_memory=False, na_filter=False)



judges_appearances_dict = dict()
# Count amount of appearances for each judge in all cases
def count_appearances_of_judges_in_cases():
    judges_name_by_cases = df['Name'].to_list()
    for name in judges_name_by_cases:
        if name not in judges_appearances_dict:
            judges_appearances_dict[name] = 1
        else:
            judges_appearances_dict[name] += 1


count_appearances_of_judges_in_cases()

# Generate wordcloud
wc = WordCloud(background_color="white", width=1000, height=500, normalize_plurals=False).generate_from_frequencies(judges_appearances_dict)
plt.xticks([])
plt.yticks([])


plt.imshow(wc)

plt.title("Judges word cloud - size correlates to amount of appearances")
plt.savefig("./judges_cases_visualization/judges_word_cloud_by_appearances")



