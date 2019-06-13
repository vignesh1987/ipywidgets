def gas_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #GAS Production (Detailed)
    gas_df = all_params['ProductionByTechnologyAnnual']
    gas_df_export1=gas_df[(gas_df['t'].str[0:4]==cc+'NG')&(gas_df['t'].str[6:10]=='BP00')].copy()
    gas_df_export1['value'] = gas_df_export1['value'].astype(float)*-1
    gas_df_import1=gas_df[(gas_df['t'].str[2:10]=='NG'+cc+'BP00')].copy()
    gas_df=gas_df[(gas_df['t'].str[:2]==cc)&(gas_df['t'].str[2:4]=='NG')&(gas_df['t'].str[6:7]!='P')].copy()
    gas_df= gas_df[(gas_df['t'].str[6:10]=='ELGX')|(gas_df['t'].str[6:10]=='ILGX')|(gas_df['t'].str[6:10]=='X00X')].copy()
    #gas_df = df_filter_gas(gas_df,2,10,gas_df_export1,gas_df_import1)
    gas_df['t'] = gas_df['t'].str[2:10]
    gas_df['value'] = gas_df['value'].astype('float64')
    gas_df['t'] = gas_df['t'].astype(str)
    gas_df=pd.concat([gas_df,gas_df_export1,gas_df_import1])
    gas_df = gas_df.pivot_table(index='y',columns='t',
                                      values='value', 
                                      aggfunc='sum').reset_index().fillna(0)
    gas_df = gas_df.reindex(sorted(gas_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #gas_df['y'] = years
    #gas_df=gas_df[gas_df['y']>2018]
    for each in gas_df.columns:
        if each=='Natural gas exports (Liquification terminal)':
            gas_df[each] =gas_df[each].astype(float)*-1
        else:
            pass
    if len(gas_df.columns)==1:
            print('There are no values for the result variable that you want to plot')
    else:
        gas_df.iplot(x='y',
                 kind='bar', 
                 barmode='relative',
                 xTitle='Year',
                 yTitle="Petajoules (PJ)",
                 color=[color_dict[x] for x in gas_df.columns if x != 'y'],
                 title=cc+"-"+"Gas extraction, imports and exports")