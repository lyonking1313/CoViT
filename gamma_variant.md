---
layout: page
title: "Gamma Variant"
permalink: /gamma/
feature_image: "/images/covid.jpg"

---



### Tracking the P.1 (Gamma) Variant in the U.S.

The P.1 variant, which originated in Brazil during the winter of 2020/21, became known as one of the most transmissible COVID-19 variants. In addition, it has been shown to have the potential immune escape mutation and be more resistant to [vaccinations](https://gvn.org/covid-19/gamma-p-1/). In several locations throughout Brazil, there have been outbreaks of this variant and has been labeled by the [CDC](https://www.cdc.gov/coronavirus/2019-ncov/variants/variant-info.html) as a variant of concern.

{% include P.1_vs_Total_per_week.html %}

The blue line represents the total number of COVID-19 cases, while the red line shows the number of P.1 cases per week. 

Next, we divided the number of P.1 cases by the number of total COVID-19 cases in the U.S. to calculate the overall prevalence of this variant in the U.S. over time. It is important to know the ratio as opposed to just the raw number of cases of the P.1 variant to understand the relative rate of growth of the P.1 variant. Assuming that each case is randomly sampled, we are able to estimate the P.1 prevalence for the entire population. 

{% include P.1epiweek_US.html %} 

The x-axis represents the time in terms of weeks, and the y-axis is the percentage of Gamma cases out of the total number of cases between the Gamma and Alpha variants in the U.S. with a 95% credible interval (see methods section for details). The graph is currently exponentially increasing, the beginning stages of a logistic curve. As the number of cases decreases due to incomplete data, the error bars will reflect this change and increase in length. 

{% include P.1epiweek_US_logit_local.html %}

This graph shows the log odds ratio of the prevalence of the Gamma variant cases relative to Alpha in the U.S. over time. The dots represent the observed average prevalence (number of Gamma cases divided by the total cases between the Gamma and Alpha variants) with a 95% credible interval. The linear regression model (shown in blue) demonstrates an upward trend. The local regression model (shown in red) has a similar trend, but subtle shifts in the slope of the line are present.

{% include P.1transmissibility_ratio.html %}

The graph above shows the transmissibility ratio over time, with the x-axis representing time and the y-axis the transmissibility ratio. The transmissibility ratio is the transmissibility rate (how many people one person can infect on average) of the Gamma variant over the rate for the Gamma and Alpha variants combined. By representing the information as a ratio, we can see the relative fitness of the Gamma variant compared to Alpha. The initial variation is most likely due to noise and likely does not imply a meaningful trend. This shows that the Gamma variant is approximately 10% more transmissible than the Alpha variant.

