def water_chart (Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #print('The country code is:'+cc)
    #water withdrawal detailed
    wat_w_df = all_params['UseByTechnologyAnnual']
    wat_w_df=wat_w_df[wat_w_df['f'].str[:6]==cc+'WAT1'].copy()

    wat_w_df['t'] = wat_w_df['t'].str[2:10]
    wat_w_df['value'] = wat_w_df['value'].astype('float64')
    wat_w_df = wat_w_df.pivot_table(index='y', 
                                  columns='t',
                                  values='value', 
                                  aggfunc='sum').reset_index().fillna(0)
    wat_w_df = wat_w_df.reindex(sorted(wat_w_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #wat_w_df['y'] = years
    #wat_w_df=wat_w_df[wat_w_df['y']>2018]
    #df_plot(wat_w_df,'Million cubic metres (Mm^3)',cc+"-"+'Water Withdrawal')
    ###
    #Water Withdrawal (Aggregated)
    watw_agg_df = pd.DataFrame(columns=agg_col)
    watw_agg_df.insert(0,'y',wat_w_df['y'])
    watw_agg_df  = watw_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_w_df.columns:
                watw_agg_df[each] = watw_agg_df[each] + wat_w_df[tech_exists]
                watw_agg_df[each] = watw_agg_df[each].round(2)

    df_plot(watw_agg_df,'Million cubic metres (Mm^3)',cc+"-"+'Water Withdrawal')
    ##
    #water output detailed
    wat_o_df = all_params['ProductionByTechnologyAnnual']
    wat_o_df=wat_o_df[wat_o_df['f'].str[:6]==cc+'WAT2'].copy()
    wat_o_df['t'] = wat_o_df['t'].str[2:10].copy()
    wat_o_df['value'] = wat_o_df['value'].astype('float64')
    wat_o_df = wat_o_df.pivot_table(index='y', 
                                 columns='t',
                                 values='value', 
                                 aggfunc='sum').reset_index().fillna(0)
    wat_o_df = wat_o_df.reindex(sorted(wat_o_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #wat_o_df['y'] = years
    #wat_o_df=wat_o_df[wat_o_df['y']>2018]
    #df_plot(wat_o_df,'Million cubic metres (Mm^3)',cc+"-"+'Water output')
    ###
    #Water consumption missing row additions
    for wd in wat_w_df.columns:
        for wc in wat_o_df.columns:
            if wd in wat_o_df.columns:
                pass
            else:
                wat_o_df[wd]=0
    #####
    ####Water consumption (Detailed)
    wat_c_df=wat_w_df.set_index('y')-wat_o_df.set_index('y')
    wat_c_df=wat_c_df.fillna(0.00)
    wat_c_df.reset_index(inplace=True)
    #wat_c_df['y']=years
    #df_plot(wat_c_df,'Million cubic metres (Mm^3)',cc+"-"+'Water consumption')
    #Water consumption (Aggregate)
    watc_agg_df = pd.DataFrame(columns=agg_col)
    watc_agg_df.insert(0,'y',wat_c_df['y'])
    watc_agg_df  = watc_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_c_df.columns:
                watc_agg_df[each] = watc_agg_df[each] + wat_c_df[tech_exists]
                watc_agg_df[each] = watc_agg_df[each].round(2)
    df_plot(watc_agg_df,'Million cubic metres (Mm^3)',cc+'-'+'Water consumption aggregated')

