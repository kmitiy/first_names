import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.renderers.default='browser'
from dash import Dash, html, Input, Output, callback


# Function to calculate longest streak in top N. Needs to be a function so it can be applied to each row in the dataframe
def calculate_longest_streak(group):
    years = group['year'].sort_values().to_list()
    longest_streak = current_streak = 1
    for i in range(1, len(years)):
        if years[i] == years[i-1]+1:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    return longest_streak


# Function to filter the whole dataset for one name (and one sex)
def filter_for_one_name(df_all_names, name, sex):
    return df_all_names[(df_all_names['name'] == name) & (df_all_names['sex'] == sex)]


def get_df_rank_table(df_one_name):
    return df_one_name[['year', 'rank', 'rank_change_yoy']].sort_values(by='year', ascending=False)


def visualize_name_freq_over_time(fig, df_one_name):
    
    fig.add_trace(go.Scatter(mode='lines+markers', name='absolute', x=df_one_name['year'], y=df_one_name['births'], marker=dict(size=8, symbol='diamond',
                              line=dict(width=2, color='DarkSlateGrey'))
                             ),
                  row=1,col=1)
    
    fig.add_trace(go.Scatter(mode='lines+markers', name='relative', x=df_one_name['year'], y=df_one_name['prop'], marker=dict(size=8, symbol='diamond',
                              line=dict(width=2, color='DarkSlateGrey'))
                             ),
                  row=2,col=1)
    
    fig.update_layout(title=dict(text="Births Over Time", font=dict(size=36), x=0.5, xanchor='center'),
                      yaxis=dict(title='Number of Births'),
                      yaxis2=dict(title='Share of Births', tickformat=',.4%'),
                      showlegend=False,
                      hovermode="x unified")
    
    return fig


def get_font_colors_for_numbers(df, col_name):
    
    font_colors = []
    for val in df[col_name].to_list()[::-1]:
        if val == 0 or np.isnan(val):
            font_colors.append('black')
        elif val < 0:
            font_colors.append('red')
        else:
            font_colors.append('green')
    return font_colors[::-1]


def visualize_name_rank_over_time(fig, df_one_name_rank_table, font_colors_numbers):
    fig.add_trace(go.Table(header=dict(values=['Year', 'Rank', 'Year-Over-Year Change'], align='center', height=25),
                            cells=dict(values=[df_one_name_rank_table['year'], df_one_name_rank_table['rank'], df_one_name_rank_table['rank_change_yoy']],
                                      align='center', 
                                      height=25)),
                  row=[1,2], col=2)
    
# =======================================================================================
# ====== Tried to implement conditional font formatting for yoy rank change column ======
# =======================================================================================
#     fig.add_trace(go.Table(header=dict(values=['Year', 'Rank', 'Year-Over-Year Change', 'colors'], align='center', height=25),
#                             cells=dict(values=[df_one_name_rank_table['year'], df_one_name_rank_table['rank'], df_one_name_rank_table['rank_change_yoy'], font_colors_numbers],
#                                       align='center', 
#                                       font=dict(color=['black', 'black', font_colors_numbers, font_colors_numbers]),
#                                       height=25)),
#                   row=[1,2], col=2)
# =======================================================================================
# ====== Tried to implement conditional font formatting for yoy rank change column ======
# =======================================================================================
    
    return fig


def main_single_name():
    
    df_all_names = pd.read_csv(r"/Users/kaimitiyamulle/personal_projects/first_names_git_repo/first_names/raw_data/raw_data_enhanced.csv", sep=";", encoding='utf-8')
    
    df_one_name = filter_for_one_name(df_all_names, 'Thiago', 'm')
    df_one_name_rank_table = get_df_rank_table(df_one_name)
    
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {'type':'table', 'rowspan':2}], [{}, None]], shared_xaxes=False)
    
    fig = visualize_name_freq_over_time(fig, df_one_name)
    
    font_colors_numbers = get_font_colors_for_numbers(df_one_name_rank_table, 'rank_change_yoy')
    
    fig = visualize_name_rank_over_time(fig, df_one_name_rank_table, font_colors_numbers)
    
    fig.show()
    
    return None

def run_dash_app():
    
    # Instantiate dash app
    app = Dash(__name__)
        
    app.layout = html.H1('Hello kakaka')
    
    app.run_server(debug=True, host='0.0.0.0', port='9999')
    
    return None
        

# Code to execute is put in main function. That way, it can run directly in this script (by putting the function into the if-statement at the bottom)
# and can be imported and run in other scripts as well (like main.py)
def main():
    # Raw data CSV file is imported into pandas dataframes
    df_first_names_ch = pd.read_csv(r"/Users/kaimitiyamulle/personal_projects/first_names_git_repo/first_names/raw_data/raw_data_enhanced.csv", sep=";", encoding='utf-8')
    
    # Define thresholds to identify 'popular' names
    top_n = 10 # Top 10 names
    total_years = df_first_names_ch['year'].nunique()
    years_consistent = total_years // 2 # Minimum years for consistency -> if present in 50% of the top 10s
    years_in_top_n_lbl = 'years_in_top_'+  str(top_n)
    
    # Filter dataset for top N names
    top_names = df_first_names_ch[df_first_names_ch['rank'] <= top_n]
    
    grouped = top_names.groupby(['name', 'sex'])
    longevity = grouped['year'].nunique().reset_index()
    longevity.columns = ['name', 'sex', years_in_top_n_lbl]
    
    longest_streak = grouped.apply(calculate_longest_streak).reset_index()
    longest_streak.columns = ['name', 'sex', 'longest_streak_in_top_'+str(top_n)]
    
    longevity = longevity.merge(longest_streak, on=['name', 'sex'])
    
    longevity['consistent_presence'] = (longevity[years_in_top_n_lbl] >= years_consistent)
    
    consistent_names = longevity[longevity['consistent_presence']].reset_index()
    
    main_single_name()
    
if __name__ == "__main__":
    # main()
    run_dash_app()
    
    