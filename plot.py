import pandas as pd

def df_plot(df, y_title, p_title):

    colorcode = pd.read_csv('./techcodes.csv', sep=',')
    colorcode2 = colorcode.drop('tech_code', axis=1)

    color_dict = dict([(a,b) for a,b in zip(colorcode2.tech_name, colorcode2.colour)])
    
    if len(df.columns) == 1:
        print('There are no values for the result variable that you want to plot')
    else:
         return df.iplot(x='y',
                         kind='bar', 
                         barmode='stack',
                         xTitle='Year',
                         yTitle=y_title,
                         color=[color_dict[x] for x in df.columns if x != 'y'],
                         title=p_title, 
                         showlegend=True)
