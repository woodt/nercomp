#! /usr/bin/env python

import csv
from collections import defaultdict
import datetime
import numpy as np
import matplotlib as mpl
mpl.use('Qt4Agg')

import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter

f = open("commits.csv")
reader = csv.reader(f)
commits = defaultdict(list)

first_date = None
last_date = None

for row in reader:
    project = row[0]
    commit_date = datetime.datetime.strptime(row[1], "%m/%d/%Y %H:%M")
    if first_date is None or commit_date < first_date:
        first_date = commit_date
    if last_date is None or commit_date > last_date:
        last_date = commit_date
    mpl_date = date2num(commit_date)
    commits[project].append(mpl_date)

f.close()


f = open("deployments.csv")
reader = csv.reader(f)
deployments = defaultdict(list)
for row in reader:
    # Date,Application,Version,Destination
    deployment_date = datetime.datetime.strptime(row[0], "%m/%d/%y")
    destination = row[3]
    deployments[destination].append(date2num(deployment_date))
f.close()
    
arrays = dict()
for key in commits:
    arrays[key] = np.array(commits[key])

hfmt = DateFormatter('%Y')
fig = plt.figure()
ax = plt.subplot2grid((4, 1), (0, 0), rowspan=2)
bins = mpl.dates.drange(first_date, last_date, datetime.timedelta(days=14))

ax.set_ylabel("Commits to trunk")
ax.hist(arrays.values(), bins=bins, label=arrays.keys(),
        histtype='barstacked')
ax.grid(True)
ax.legend()

ay = plt.subplot2grid((4, 1), (2, 0))

staffing = [3, 4, 5, 6, 5, 4, 5]

start_dates = [
    date2num(datetime.date(2007, 1, 17)),
    date2num(datetime.date(2009, 1, 30)),
    date2num(datetime.date(2010, 4, 30)),
    date2num(datetime.date(2010, 8, 13)),
    date2num(datetime.date(2010, 8, 30)),
    date2num(datetime.date(2011, 4, 1)),
    date2num(datetime.date(2011, 8, 30))
]

durations = [ start_dates[i + 1] - start_dates[i]
             for i in range(0, len(start_dates) - 1)]
durations.append(date2num(last_date) - start_dates[-1])

ay.bar(start_dates, staffing, durations, edgecolor='none')
ay.grid(True)
ay.set_ylabel("Staffing")

ad = plt.subplot2grid((4, 1), (3, 0))

ad.set_ylabel("Deployments")
ad.hist(deployments.values(), bins=bins, label=deployments.keys(),
        histtype='barstacked')

ad.grid(True)
ad.legend()

for axis in [ax, ay, ad]:
    axis.xaxis.set_major_formatter(hfmt)
    axis.xaxis.set_major_locator(mpl.dates.YearLocator())
    axis.xaxis.set_minor_locator(mpl.dates.MonthLocator())

ad.set_xlabel("Sprints")

plt.show()
plt.tight_layout()



