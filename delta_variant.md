---
layout: page
title: "Delta Variant"
permalink: /delta/
feature_image: "/images/covid.jpg"

---



### Tracking the B.1.617.2 (Delta) Variant in the U.S.

The Delta variant (B.1.617.2) has emerged as one of the most contagious and deadly new variants. Not only is it more transmissible, it is slightly more resistant to [vaccines](https://www.nature.com/articles/d41586-021-01696-3), and its rise as the new, main variant of concern is said to be ["inevitable,"](https://www.nature.com/articles/d41586-021-01696-3)  despite the best efforts to contain it. With the B.1.1.7 (Alpha) variant slowly plateauing, the Delta variant will take its place. The World Health Organization (W.H.O.) urges people to keep their masks on due to this [variant](https://www.nytimes.com/2021/06/29/world/who-mask-guidelines.html). 

The COVID sequencing data is obtained from the EpiCoV database at [GISAID](https://www.gisaid.org), and it should be noted that it does not contain all known data from the U.S. By using the PCR method to test for COVID, it only detects if COVID is present, not which variant, so our data does not include all COVID cases, but should taken as a subsample of all the data to represent the overall trends. All graphs (except the first) compare the Delta variant to Alpha instead of the total COVID cases because the total cases are a heterogeneous population of variants, but we want to make a fixed comparison.

{% include B.1.617.2_vs_Total_per_week.html %} 

In the graph above. the blue represents the total COVID cases sequenced in the dataset, while the red shows the number of cases of the Delta variant sequenced. Currently, the Delta variant is slowly increasing, but due to its increased transmissibility, it is expected to overtake Alpha as the dominant strain.

{% include B.1.617.2epiweek_US.html %} 

The x-axis represents the time in terms of weeks, and the y-axis is the percentage of Delta cases out of the total number of cases between the Delta and Alpha variants in the U.S. with a 95% credible interval. The graph is currently exponentially increasing, the beginning stages of a logistic curve. As the number of cases decreases due to incomplete data, the error bars will reflect this change and increase in length. 

{% include B.1.617.2epiweek_US_logit_local.html %}

This graph shows the log odds ratio of the prevalence of the Delta variant cases relative to Alpha in the U.S. over time. The dots represent the observed average prevalence (number of Delta cases divided by the total cases between the Delta and Alpha variants) with a 95% credible interval. The linear regression model (shown in blue) demonstrates an upward trend. The local regression model (shown in red) has a similar trend, but subtle shifts in the slope of the line are present.

{% include B.1.617.2transmissibility_ratio.html %}

The graph above shows the transmissibility ratio over time, with the x-axis representing time and the y-axis the transmissibility ratio. The transmissibility ratio is the transmissibility rate (how many people one person can infect on average) of the Delta variant over the rate for the Delta and Alpha variants combined. By representing the information as a ratio, we can see the relative fitness of the Delta variant compared to Alpha. The initial variation is most likely due to noise and likely does not imply a meaningful trend. This shows that the Delta variant is 30-50% more transmissible than the Alpha variant, consitent with other [studies](https://www.nature.com/articles/d41586-021-01696-3).

