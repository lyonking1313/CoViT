from CoViT import *

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


all_functions("B.1.1.7", False)

all_functions("P.1", False)
all_functions("P.1", True)

all_functions("B.1.617.2", False)
all_functions("B.1.617.2", True)
