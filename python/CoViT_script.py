from CoViT import *
from important_variant_finder import *
from bokeh.plotting import figure, output_file
from bokeh.io import output_file, show
import matplotlib.pyplot as plt

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
    labels = list(top_cases_by_variant.keys())
    sizes = np.array(list(top_cases_by_variant.values()))/total_cases
    fig1, ax1 = plt.subplots()
    colors = ("red", "orange", "yellow", 
              "lime", "royalblue", "cyan", "violet") 
    ax1.pie(sizes, labels=labels, colors = colors, autopct='%1.1f%%',
            shadow=True, startangle=0, radius=5000)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig1.set_size_inches(7,7)
    # output_file("../includes/US_variant_percentages.html")
    plt.savefig('../includes/US_variant_percentages.png')


def pie():
	top_cases_by_variant, total_cases = pie_chart_variables()
	pie_chart(top_cases_by_variant, total_cases)

def all_functions(variant_name, denom):
	k_list, n_list, file_name, start_index, B117_over_total_USA, B117_per_week, USA_per_week = set_up_variables(variant_name, denom)

	lower_bounds, upper_bounds, max_epiweek = get_upper_lower_bounds(k_list, n_list, file_name, start_index)
		
	lin_x, lin_y, x_list, y_list, y_logistic_scale, lin_reg_y = logit_function(max_epiweek, start_index, B117_over_total_USA, k_list)

	logit_lower_bounds, logit_upper_bounds = logit_bounds(lower_bounds, upper_bounds)

	midpoint_x, midpoint_list, incubation_m_list, log_reg_y, k_list_int = last_variables(lin_y, k_list, x_list, y_list)

	if not denom:
		total_cases(k_list, B117_per_week, USA_per_week, variant_name)

	if variant_name == "B.1.1.7" or denom:
		percentage_cases(k_list_int, lower_bounds, upper_bounds, B117_over_total_USA, lin_x, log_reg_y, variant_name)

		logit_graph(k_list_int, logit_lower_bounds, logit_upper_bounds, y_logistic_scale, lin_reg_y, midpoint_x, midpoint_list, variant_name)

		transmissibility_graph(midpoint_x, incubation_m_list, variant_name)

 	
pie()

# all_functions("B.1.1.7", False)

# all_functions("P.1", False)
# all_functions("P.1", True)

# all_functions("B.1.617.2", False)
# all_functions("B.1.617.2", True)
