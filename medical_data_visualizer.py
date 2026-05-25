import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##1. import data
df = pd.read_csv('medical_examination.csv')

##2. Add overweight column (BMI = weight (kg) / height (m) **2)
df['overweight'] = (df['weight'] / (df['height']/100)**2).round(2)
df['overweight'] = np.where(df['overweight'] > 25, 1, 0)

##3. Normalize data by making 0 always good and 1 always bad. (cholesterol or gluc = 1 -> 0, >1 -> 1)
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

##4. Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
##5. Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
##6. Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
##7. Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import: sns.catplot().
    graph = sns.catplot(
        x='variable', 
        y='total', 
        hue='value', 
        col='cardio', 
        data=df_cat, 
        kind='bar')
##8. Get the figure for the output and store it in the fig variable.
    fig = graph.fig
##9. Do not modify the next two lines !!
    fig.savefig('catplot.png')
    return fig

##10. Draw the Heat Map in the draw_heat_map function.
def draw_heat_map():
##11. Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &  ##diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
        (df['height'] >= df['height'].quantile(0.025)) &  ##height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
        (df['height'] <= df['height'].quantile(0.975)) &  ##height is more than the 97.5th percentile
        (df['weight'] >= df['weight'].quantile(0.025)) &  ##weight is less than the 2.5th percentile
        (df['weight'] <= df['weight'].quantile(0.975))]    ##weight is more than the 97.5th percentile
##12. Calculate the correlation matrix and store it in the corr variable.
    corr = df_heat.corr()
##13. Generate a mask for the upper triangle and store it in the mask variable.
    mask = np.triu(np.ones_like(corr, dtype=bool))
##14. Set up the matplotlib figure.
    fig, ax = plt.subplots(figsize=(12, 12))
##15. Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap().
    sns.heatmap(
        corr, 
        mask = mask,
        center = 0,
        annot = True, 
        fmt = ".1f", 
        linewidths = 0.5, 
        square = True, 
        cbar_kws = {"shrink": 0.5},
        ax = ax )
##Do not modify the next two lines !!
    fig.savefig('heatmap.png')
    return fig
