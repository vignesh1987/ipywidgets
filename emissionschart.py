def emissions_chart(Country):
    cc=country_code[country_code['Country Name']==Country]['Country code'].tolist()[0]
    #CO2-Emission detailed
    co2_df = all_params['AnnualTechnologyEmission']
    co2_df=co2_df[co2_df['e'].str[:6]==cc+'CO2'].copy()

    co2_df['value'] = co2_df['value'].astype('float64')
    co2_df = co2_df.pivot_table(index='y',columns='t',
                            values='value',
                            aggfunc='sum').reset_index().fillna(0)
    for each in co2_df.columns:
        if len(each)!=1:
            if (each[2:4]=='NG') & (each[6:10]=='BP00'):
                pass
            else:
                co2_df.rename(columns={each:each[2:10]},inplace=True)
        else:
            pass
    co2_df = co2_df.reindex(sorted(co2_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    #co2_df['y'] = years
    #co2_df=co2_df[co2_df['y']>2018]
    df_plot(co2_df,'Million Tonnes (Mt)',cc+'-''Emissions (CO2)-by technology')
