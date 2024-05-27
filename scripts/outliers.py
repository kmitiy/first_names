import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function to calculate decline rate. Needs to be a function so it can be applied to each row in the dataframe
def calculate_decline_rate(group, decline_period, decline_threshold):
    
    peak_year = group.loc[group['rank'].idxmax(), 'year']
    post_peak_years = group[group['year'] > peak_year]
    post_peak_years = post_peak_years.sort_values(by='year')
    
    if len(post_peak_years) < decline_period:
        return None
    
    # Check if name drops out of top N within the specified decline period
    for i in range(decline_period):
        if i < len(post_peak_years) and post_peak_years.iloc[i]['rank'] > decline_threshold:
            return post_peak_years.iloc[i]['year']
    return None
    

# Code to execute is put in main function. That way, it can run directly in this script (by putting the function into the if-statement at the bottom)
# and can be imported and run in other scripts as well (like main.py)
def main():
    # Raw data CSV file is imported into pandas dataframes
    df_first_names_ch = pd.read_csv(r"C:\Users\A933904\Downloads\vornamen\raw_data_enhanced.csv", sep=";", encoding='utf-8')
        
    # Threshold is defined (e.g., drop out of top 50 within 3 years)
    decline_period = 3
    decline_threshold = 100
    
    
    # Filter dataset for top N names
    # df_names_with_rapid_decline = df_first_names_ch[df_first_names_ch['rank'] < decline_threshold]    
    
    group_std = df_first_names_ch.groupby(['name', 'sex'])['rank'].std()*3
    df_std = group_std.reset_index()
    df_std.columns = ['name', 'sex', 'std']
    df_first_names_ch = df_first_names_ch.merge(df_std, on=['name', 'sex'])
    
    group_avg = df_first_names_ch.groupby(['name', 'sex'])['rank'].mean()
    df_avg = group_avg.reset_index()
    df_avg.columns = ['name', 'sex', 'avg']
    df_first_names_ch = df_first_names_ch.merge(df_avg, on=['name', 'sex'])
    
    print(df_first_names_ch.head())
    
    # Content of df is written into a CSV file. Encoding 'utf-8-sig' is used to accurately read Umlaute (like 'ö', 'ä', 'ü', 'é', etc.). For example, 'Ömer'
    # would be written into the CSV file as 'Ã–mer' if encoding 'utf-8' was used
    df_first_names_ch.to_csv(r"C:\Users\A933904\Downloads\vornamen\outliers.csv", index=False, sep=';', encoding='utf-8-sig')
    
    # grouped = top_names.groupby(['name', 'sex'])
    # longevity = grouped['year'].nunique().reset_index()
    # longevity.columns = ['name', 'sex', years_in_top_n_lbl]
    
    # longest_streak = grouped.apply(calculate_longest_streak).reset_index()
    
    
    # The rows are sorted according to sex, then name and lastly year. This is a pre-requisite for the loop that iterates through the df in the next step
    # df_names_with_rapid_decline.sort_values(by=['sex', 'name', 'year'])
    
    # # The df is being iterated over. Each row is compared with its predecesor. If both records have the same sex, samne name and are one year apart, the
    # # ranks are subtracted from each other and the result is assigned to the "rank_change_yoy" column. If the conditions are not fulfilled, calculating
    # # the rank change does not make sense and the value in the corresponding column remains at nan.
    # for i in range(len(df_first_names_ch)):
    #     if i > 0:
    #         if df_first_names_ch.iloc[i, 5]
    #         same_sex = (df_first_names_ch.iloc[i, 2] == df_first_names_ch.iloc[i-1, 2])
    #         same_name = (df_first_names_ch.iloc[i, 0] == df_first_names_ch.iloc[i-1, 0])
    #         one_year_diff = ((df_first_names_ch.iloc[i, 1] - 1) == df_first_names_ch.iloc[i-1, 1])
    #         if same_sex and same_name and one_year_diff:
    #             df_first_names_ch.iloc[i, 6] = df_first_names_ch.iloc[i-1, 5] - df_first_names_ch.iloc[i, 5]
    
    
    
    
    
    # df_names_with_rapid_decline = df_first_names_ch[df_first_names_ch['rank'] > decline_threshold]
    # df_names_with_rapid_decline = df_names_with_rapid_decline[df_names_with_rapid_decline['rank'] + df_names_with_rapid_decline['rank_change_yoy'] <= decline_threshold]
    # df_names_with_rapid_decline = df_names_with_rapid_decline[df_first_names_ch['rank_change_yoy'] < -50].reset_index()
    
    # print(df_names_with_rapid_decline.tail())
    
if __name__ == "__main__":
    main()