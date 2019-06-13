def crude_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Crude oil refined in the country
    cru_r_df = all_params['ProductionByTechnologyAnnual']
    cru_r_df=cru_r_df[cru_r_df['f'].str[:6]==cc+'CRU2'].copy()
    cru_r_df['t'] = cru_r_df['t'].str[2:10]
    cru_r_df['value'] = cru_r_df['value'].astype('float64')
    cru_r_df = cru_r_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    cru_r_df = cru_r_df.reindex(sorted(cru_r_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cru_r_df['y'] = years
    #cru_r_df=cru_r_df[cru_r_df['y']>2018]
    df_plot(cru_r_df,'Petajoules (PJ)',cc+'-'+'Crude oil refined in the country')
    #Crude oil production/imports/exports (Detailed)
    cru_df = all_params['ProductionByTechnologyAnnual']
    cru_df=cru_df[(cru_df['f'].str[:6]==cc+'CRU1')].copy()
    cru_df['t'] = cru_df['t'].str[2:10]
    cru_df['value'] = cru_df['value'].astype('float64')
    cru_df['t'] = cru_df['t'].astype(str)
    cru_df = cru_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    cru_df = cru_df.reindex(sorted(cru_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cru_df['y'] = years
    #cru_df=cru_df[cru_df['y']>2018]
    cru_df.iplot(x='y',
                  kind='bar', 
                  barmode='relative',
                  xTitle='Year',
                  yTitle="Petajoules (PJ)",
                  color=[color_dict[x] for x in cru_df.columns if x != 'y'],
                  title=cc+"-"+"Crude oil extraction, imports and exports",showlegend=True)
    