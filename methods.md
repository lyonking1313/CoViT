---
layout: page
title: "Methods"
permalink: /methods/
feature_image: "/images/covid.jpg"
---



The COVID-19 data we use is stored in the [GISAID](gisaid.org) (Global Initiative of Sharing all Influenza Data) database. We update the information weekly in order to provide graphs and trends that are up-to-date and indicative of the current COVID-19 situation. 

Explained below are the methods for how we analyzed the data:

The dataset includes information on the variant each patient had, when the information was collected, their location (as specific as the state), and more. We focused on these three details. We will use "V" to represent the variant of interest (i.e.: the Alpha variant)

Our first function has an input of a specific variant or location and outputs a list of the number of cases for each epiweek. The code checks the variant or location column for a specific label (e.g. "B.1.1.7" or "USA") as well as the date collected, separating the number of patients by week.  We implemented this function to calculate the total number of COVID-19 and V cases in the U.S. 

We plotted both the total number of COVID-19 and V cases. For analyses below, when considering variants other than B.1.1.7, instead of comparing it to the total COVID cases, we compared it to the total cases between variant V and B.1.1.7.

Figure 2 represents the percentage of V cases (*m<sub>i</sub>*) out of the the total number of cases (*n<sub>i</sub>*). *m<sub>i</sub>* and *n<sub>i</sub>* are the observed counts from the dataset. The subscript *i* represents that the number of cases are determined by each week. *p<sub>i</sub>*, the portion of COVID-19 cases that are V , is estimated below:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0Ap_i%20%26%3D%20%5Cfrac%7Bm_i%7D%7Bn_i%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;"> 

We created error bounds using a 95% credible interval derived from the beta prior and binomal likelihood. *p* is the variable that deterimines the probability (*p<sub>i</sub>*). This is the beta distribition pdf, with shape parameters &alpha; and &beta;:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Cfrac%7Bp%5E%7B%5Calpha-1%7D(1-p)%5E%7B%5Cbeta-1%7D%7D%7B%5CBeta(%5Calpha%2C%20%5Cbeta)%7D%0A%5Cend%7Balign*%7D" class="center" style="display: block; margin-left: auto; margin-right: auto;">



Now, we can define the prior as a uniform prior using &alpha;=1 and &beta;=1:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Ctextrm%7BBeta%7D(%5Calpha%2C%5Cbeta)%20%26%3D%20%5Ctextrm%7BBeta%7D(1%2C1)%5C%5C%0A%5Cfrac%7Bp%5E%7B0%7D(1-p)%5E%7B0%7D%7D%7B%5CBeta(1%2C1)%7D%20%26%3D%201%5C%5C%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

The fact that the prior equals 1 suggests that every value from 0 to 1 has an equal likelihood of being *p<sub>i</sub>* for each i.

The binomial likelihood was then calculated as follows, with n equal to the total number of COVID-19 cases, and k equal to the number of observed COVID-19 V cases: 

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Ctextrm%7BBinom%7D(n%2Cp)%20%26%3D%20%5Cbinom%7Bn%7D%7Bk%7Dp%5Ek(1-p)%5E%7Bn-k%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

The posterior is calculated by multiplying the prior with the likelihood, and since the prior is equal to 1, the posterior is equal to the prior. The equation above can be rearranged into:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0Ap%5E%7Bk%7D(1-p)%5E%7Bn-k%7D%20%26%3D%20p%5E%7B(k%2B1)-1%7D(1-p)%5E%7B(n-k%2B1)-1%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

This then can be written as:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Ctextrm%7BBeta%7D(k%2B1%2C%20n-k%2B1)%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

If we were to maximize this function by setting the derivative to 0, *p* would be estimated as *n/k*. This is the MAP (Maximum a posteriori) estimator for p. We calculated the 95% credible interval by computing the 0.025 and 0.975 quantiles of the beta distribution.

According to epidemiologic data, we knew that the graph would be logistic. Therefore, we were able to use a logit function in order to create a linear model:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0Ay_i%20%26%3D%20%20%5Clog%7B%5Cfrac%7Bp_i%7D%7B1-p_i%7D%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

A linear regression model was then computed. First, we used the linear regression estimate of slope. *x<sub>i</sub>* represents the week number, and we define *<SPAN STYLE="text-decoration:overline">x</SPAN>* and *<SPAN STYLE="text-decoration:overline">y</SPAN>* to be the means of *x<sub>i</sub>* and *y<sub>i</sub>* respectively. *W* is the total number of epiweeks available. Here, we calculate the slope, *m*:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0Am%20%3D%20%5Cfrac%7B%5Csum_%7Bi%3D0%7D%5E%7BW%7D(x_i-%5Cbar%7Bx%7D)(y_i-%5Cbar%7By%7D)%7D%7B%5Csum_%7Bi%3D0%7D%5E%7BW%7D(x_i-%5Cbar%7Bx%7D)%5E2%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

*&#375;<sub>i</sub>* is the y-coordinate for the linear regression model, whose equation is listed below:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Chat%7By%7D_i%20%3D%20m(x_i-%5Cbar%7Bx%7D)%2B%5Cbar%7By%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

The 95% credible intervals are then determined again by a beta prior and binomial likelihood. The doubling time, which is how long it takes for the number of V cases to double. In order to find this, we calculated in logistic space, how long it would take to double *p<sub>i</sub>*, which was *ln(2)*. Then, to get the change in time, we divided *ln(2)* by *m* (the slope). 

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0At%20%3D%20%5Cfrac%7B%5Cln%7B2%7D%7D%7Bm%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

The last step was to convert this linear model back to the logit scale to estimate a logistic curve for our data. To do so, we created the inverse of the logit function:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%0A%5Cbegin%7Balign*%7D%0A%5Chat%7Bp_i%7D%20%3D%20%5Cfrac%7Be%5E%7B%5Chat%7By_i%7D%7D%7D%7B1%2Be%5E%7B%5Chat%7By_i%7D%7D%7D%0A%5Cend%7Balign*%7D" style="display: block; margin-left: auto; margin-right: auto;">

Thus, we were able to fit a logistic curve to our data.

In addition to the linear model, we created a local regression. We used intervals of 5 weeks and calculated the equations of the lines for each interval. Essentially, it is a localized version of the linear model. 

The reproductive number is defined as the number of people one infected person can trasmit the disease to over an incubation period of 5 days. Using this, we can calculate the transmissibility ratio, which is the reproductive number of the V variant (*R<sub>B</sub>*) over the reproductive number of the other variants (*R<sub>0</sub>*):

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%7B%5Cfrac%7BR_B%7D%7BR_0%7D%7D" class="center" style="display: block; margin-left: auto; margin-right: auto;">

The slope of the graph of the *log(p/(1-p))* over time can be calculated as the change of the log ratio over one incubation period (5/7 of a week). If we consider  *p* as the initial proportion of V cases and note that over one incubation period the V cases will grow by a factor of *R<sub>B</sub>*, while other cases grow by a factor of *R<sub>0</sub>*, then slope will be calculated as follows:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%7Bm%20%3D%20%5Cfrac%7B%5Clog%7B%5Cfrac%7Bp*R_B%7D%7B(1-p)*R_0%7D%7D%20-%5Clog%7B%5Cfrac%7Bp%7D%7B1-p%7D%7D%7D%7B%5Cfrac%7B5%7D%7B7%7D%7D%7D" class="center" style="display: block; margin-left: auto; margin-right: auto;">

By logarithmic properties, we can simply the expression to:

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%7Bm%20%3D%20%5Cfrac%7B%5Clog%7B%5Cfrac%7BR_B%7D%7BR_0%7D%7D%7D%7B%5Cfrac%7B5%7D%7B7%7D%7D%7D" class="center" style="display: block; margin-left: auto; margin-right: auto;">

Thus, we can manipulate *m* to get the trasmissibility ratio (*T*):

<img src="https://render.githubusercontent.com/render/math?math=%5CLARGE%7BT%20%3D%20e%5E%7B(%5Cfrac%7B5%7D%7B7%7D)*m%7D%7D" class="center" style="display: block; margin-left: auto; margin-right: auto;">