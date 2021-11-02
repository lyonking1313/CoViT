---
layout: page
title: "AY.25 Variant"
permalink: /AY.25/
feature_image: "/images/covid.jpg"

---



### Tracking the AY.25 Variant in the U.S.

The AY.25 variant is a subtype of the Delta variant, B.1.617.2.

The COVID sequencing data is obtained from the EpiCoV database at [GISAID](https://www.gisaid.org), and it should be noted that it does not contain all known data from the U.S. By using the PCR method to test for COVID, it only detects if COVID is present, not which variant, so our data does not include all COVID cases, but should taken as a subsample of all the data to represent the overall trends. All graphs (except the first) compare the AY.25 variant to Delta instead of the total COVID cases because the total cases are a heterogeneous population of variants, but we want to make a fixed comparison.

{% include AY.25_vs_Total_per_week.html %}

The blue line represents the total number of COVID-19 cases, while the red line shows the number of AY.25 cases per week. 

Next, we divided the number of AY.25 cases by the number of total COVID-19 cases in the U.S. to calculate the overall prevalence of this variant in the U.S. over time. It is important to know the ratio as opposed to just the raw number of cases of the AY.25 variant to understand the relative rate of growth of the AY.25 variant. Assuming that each case is randomly sampled, we are able to estimate the AY.25 prevalence for the entire population. 

{% include AY.25epiweek_US.html %} 

The x-axis represents the time in terms of weeks, and the y-axis is the percentage of AY.25 cases out of the total number of cases between the AY.25 and Delta variants in the U.S. with a 95% credible interval (see methods section for details). The graph is currently exponentially increasing, the beginning stages of a logistic curve. As the number of cases decreases due to incomplete data, the error bars will reflect this change and increase in length. 

{% include AY.25epiweek_US_logit_local.html %}

This graph shows the log odds ratio of the prevalence of the AY.25 variant cases relative to Delta in the U.S. over time. The dots represent the observed average prevalence (number of AY.25 cases divided by the total cases between the AY.25 and Delta variants) with a 95% credible interval. The linear regression model (shown in blue) demonstrates an upward trend. The local regression model (shown in red) has a similar trend, but subtle shifts in the slope of the line are present.

{% include AY.25transmissibility_ratio.html %}

The graph above shows the transmissibility ratio over time, with the x-axis representing time and the y-axis the transmissibility ratio. The transmissibility ratio is the transmissibility rate (how many people one person can infect on average) of the AY.25 variant over the rate for the AY.25 and Delta variants combined. By representing the information as a ratio, we can see the relative fitness of the AY.25 variant compared to Delta. The initial variation is most likely due to noise and likely does not imply a meaningful trend. This shows that the AY.25 variant is approximately 5% more transmissible than the Delta variant.

