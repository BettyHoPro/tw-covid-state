import numpy as np
import matplotlib.pyplot as plt
import datetime as dt



date_day0 = dt.date(2021,5,15)
date_today = dt.date.today()
date_delta = dt.date.today() - date_day0
day_delta = date_delta.days
date_array = np.array( [( date_day0+dt.timedelta(days=i) ).strftime("%m%d") for i in range(day_delta)] ) 

#######################################
### update these 3 quantities daily ###
#######################################
daily_tested = np.array( [6534.,8459.,15617.,18178.,17867.,18099.,21875.,14568.,12911.,23608., 25005., 21634., 20512., 15190.] ) #https://od.cdc.gov.tw/eic/covid19/covid19_tw_stats.csv May 27 送驗數字更新 
daily_reported_positive = np.array( [185.,280.,533.,454.,525.,474.,424.,472.,487.,498., 482., 505., 493., 342., 320. ] ) #Add MAY 28,  correction before May 27,
daily_reported_positive_rate = np.array( [5.8,4.4,2.6,2.2,2.1,2.7,2.8,3.4,3.4, ] )*0.01 #covid-19 本土病例 每日採檢陽性率 , May 24 not update yet. 
daily_reported_total = daily_reported_positive / daily_reported_positive_rate
## https://data.gov.tw/dataset/120451 ##

#######################################
### Epidemic statistics calculation ###
#######################################
daily_positive_rate = daily_reported_positive_rate
daily_positive_total_estimate = daily_positive_rate * daily_tested

daily_positive_rate_SD = np.sqrt( daily_positive_rate * (1-daily_positive_rate) / daily_reported_total )
daily_positive_total_estimate_SD = daily_positive_rate_SD * daily_tested

CL90_sigma = 1.64
CL95_sigma = 1.96
CL99_sigma = 2.57
daily_positive_total_estimate_CL90_up = daily_positive_total_estimate + daily_positive_total_estimate_SD*CL90_sigma
daily_positive_total_estimate_CL90_lo = daily_positive_total_estimate - daily_positive_total_estimate_SD*CL90_sigma
daily_positive_total_estimate_CL95_up = daily_positive_total_estimate + daily_positive_total_estimate_SD*CL95_sigma
daily_positive_total_estimate_CL95_lo = daily_positive_total_estimate - daily_positive_total_estimate_SD*CL95_sigma
daily_positive_total_estimate_CL99_up = daily_positive_total_estimate + daily_positive_total_estimate_SD*CL99_sigma
daily_positive_total_estimate_CL99_lo = daily_positive_total_estimate - daily_positive_total_estimate_SD*CL99_sigma

#########################
### Data presentation ###
#########################
plt.fill_between(date_array, daily_positive_total_estimate_CL99_lo, daily_positive_total_estimate_CL99_up, \
    color="lightblue", label="99% CL", lw=0.)
plt.fill_between(date_array, daily_positive_total_estimate_CL95_lo, daily_positive_total_estimate_CL95_up, \
    color="plum", label="95% CL", lw=0.)
plt.fill_between(date_array, daily_positive_total_estimate_CL90_lo, daily_positive_total_estimate_CL90_up, \
    color="mistyrose", label="90% CL", lw=0.)
plt.plot(date_array, daily_positive_total_estimate, \
    ls="-", lw=2, marker="X", ms=15, c="deepskyblue", label="ctr. est.")
plt.plot(date_array, daily_reported_positive, \
    ls="-", lw=2, marker="o", ms=8, c="deepskyblue", label="cur. #")


plt.legend(fontsize=20, loc="lower right")
plt.ylim(bottom=0)

plt.xlabel("Date", fontsize=20)
plt.ylabel("#positive", fontsize=20)

plt.xticks(fontsize=20, rotation=30)
plt.yticks(fontsize=20)

plt.tight_layout()
plt.show()