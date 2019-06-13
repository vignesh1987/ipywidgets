def power_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #print('The country code is:'+cc)
    # Power capacity (detailed)
    #cap_df = all_params['TotalCapacityAnnual'][all_params['TotalCapacityAnnual'].t.str.startswith('PWR')].drop('r', axis=1)
    cap_df = all_params['TotalCapacityAnnual']
    cap_df=cap_df[cap_df['t'].str[:2]==cc].copy()
    cap_df['t'] = cap_df['t'].str[2:10]
    cap_df['value'] = cap_df['value'].astype('float64')
    cap_df = cap_df[cap_df['t'].isin(t_include)].pivot_table(index='y', 
                                               columns='t',
                                               values='value', 
                                               aggfunc='sum').reset_index().fillna(0)
    cap_df = cap_df.reindex(sorted(cap_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cap_df['y'] = years
    #cap_df=cap_df[cap_df['y']>2018]
    # The following code can be unhashed to get a detailed power capcity graph.
    #df_plot(cap_df,'Gigawatts (GW)',cc+"-"+'Power Generation Capacity (Detail)')
    #***********************************************
    # Power capacity (Aggregated)
    cap_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_agg_df.insert(0,'y',cap_df['y'])
    cap_agg_df  = cap_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_df.columns:
                cap_agg_df[each] = cap_agg_df[each] + cap_df[tech_exists]
                cap_agg_df[each] = cap_agg_df[each].round(3)
    #
    df_plot(cap_agg_df,'Gigawatts (GW)',cc+"-"+'Power Generation Capacity (Aggregate)')
  ## Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    #gen_df=gen_df[gen_df['t'].str[:2]==cc].copy()
    #gen_df['t'] = gen_df['t'].str[2:10]
    gen_df=gen_df[(gen_df['f'].str[:2]==cc)].copy()
    gen_df=gen_df[(gen_df['f'].str[2:6]=='EL01')|(gen_df['f'].str[2:6]=='EL03')].copy()
    gen_df=gen_df[(gen_df['t'].str[2:10]!='EL00T00X')&(gen_df['t'].str[2:10]!='EL00TDTX')].copy()
    gen_df['value'] = gen_df['value'].astype('float64')
    gen_df = gen_df.pivot_table(index='y', 
                                           columns='t',
                                           values='value', 
                                           aggfunc='sum').reset_index().fillna(0)
    for each in gen_df.columns:
        if len(each)!=1:
            if (each[2:4]=='EL') & (each[6:10]=='BP00'):
                pass
            else:
                gen_df.rename(columns={each:each[2:10]},inplace=True)
        else:
            pass
    gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #gen_df['y'] = years
    #gen_df=gen_df[gen_df['y']>2018]
    #df_plot(gen_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Detail)')
    #####
    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_pow_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
    df_plot(gen_agg_df,'Petajoules (PJ)',cc+"-"+'Power Generation (Aggregate)')
    # New capacity (detailed)
    cap_new_df = all_params['NewCapacity']
    cap_new_df=cap_new_df[cap_new_df['t'].str[:2]==cc].copy()
    cap_new_df['t'] = cap_new_df['t'].str[2:10]
    cap_new_df['value'] = cap_new_df['value'].astype('float64')
    cap_new_df = cap_new_df[cap_new_df['t'].isin(t_include)].pivot_table(index='y', 
                                               columns='t',
                                               values='value', 
                                               aggfunc='sum').reset_index().fillna(0)
    cap_new_df = cap_new_df.reindex(sorted(cap_new_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #cap_new_df['y'] = years
    #cap_new_df=cap_new_df[cap_new_df['y']>2018]
    # The following code can be unhashed to get a detailed power capacity graph.
    #df_plot(cap_new_df,'Gigawatts (GW)','New Power Generation Capacity (Detail)')
    #***********************************************
    # Power capacity (Aggregated)
    cap_new_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_new_agg_df.insert(0,'y',cap_new_df['y'])
    cap_new_agg_df  = cap_new_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_new_df.columns:
                cap_new_agg_df[each] = cap_new_agg_df[each] + cap_new_df[tech_exists]
                cap_new_agg_df[each] = cap_new_agg_df[each].round(3)
                ##
    df_plot(cap_new_agg_df,'Gigawatts (GW)',cc+"-"+ 'New power generation capacity (Aggregate)')
    
