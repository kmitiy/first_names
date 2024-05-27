import pandas as pd
import numpy as np


# Function to calculate proportianality of names. Needs to be a function so it can be applied to each row in the dataframe
def add_prop(group):
    group['prop'] = group["births"] / group["births"].sum()
    return group

# Code to execute is put in main function. That way, it can run directly in this script (by putting the function into the if-statement at the bottom)
# and can be imported and run in other scripts as well (like main.py)
def main():
    # Raw data CSV files are imported into pandas dataframes (one for male and one for female)
    df_first_names_male_by_canton = pd.read_csv(r"C:\Users\A933904\Downloads\vornamen\Rohdaten\vornamen_schweiz_seit-2000_rohdaten_nach_kanton_m.csv", sep=";", encoding='utf-8')
    df_first_names_female_by_canton = pd.read_csv(r"C:\Users\A933904\Downloads\vornamen\Rohdaten\vornamen_schweiz_seit-2000_rohdaten_nach_kanton_w.csv", sep=";", encoding='utf-8')
    
    # Column for sex is added
    df_first_names_male_by_canton["sex"] = "m"
    df_first_names_female_by_canton["sex"] = "f"
    
    # Two dfs are combined into one
    df_first_names_by_canton = pd.concat([df_first_names_male_by_canton, df_first_names_female_by_canton], ignore_index=True)
    
    # The number of births are aggregated along name, year and sex. The canton is excluded from the dataset since we are only interested in looking at the
    # data across all of Switzerland, without going deeper into the regions.
    df_first_names_ch = df_first_names_by_canton.groupby(['name', 'year', 'sex'])['births'].sum().reset_index(name='births')
    
    # The relative proportion of each name per year and sex is added as a new column (think of the values as percentages)
    df_first_names_ch = df_first_names_ch.groupby(['year', 'sex']).apply(add_prop)
    
    # Using the proportional value, a ranking is created per year and sex for each name. The ranking is added as a new column (the value 1 would signify the
    # the most popular name per this year and sex)
    df_first_names_ch['rank'] = df_first_names_ch.groupby(['year', 'sex'])['prop'].rank(method='min', ascending=False)
    
    # The year-on-year rank change is added as a new column and filled with nan values
    df_first_names_ch['rank_change_yoy'] = np.nan
    
    # The rows are sorted according to sex, then name and lastly year. This is a pre-requisite for the loop that iterates through the df in the next step
    df_first_names_ch = df_first_names_ch.sort_values(by=['sex', 'name', 'year'])
    print(df_first_names_ch.head())
    print(df_first_names_ch.tail())
    
    # The df is being iterated over. Each row is compared with its predecesor. If both records have the same sex, samne name and are one year apart, the
    # ranks are subtracted from each other and the result is assigned to the "rank_change_yoy" column. If the conditions are not fulfilled, calculating
    # the rank change does not make sense and the value in the corresponding column remains at nan.
    for i in range(len(df_first_names_ch)):
        if i > 0:
            same_sex = (df_first_names_ch.iloc[i, 2] == df_first_names_ch.iloc[i-1, 2])
            same_name = (df_first_names_ch.iloc[i, 0] == df_first_names_ch.iloc[i-1, 0])
            one_year_diff = ((df_first_names_ch.iloc[i, 1] - 1) == df_first_names_ch.iloc[i-1, 1])
            if same_sex and same_name and one_year_diff:
                df_first_names_ch.iloc[i, 6] = df_first_names_ch.iloc[i-1, 5] - df_first_names_ch.iloc[i, 5]
    
    # Content of df is written into a CSV file. Encoding 'utf-8-sig' is used to accurately read Umlaute (like 'ö', 'ä', 'ü', 'é', etc.). For example, 'Ömer'
    # would be written into the CSV file as 'Ã–mer' if encoding 'utf-8' was used
    df_first_names_ch.to_csv(r"C:\Users\A933904\Downloads\vornamen\raw_data_enhanced.csv", index=False, sep=';', encoding='utf-8-sig')

if __name__ == "__main__":

    main()