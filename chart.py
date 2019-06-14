from plot import df_plot
import pandas as pd
from functools import lru_cache

def get_colour_code():

    colorcode = pd.read_csv('./techcodes.csv', sep=',')
    colorcode1 = colorcode.drop('colour', axis=1)
    return dict([(a,b) for a,b in zip(colorcode1.tech_code, colorcode1.tech_name)])

@lru_cache(maxsize=64)
def get_country_code(Country):

    country_code = pd.read_csv('./countrycode.csv', sep=',')
    return country_code[country_code['Country Name'] == Country]['Country code'].tolist()[0]    

def water_chart(Country, all_params, t_include):
    """Plots water abstraction results
    """
    cc = get_country_code(Country)
    det_col = get_colour_code()
    agg_col = pd.read_csv('./agg_col.csv', sep=',').to_dict('list')

    # water withdrawal detailed
    wat_w_df = all_params['UseByTechnologyAnnual']
    wat_w_df = wat_w_df[wat_w_df['f'].str[:6] == cc + 'WAT1'].copy()

    wat_w_df['t'] = wat_w_df['t'].str[2:10]
    wat_w_df['value'] = wat_w_df['value'].astype('float64')
    wat_w_df = wat_w_df.pivot_table(index='y', 
                                    columns='t',
                                    values='value', 
                                    aggfunc='sum').reset_index().fillna(0)
    wat_w_df = wat_w_df.reindex(sorted(wat_w_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    # Water Withdrawal (Aggregated)
    watw_agg_df = pd.DataFrame(columns=agg_col)
    watw_agg_df.insert(0,'y',wat_w_df['y'])
    watw_agg_df = watw_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_w_df.columns:
                watw_agg_df[each] = watw_agg_df[each] + wat_w_df[tech_exists]
                watw_agg_df[each] = watw_agg_df[each].round(2)

    df_plot(watw_agg_df, 'Million cubic metres (Mm^3)', cc + "-" + 'Water Withdrawal')

    # water output detailed
    wat_o_df = all_params['ProductionByTechnologyAnnual']
    wat_o_df = wat_o_df[wat_o_df['f'].str[:6]==cc+'WAT2'].copy()
    wat_o_df['t'] = wat_o_df['t'].str[2:10].copy()
    wat_o_df['value'] = wat_o_df['value'].astype('float64')
    wat_o_df = wat_o_df.pivot_table(index='y', 
                                    columns='t',
                                    values='value', 
                                    aggfunc='sum').reset_index().fillna(0)
    wat_o_df = wat_o_df.reindex(sorted(wat_o_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)

    #Water consumption missing row additions
    for wd in wat_w_df.columns:
        for wc in wat_o_df.columns:
            if wd in wat_o_df.columns:
                pass
            else:
                wat_o_df[wd] = 0
    #####
    ####Water consumption (Detailed)
    wat_c_df = wat_w_df.set_index('y') - wat_o_df.set_index('y')
    wat_c_df = wat_c_df.fillna(0.00)
    wat_c_df.reset_index(inplace=True)
    # Water consumption (Aggregate)
    watc_agg_df = pd.DataFrame(columns=agg_col)
    watc_agg_df.insert(0,'y',wat_c_df['y'])
    watc_agg_df  = watc_agg_df.fillna(0.00)
    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in wat_c_df.columns:
                watc_agg_df[each] = watc_agg_df[each] + wat_c_df[tech_exists]
                watc_agg_df[each] = watc_agg_df[each].round(2)
    df_plot(watc_agg_df, 'Million cubic metres (Mm^3)',cc+'-'+'Water consumption aggregated')


def power_chart(Country, all_params, agg_pow_col, t_include):

    cc = get_country_code(Country)
    det_col = get_colour_code()
    
    # colorcode = pd.read_csv('./techcodes.csv', sep=',')
    # colorcode2 = colorcode.drop('tech_code', axis=1)
    # color_dict = dict([(a,b) for a,b in zip(colorcode2.tech_name, colorcode2.colour)])

    # Power capacity (detailed)
    cap_df = all_params['TotalCapacityAnnual']
    cap_df = cap_df[cap_df['t'].str[:2]==cc].copy()
    cap_df['t'] = cap_df['t'].str[2:10]
    cap_df['value'] = cap_df['value'].astype('float64')
    cap_df = cap_df[cap_df['t'].isin(t_include)].pivot_table(index='y',
                                               columns='t',
                                               values='value',
                                               aggfunc='sum').reset_index().fillna(0)
    cap_df = cap_df.reindex(sorted(cap_df.columns), axis=1
        ).set_index('y'
        ).reset_index(
        ).rename(columns=det_col)
    #***********************************************
    # Power capacity (Aggregated)
    cap_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_agg_df.insert(0,'y',cap_df['y'])
    cap_agg_df = cap_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_df.columns:
                cap_agg_df[each] = cap_agg_df[each] + cap_df[tech_exists]
                cap_agg_df[each] = cap_agg_df[each].round(3)
    #
    df_plot(cap_agg_df, 'Gigawatts (GW)', 
            cc + "-" + 'Power Generation Capacity (Aggregate)')
    ## Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'].copy()
    gen_df = gen_df[(gen_df['f'].str[:2] == cc)].copy()
    gen_df = gen_df[(gen_df['f'].str[2:6] == 'EL01') | (gen_df['f'].str[2:6] == 'EL03')].copy()
    gen_df = gen_df[(gen_df['t'].str[2:10] != 'EL00T00X') & (gen_df['t'].str[2:10] != 'EL00TDTX')].copy()
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
    gen_df = gen_df.reindex(sorted(gen_df.columns), axis=1
                            ).set_index('y'
                            ).reset_index(
                            ).rename(columns=det_col)
    #####
    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_pow_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df = gen_agg_df.fillna(0.00)
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
    df_plot(gen_agg_df, 'Petajoules (PJ)', cc+"-"+'Power Generation (Aggregate)')
    # New capacity (detailed)
    cap_new_df = all_params['NewCapacity']
    cap_new_df = cap_new_df[cap_new_df['t'].str[:2]==cc].copy()
    cap_new_df['t'] = cap_new_df['t'].str[2:10]
    cap_new_df['value'] = cap_new_df['value'].astype('float64')
    cap_new_df = cap_new_df[cap_new_df['t'].isin(t_include)].pivot_table(
        index='y', columns='t', values='value', aggfunc='sum'
        ).reset_index().fillna(0)
    cap_new_df = cap_new_df.reindex(sorted(cap_new_df.columns), axis=1
        ).set_index('y'
        ).reset_index(
            
        ).rename(columns=det_col)
    #***********************************************
    # Power capacity (Aggregated)
    cap_new_agg_df = pd.DataFrame(columns=agg_pow_col)
    cap_new_agg_df.insert(0, 'y', cap_new_df['y'])
    cap_new_agg_df  = cap_new_agg_df.fillna(0.00)
    #
    for each in agg_pow_col:
        for tech_exists in agg_pow_col[each]:
            if tech_exists in cap_new_df.columns:
                cap_new_agg_df[each] = cap_new_agg_df[each] + cap_new_df[tech_exists]
                cap_new_agg_df[each] = cap_new_agg_df[each].round(3)
                ##
    df_plot(cap_new_agg_df, 'Gigawatts (GW)', 
            cc + "-" + 'New power generation capacity (Aggregate)')
