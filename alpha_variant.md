---
layout: page
title: "Alpha Variant"
permalink: /alpha/
feature_image: "/images/covid.jpg"

---



### Tracking the B.1.1.7 (Alpha) Variant in the U.S.

Currently, the [B.1.1.7 variant](https://www.cdc.gov/coronavirus/2019-ncov/transmission/variant-cases.html) is the most prevalent in the U.S., making it a variant of concern. The variant emerged in late 2020 in the U.K. before traveling across the globe. It is known for its [increased transmissibility](https://www.cdc.gov/coronavirus/2019-ncov/science/science-briefs/scientific-brief-emerging-variants.html), which is why it is as of now, the most widespread variant in the U.S. The COVID sequencing data is obtained from the EpiCoV database at [GISAID](https://www.gisaid.org). This database allows us to quantify the number of B.1.1.7 cases in order to calculate this variant's trajectory over time. For each individual sample, the database used the RNA sequencing data to label the variants. More specifically, each variant of the COVID-19 virus has specific mutations, which can be used by an algorithm for classification. As a result, we were able to aggregate the B.1.1.7 and total cases per week.

{% include B.1.1.7_vs_Total_per_week.html %}

The blue line represents the total number of COVID-19 cases, while the red line shows the number of B.1.1.7 cases per week. The drop in the most recent weeks is caused by incomplete data, due to delays in reporting. 

Next, we divided the number of B.1.1.7 cases by the number of total COVID-19 cases in the U.S. to calculate the overall prevalence of this variant in the U.S. over time. It is important to know the ratio as opposed to just the raw number of cases of the B.1.1.7 variant to understand the relative rate of growth of the B.1.1.7 variant. Assuming that each case is randomly sampled, we are able to estimate the B.1.1.7 prevalence for the entire population. 

{% include B.1.1.7epiweek_US.html %} 

The x-axis represents the time in terms of weeks, and the y-axis is the percentage of B.1.1.7 cases out of the total number of COVID cases in the U.S. Each data point (in black) has error bars as a 95% credible interval. This interval shows the maximum and minimum possible points that is 95% likely to contain the true prevalence, computed using a beta prior and a binomial likelihood. As the number of cases decreases due to incomplete data, the error bars will reflect this change and increase in length. The curve (in blue) represents the initial section of the fitted logistic curve (determined by the linear regression model shown in the following figure) where it increases exponentially. It is interesting to note that despite vaccines being introduced in early 2021 with a steady increasing rate of vaccination, the graph is not affected. 

According to epidemiologic data, the COVID virus follows a [logistic trend](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7328553/). Since the data is logistic, it can then be transformed by a logit function (log odds ratio) to obtain a linear model. As a result, we took the log odds ratio of the number of B.1.1.7 cases at each week, and generated a line with the smallest difference in the estimated and observed data. 

Because the global linearity assumption could be false due to dynamic changes in the battle against COVID-19, we calculated the local regression. We tested a window of 5 weeks, in order to represent a more specific slope without sacrificing the overall trend of the model.

{% include B.1.1.7epiweek_US_logit_local.html %}

This graph shows the log odds ratio of the prevalence of B.1.1.7 cases in the U.S. over time. The dots represent the observed average prevalence (number of B.1.1.7 cases divided by the total number of COVID cases) with a 95% credible interval. The linear regression model (shown in blue) demonstrates an upward trend. The local regression model (shown in red) has a similar trend, but subtle shifts in the slope of the line are present.

According to the model, the B.1.1.7 variant is becoming more widespread in the U.S. The slope of the line is 0.38, which represents a 47% increase in the odds ratio every week. The estimated doubling time is approximately 13 days, consistent with [prior studies](https://www.medrxiv.org/content/10.1101/2021.02.06.21251159v1.full.pdf). 

In order to better interpret the slopes of the local regression model, we calculated the transmissibility ratios inferred from the slopes and graphed the results, using an incubation period of [5 days](https://www.cdc.gov/coronavirus/2019-ncov/hcp/clinical-guidance-management-patients.html). The transmissibility ratio is the transmissibility rate (how many people one person can infect on average) of B.1.1.7 over the rate for other existing COVID-19 variants. By representing the information as a ratio, we can see the relative fitness of the B.1.1.7 variant and detect the relative fitness of other variants.

{% include B.1.1.7transmissibility_ratio.html %}

The graph above shows the transmissibility ratio over time, with the x-axis representing time and the y-axis the transmissibility ratio. The initial variation is most likely due to noise and likely does not imply a meaningful trend. The gradual dip toward the end, however, represents that other variants are becoming more transmissible and relatively more fit. 



