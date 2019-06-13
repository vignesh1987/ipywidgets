def hfo_lfo_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Heavy Fuel Oil overview
    hfo_df = all_params['ProductionByTechnologyAnnual']
    hfo_df=hfo_df[hfo_df['f'].str[:6]==cc+'HFOI'].copy()
    hfo_df['t'] = hfo_df['t'].str[2:10]
    hfo_df['value'] = hfo_df['value'].astype('float64')
    hfo_df = hfo_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    hfo_df = hfo_df.reindex(sorted(hfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #hfo_df['y'] = years
    #hfo_df=hfo_df[hfo_df['y']>2018]
    df_plot(hfo_df,'Petajoules (PJ)',cc+'-'+'HFO production by technology')
    #Light Fuel Oil overview
    lfo_df = all_params['ProductionByTechnologyAnnual']
    lfo_df=lfo_df[lfo_df['f'].str[:6]==cc+'LFOI'].copy()
    lfo_df['t'] = lfo_df['t'].str[2:10]
    lfo_df['value'] = lfo_df['value'].astype('float64')
    lfo_df = lfo_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    lfo_df = lfo_df.reindex(sorted(lfo_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #lfo_df['y'] = years
    #lfo_df=lfo_df[lfo_df['y']>2018]
    df_plot(lfo_df,'Petajoules (PJ)',cc+'-'+'LFO production by technology')