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
import glob
import os


def define_datasets():
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
    USA_variants = dataset[USA]

    USA_B117 = USA_variants["pango_lineage"] == "B.1.1.7"
    USA_B117_variants = USA_variants[USA_B117]
    return(USA_variants, USA_B117_variants, new_file_name)



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

def create_graphs():
    USA_variants, USA_B117_variants, file_name = define_datasets()

    B117_per_week = cases_per_week_function(USA_B117_variants, file_name)
    USA_per_week = cases_per_week_function(USA_variants, file_name)

    B117_over_total_USA = B117_per_week*100/USA_per_week
    k_list = cases_per_week_function(USA_B117_variants, file_name)
    n_list = cases_per_week_function(USA_variants, file_name)

    lower_bounds = []
    upper_bounds = []
    max_epiweek = max_epiweek_finder(file_name)


    for i in range (0, max_epiweek +2):
        k = k_list[i]
        n = n_list[i]
    #     print("lower bound: " + str(sc.beta.ppf(.025, k+1, n-k+1)))
    #     print("upper bound: " + str(sc.beta.ppf(.975, k+1, n-k+1)))
        l = beta.ppf(.025, k+1, n-k+1) * 100
        u = beta.ppf(.975, k+1, n-k+1) * 100
        lower_bounds.append(l)
        upper_bounds.append(u)
    # print(lower_bounds)




    y_logistic_scale = []

    len(B117_over_total_USA.tolist())
    for i in range (0, max_epiweek+2):
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



    logit_upper_bounds = []
    for i in range (0, len(upper_bounds)):
        l = logit_scale(upper_bounds[i])
        logit_upper_bounds.append(l)

    logit_lower_bounds = []
    for i in range (0, len(lower_bounds)):
        l = logit_scale(lower_bounds[i])
        logit_lower_bounds.append(l)




    log_reg_y = (np.exp(lin_y)*100)/(1+np.exp(lin_y))
    k_list_int = [int(i) for i in k_list.index.tolist()]

    window=5
    short_window_list, m_list, midpoint_list, midpoint_x = local_reg(x_list, y_list, window)
    incubation_m_list = np.exp((5/7)*(np.array(m_list)))
    incubation_m_list = incubation_m_list[1:len(incubation_m_list)]
    midpoint_list = midpoint_list[1:len(midpoint_list)]
    midpoint_x = midpoint_x[1:len(midpoint_x)]


    source = ColumnDataSource(data=dict(groups=k_list.index.tolist(), counts=B117_per_week))
    source_1 = ColumnDataSource(data=dict(groups=k_list.index.tolist(), counts=USA_per_week))

    p = figure(x_range=k_list.index.tolist(), plot_height=350, title="B.1.1.7 vs Total U.S. COVID-19 Cases per Week", y_range=(0,max(USA_per_week)*1.025))
    p.line(x='groups', y='counts', line_width=2, color = 'red', source=source, legend_label = "B.1.1.7")
    p.line(x='groups', y='counts', line_width=2, source=source_1, color = 'blue', legend_label = "Total Cases")


    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Number of Cases'

    p.legend.location = "top_left"

    output_file("_includes/B117_vs_Total_per_week.html")

    show(p)



    source = ColumnDataSource(data=dict(groups=k_list_int, upper=upper_bounds, lower=lower_bounds, counts=B117_over_total_USA.tolist()))
    source_1 = ColumnDataSource(data=dict(second_x=lin_x, second_y = log_reg_y))

    p = figure(plot_height=350, title="Prevalence of B.1.1.7 over Time in the U.S.", y_range=(0,max(max(log_reg_y), max(upper_bounds))*1.025))
    p.circle(x='groups', y='counts', size=3, color = 'black', source = source, legend_label = "Observed Data")
    p.line(x='second_x', y='second_y', line_width=2, source=source_1, legend_label = "Estimated Logistic Model")


    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Percentage of B.1.1.7 out of COVID Cases'

    p.add_layout(
        Whisker(source=source, base="groups", upper="upper", lower="lower", level="overlay")
    )
    p.legend.location = "bottom_right"
    # bokeh add axis labels and title y axis is percentage of cases that are B.1.1.7

    output_file("_includes/epiweek_US.html")

    show(p)


    source = ColumnDataSource(data=dict(groups=k_list_int, upper=logit_upper_bounds, lower=logit_lower_bounds, counts=y_logistic_scale, lin_reg = lin_reg_y))
    source_1 = ColumnDataSource(data=dict(groups=midpoint_x,counts1=midpoint_list))

    p = figure(plot_height=350, title="Linear and Local Regression Models for the Prevalence of B.1.1.7", y_range=(np.min(logit_lower_bounds)-0.5,np.max(lin_reg_y)+0.5))

    p.line(x='groups', y='lin_reg', line_width=2, source=source, legend_label = "Estimated Linear Model")
    p.line(x='groups', y='counts1', line_width=2, color = 'red', source=source_1, legend_label = 'Local Regression')
    p.circle(x='groups', y='counts', size=3, color = 'black', source = source, legend_label = "Observed Data")

    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Log Odds Ratio of the Prevalence of B.1.1.7 Cases'
    p.add_layout(
        Whisker(source=source, base="groups", upper="upper", lower="lower", level="overlay")
    ) 

    p.legend.location = "bottom_right"

    output_file("_includes/epiweek_US_logit_local.html")

    show(p)



    source = ColumnDataSource(data=dict(groups=midpoint_x, counts=incubation_m_list))
    # p = figure(plot_height=350, title = 'Local Regression Slope over Time', y_range=(np.min(incubation_m_list)-1,np.max(incubation_m_list)+1))
    p = figure(plot_height=350, title = 'Transmissibility Ratio Over Time', y_range=(0.75,1.75))
    p.line(x='groups', y = 'counts', line_width = 2, source = source)

    p.xaxis.axis_label = 'Epiweek'
    p.yaxis.axis_label = 'Transmissibility Ratio'
    output_file("_includes/transmissibility_ratio.html")

    show(p)