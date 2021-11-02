import pandas as pd
import datetime
from datetime import datetime
from scipy.stats import beta
import scipy as sc
import matplotlib.pyplot as plt
import numpy as np
from bokeh.models import ColumnDataSource, Whisker
from bokeh.plotting import figure
from bokeh.io import output_file, show
import math
from math import pi

from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum


import glob
import os

def important_variant_finder():
    USA_variants, y, file_name = define_datasets("B.1.617.2", False)
    var = USA_variants["date"]

    yday_list = []
    for i in range (0, len(var)):
        date_str = var.iloc[i]
        if len(date_str) == 10:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            yday=date_obj.timetuple().tm_yday
            if date_obj.timetuple().tm_year == 2020:
                yday = yday - 366
            yday_list.append(yday)
        else:
            yday_list.append(-1)
            


    variant_counter = {}

    variant_list = list(USA_variants["pango_lineage"])
    max_epiweek = max_epiweek_finder(file_name)
    for i in range (0, len(USA_variants["pango_lineage"])):
        if yday_list[i]>=(7*(max_epiweek-1))-4 and yday_list[i] < (7*max_epiweek-4):


            if variant_list[i] in list(variant_counter.keys()):
                variant_counter[variant_list[i]] += 1
            else:
                variant_counter[variant_list[i]] = 1
            
    return({k: v for k, v in sorted(variant_counter.items(), key=lambda item: item[1])})


def define_datasets(variant_name, B117_denom = False):
    #REMEMBER TO ADD B117_denom IN OTHER CALLS

    # df = "metadata_updates/metadata_2021-04-30_13-06.tsv"
    list_of_files = glob.glob('metadata_updates/*') # * means all if need specific format then *.csv
    file_name = max(list_of_files, key=os.path.getctime)

    os_time = os.path.getctime(file_name)
    ymd = datetime.fromtimestamp(os_time).strftime('%Y-%m-%d')

    new_file_name = "metadata_updates/metadata_" + ymd + '.tsv'
    if file_name != new_file_name:
        os.rename(file_name, new_file_name)


    dataset = pd.read_csv(new_file_name, sep="\t") 



    USA = dataset["country"].str.contains("USA")
    USA_total_variants = dataset[USA]

    USA_variant_name = USA_total_variants["pango_lineage"] == variant_name
    USA_variant = USA_total_variants[USA_variant_name]

    if B117_denom:
        USA_B117_variant = USA_total_variants["pango_lineage"] == "B.1.617.2"
        USA_B117_and_variant = USA_B117_variant | USA_variant_name
        USA_B117 = USA_total_variants[USA_B117_and_variant]
        return(USA_B117, USA_variant, new_file_name)
        #first 2 things returned should be datatables
    else:
        return(USA_total_variants, USA_variant, new_file_name)





def max_epiweek_finder(file_name):
    os_time = os.path.getctime(file_name)
    ymd = datetime.fromtimestamp(os_time).strftime('%Y-%m-%d')

    
    date_obj = datetime.strptime(ymd, '%Y-%m-%d')
    yday=date_obj.timetuple().tm_yday
    weeks = (yday-2)/7
    weeks = math.ceil(weeks) - 3
    return(weeks)




def cases_per_week_function(variant_type, file_name):
    var = variant_type["date"]

    yday_list = []
    for i in range (0, len(var)):
        date_str = var.iloc[i]  
        if len(date_str) == 10:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            yday=date_obj.timetuple().tm_yday
            if date_obj.timetuple().tm_year == 2020:
                yday = yday - 366
            yday_list.append(yday)

    max_epiweek = max_epiweek_finder(file_name)
    
    d = [0 for i in range (0, max_epiweek+2)]
    for i in range (-1, max_epiweek+1):
        day_counter = 0
        for j in range (0, len(yday_list)):
            if yday_list[j]>=(7*(i-1))-4 and yday_list[j] < (7*i-4):
                day_counter += 1
                d[i+1] = day_counter
                
    week_counter = [str(i) for i in range (-1, max_epiweek+1)]

    cases_per_week = pd.Series(data=d, index=week_counter)
    return(cases_per_week)


def logit_scale(percent_input):
    p = percent_input/100
    logit_num = np.log(p/(1-p))
    return(logit_num)


def lin_reg_slope(x_list,y_list):
    mean_x = np.mean(x_list)
    mean_y = np.mean(y_list)

    shifted_x = x_list-mean_x
    shifted_y = y_list-mean_y
    z = np.mean((shifted_x)*(shifted_y))
    s = np.mean((shifted_x)**2)
    m = z/s
    return(m, shifted_x)

def local_reg(x_list, y_list, window):
    m_list = []
    midpoint_list = []
    short_window_list = []
    midpoint_x = []
    for i in range (0, len(x_list)-window+1):
        s_w = [x_list[i], x_list[i+window-1]]
        short_window_list.append(s_w)
        x = x_list[i:i+window]
        y = y_list[i:i+window]
        m, shifted_x = lin_reg_slope(x,y)
        m_list.append(m)
        mean_y = np.mean(y)
        lin_reg_y = m*(shifted_x) + mean_y
        if window %2 == 0:
            midpoint = (lin_reg_y[int(window/2-1)]+lin_reg_y[int((window/2))])/2
            midpoint_list.append(midpoint)
        else:
            midpoint = lin_reg_y[int((window+1)/2)-1]
            midpoint_list.append(midpoint)
        mdx = int((s_w[0]+s_w[1])/2)
        midpoint_x.append(mdx)
    return(short_window_list, m_list, midpoint_list, midpoint_x)


# *******************************************************************************************************************************

def set_up_variables(variant_name, denom):
    # DEFINE VARIANT NAME HERE 
    
    # variant_name = "B.1.617.2"
    # variant_name = "P.1"
    # if variant_name == "B.1.1.7":
    #     denom = False
    # else:
    #     denom = True
    USA_variants, USA_B117_variants, file_name = define_datasets(variant_name, B117_denom = denom)

    B117_per_week = cases_per_week_function(USA_B117_variants, file_name)
    USA_per_week = cases_per_week_function(USA_variants, file_name)
    B117_over_total_USA = B117_per_week*100/USA_per_week
    start_index = 0 
    for i in range (0, len(B117_over_total_USA)):
        if B117_over_total_USA[len(B117_over_total_USA)-i-1] < np.exp(-8.5) or B117_per_week[len(B117_over_total_USA)-i-1] < 10:
            start_index = len(B117_over_total_USA) - i
            break;

    B117_over_total_USA = B117_over_total_USA[start_index:len(B117_over_total_USA)]
    B117_per_week = B117_per_week[start_index:len(B117_per_week)]
    USA_per_week = USA_per_week[start_index:len(USA_per_week)]

    for i in range (0, len(B117_over_total_USA)):
        B117_over_total_USA[i] = B117_over_total_USA[i] + 10**-8



    k_list = cases_per_week_function(USA_B117_variants, file_name)
    n_list = cases_per_week_function(USA_variants, file_name)

    k_list = k_list[start_index:len(k_list)]
    n_list = n_list[start_index:len(n_list)]
    return(k_list, n_list, file_name, start_index, B117_over_total_USA, B117_per_week, USA_per_week)


def get_upper_lower_bounds(k_list, n_list, file_name, start_index):
    lower_bounds = []
    upper_bounds = []
    max_epiweek = max_epiweek_finder(file_name)


    for i in range (0, max_epiweek +2-start_index):
        k = k_list[i]
        n = n_list[i]
    #     print("lower bound: " + str(sc.beta.ppf(.025, k+1, n-k+1)))
    #     print("upper bound: " + str(sc.beta.ppf(.975, k+1, n-k+1)))
        l = beta.ppf(.025, k+1, n-k+1) * 100
        u = beta.ppf(.975, k+1, n-k+1) * 100
        lower_bounds.append(l)
        upper_bounds.append(u)
    # print(lower_bounds)
    return (lower_bounds, upper_bounds, max_epiweek)


def logit_function(max_epiweek, start_index, B117_over_total_USA, k_list):

    y_logistic_scale = []

    len(B117_over_total_USA.tolist())
    for i in range (0, max_epiweek+2-start_index):
        y = logit_scale(B117_over_total_USA.tolist()[i])
        y_logistic_scale.append(y)

    x_list = [int(k_list.index[x]) for x in range(len(k_list.index.tolist()))]
    y_list = y_logistic_scale


    m, shifted_x = lin_reg_slope(x_list,y_list)
    mean_x = np.mean(x_list)
    mean_y = np.mean(y_list)

    lin_reg_y = m*(shifted_x) + mean_y
    doubling_time = np.log(2)/m
    doubling_time * 7


    lin_x = np.linspace(-1,max_epiweek+1,1000)
    lin_y = m*(lin_x-mean_x) + mean_y
    return(lin_x, lin_y, x_list, y_list, y_logistic_scale, lin_reg_y)


def logit_bounds(lower_bounds, upper_bounds):
    logit_upper_bounds = []
    for i in range (0, len(upper_bounds)):
        l = logit_scale(upper_bounds[i])
        logit_upper_bounds.append(l)

    logit_lower_bounds = []
    for i in range (0, len(lower_bounds)):
        l = logit_scale(lower_bounds[i])
        logit_lower_bounds.append(l)
    return(logit_lower_bounds, logit_upper_bounds)



def last_variables(lin_y, k_list, x_list, y_list):
    log_reg_y = (np.exp(lin_y)*100)/(1+np.exp(lin_y))
    k_list_int = [int(i) for i in k_list.index.tolist()]

    window=5
    short_window_list, m_list, midpoint_list, midpoint_x = local_reg(x_list, y_list, window)
    incubation_m_list = np.exp((5/7)*(np.array(m_list)))
    incubation_m_list = incubation_m_list[1:len(incubation_m_list)]
    midpoint_list = midpoint_list[1:len(midpoint_list)]
    midpoint_x = midpoint_x[1:len(midpoint_x)]
    return(midpoint_x, midpoint_list, incubation_m_list, log_reg_y, k_list_int)

def pie_chart_variables():
    cases_by_variant_dict = important_variant_finder()
    values = cases_by_variant_dict.values()
    total_cases = sum(values)
    top_cases_by_variant = {}
    for i in range (0, len(cases_by_variant_dict)):
        if list(cases_by_variant_dict.values())[i] >= total_cases/100:
          top_cases_by_variant[list(cases_by_variant_dict.keys())[i]] = list(cases_by_variant_dict.values())[i]
    sum_top = sum(top_cases_by_variant.values())
    top_cases_by_variant["Other"] = total_cases - sum_top
    return(top_cases_by_variant, total_cases)

def pie_chart(top_cases_by_variant, total_cases):

    output_file("../_includes/" + "US_variant_percentages.html")



    data = pd.Series(top_cases_by_variant).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(top_cases_by_variant)]

    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='country', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    show(p)

def total_cases(k_list, B117_per_week, USA_per_week, variant_name): 
    source = ColumnDataSource(data=dict(groups=k_list.index.tolist(), counts=B117_per_week))
    source_1 = ColumnDataSource(data=dict(groups=k_list.index.tolist(), counts=USA_per_week))

    p = figure(x_range=k_list.index.tolist(), plot_height=350, title= variant_name + " vs Total U.S. COVID-19 Cases per Week", y_range=(0,max(USA_per_week)*1.025))
    p.line(x='groups', y='counts', line_width=2, color = 'red', source=source, legend_label = variant_name)
    p.line(x='groups', y='counts', line_width=2, source=source_1, color = 'blue', legend_label = "Total Cases")


    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Number of Cases'

    p.legend.location = "top_left"

    # output_file("_includes/B117_vs_Total_per_week.html")

    output_file("../_includes/" + variant_name + "_vs_Total_per_week.html")
    show(p)


def percentage_cases(k_list_int, lower_bounds, upper_bounds, B117_over_total_USA, lin_x, log_reg_y, variant_name):
    source = ColumnDataSource(data=dict(groups=k_list_int, upper=upper_bounds, lower=lower_bounds, counts=B117_over_total_USA.tolist()))
    source_1 = ColumnDataSource(data=dict(second_x=lin_x, second_y = log_reg_y))

    p = figure(plot_height=350, title="Prevalence of " + variant_name + " over Time in the U.S.", y_range=(0,max(max(log_reg_y), max(upper_bounds))*1.025))
    p.circle(x='groups', y='counts', size=3, color = 'black', source = source, legend_label = "Observed Data")
    p.line(x='second_x', y='second_y', line_width=2, source=source_1, legend_label = "Estimated Logistic Model")


    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Percentage of ' + variant_name + ' out of COVID Cases'

    p.add_layout(
        Whisker(source=source, base="groups", upper="upper", lower="lower", level="overlay")
    )
    p.legend.location = "top_left"
    # bokeh add axis labels and title y axis is percentage of cases that are B.1.1.7

    # output_file("_includes/epiweek_US.html")
    output_file("../_includes/" + variant_name + "epiweek_US.html")

    show(p)


def logit_graph(k_list_int, logit_lower_bounds, logit_upper_bounds, y_logistic_scale, lin_reg_y, midpoint_x, midpoint_list, variant_name):
    source = ColumnDataSource(data=dict(groups=k_list_int, upper=logit_upper_bounds, lower=logit_lower_bounds, counts=y_logistic_scale, lin_reg = lin_reg_y))
    source_1 = ColumnDataSource(data=dict(groups=midpoint_x,counts1=midpoint_list))

    p = figure(plot_height=350, title="Linear and Local Regression Models for the Prevalence of " + variant_name, y_range=(np.min(logit_lower_bounds)-0.5,np.max(lin_reg_y)+0.5))

    p.line(x='groups', y='lin_reg', line_width=2, source=source, legend_label = "Estimated Linear Model")
    p.line(x='groups', y='counts1', line_width=2, color = 'red', source=source_1, legend_label = 'Local Regression')
    p.circle(x='groups', y='counts', size=3, color = 'black', source = source, legend_label = "Observed Data")

    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Log Odds Ratio of the Prevalence of '+ variant_name + ' Cases'
    p.add_layout(
        Whisker(source=source, base="groups", upper="upper", lower="lower", level="overlay")
    ) 

    p.legend.location = "bottom_right"

    # output_file("_includes/epiweek_US_logit_local.html")
    output_file("../_includes/" + variant_name+ "epiweek_US_logit_local.html")

    show(p)


def transmissibility_graph(midpoint_x, incubation_m_list, variant_name):
    source = ColumnDataSource(data=dict(groups=midpoint_x, counts=incubation_m_list))
    # p = figure(plot_height=350, title = 'Local Regression Slope over Time', y_range=(np.min(incubation_m_list)-1,np.max(incubation_m_list)+1))
    p = figure(plot_height=350, title = 'Transmissibility Ratio Over Time of ' + variant_name, y_range=(min(incubation_m_list) - 1, max(incubation_m_list)+1))
    p.line(x='groups', y = 'counts', line_width = 2, source = source)

    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Transmissibility Ratio'
    # output_file("_includes/transmissibility_ratio.html")
    output_file("../_includes/" + variant_name + "transmissibility_ratio.html")

    show(p)