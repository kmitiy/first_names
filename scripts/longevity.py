import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pio.renderers.default='browser'


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

# Code to execute is put in main function. That way, it can run directly in this script (by putting the function into the if-statement at the bottom)
# and can be imported and run in other scripts as well (like main.py)
def main():
    # Raw data CSV file is imported into pandas dataframes
    df_first_names_ch = pd.read_csv(r"C:\Users\A933904\Downloads\vornamen\raw_data_enhanced.csv", sep=";", encoding='utf-8')
    
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
    
    
# =============================== Here, parameters are added. Ideally, this is integrated into the UI ==============================================
     
    plotly_filter = df_first_names_ch[(df_first_names_ch['name'] == 'Thiago') & (df_first_names_ch['sex'] == 'm')]
    # print(plotly_filter.head())
     
# =============================== Here, parameters are added. Ideally, this is integrated into the UI ==============================================
    
    
    plotly_rank_table = plotly_filter[['year', 'rank', 'rank_change_yoy']].sort_values(by='year', ascending=False)

    fig = make_subplots(rows=2, cols=2, specs=[[{}, {'type':'table', 'rowspan':2}], [{}, None]], shared_xaxes=False)
    
    
    fig.add_trace(go.Scatter(mode='lines+markers', name='absolute', x=plotly_filter['year'], y=plotly_filter['births'], marker=dict(size=8, symbol='diamond',
                              line=dict(width=2, color='DarkSlateGrey'))
                             ),
                  row=1,col=1)
    
    fig.add_trace(go.Scatter(mode='lines+markers', name='relative', x=plotly_filter['year'], y=plotly_filter['prop'], marker=dict(size=8, symbol='diamond',
                              line=dict(width=2, color='DarkSlateGrey'))
                             ),
                  row=2,col=1)
    
    # tbl_val_font_colors = [('black' if val = 0 else '#ff2d5d' if val > 0 else '#04b29b') for val in plotly_filter['rank_change_yoy'].to_list()]
    
    # figure out correct order!!!
    tbl_val_font_colors = []
    for val in plotly_filter['rank_change_yoy'].to_list()[::-1]:
        if val == 0:
            tbl_val_font_colors.append('black')
        elif val < 0:
            tbl_val_font_colors.append('#ff2d5d')
        else:
            tbl_val_font_colors.append('#04b29b')
            
    fig.add_trace(go.Table(header=dict(values=['Year', 'Rank', 'Year-Over-Year Change'], align='center', height=45.5),
                           cells=dict(values=[plotly_rank_table['year'], plotly_rank_table['rank'], plotly_rank_table['rank_change_yoy']],
                                      align='center', 
                                      font=dict(color=['black', 'black', tbl_val_font_colors]),
                                      height=45.5)),
                  row=[1,2], col=2)

    
    fig.update_layout(title=dict(text="Births Over Time", font=dict(size=36), x=0.5, xanchor='center'),
                      yaxis=dict(title='Number of Births'),
                      yaxis2=dict(title='Share of Births', tickformat=',.4%'),
                      showlegend=False,
                      hovermode="x unified")
    
    # why does this not work like here? https://plotly.com/python/marker-style/#custom-marker-symbols
    # fig.update_traces(marker=dict(size=20, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")), selector=dict(mode="markers"))
    
    fig.show()
    
if __name__ == "__main__":
    main()