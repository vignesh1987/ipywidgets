def coal_biomass_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #Coal overview
    coal_df = all_params['ProductionByTechnologyAnnual']
    coal_df=coal_df[coal_df['f'].str[:6]==cc+'COAL'].copy()
    coal_df['t'] = coal_df['t'].str[2:10]
    coal_df['value'] = coal_df['value'].astype('float64')
    coal_df = coal_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    coal_df = coal_df.reindex(sorted(coal_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #coal_df['y'] = years
    #coal_df=coal_df[coal_df['y']>2018]
    df_plot(coal_df,'Petajoules (PJ)',cc+'-'+'Coal production by technology')
    #Biomass overview
    biom_df = all_params['ProductionByTechnologyAnnual']
    biom_df=biom_df[biom_df['f'].str[:6]==cc+'BIOM'].copy()
    biom_df['t'] = biom_df['t'].str[2:10]
    biom_df['value'] = biom_df['value'].astype('float64')
    biom_df = biom_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    biom_df = biom_df.reindex(sorted(biom_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #biom_df['y'] = years
    #biom_df=biom_df[biom_df['y']>2018]
    df_plot(biom_df,'Petajoules (PJ)',cc+'-'+'Biomass production by technology')