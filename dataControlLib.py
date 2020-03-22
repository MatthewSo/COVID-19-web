from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px
import json
import urllib
import plotly.io as pio
import git
import os
import glob
import pickle
from datetime import date



def hopkins_pull():
    g = git.cmd.Git("COVID-19")
    g.pull()
    print(glob.glob("COVID-19/*"))

def update_csse_data():
    csse_daily_reports = glob.glob(csse_daily_reports_folder + "/*")
    csse_daily_reports.remove(max(csse_daily_reports))

    csse_daily_report_latest_date = max(csse_daily_reports)[-14:-4]
    csse_daily_reports_df = pd.read_csv(max(csse_daily_reports))

    var['csse_total_confirmed'] = csse_daily_reports_df['Confirmed'].sum()
    var['csse_total_deaths'] = csse_daily_reports_df['Deaths'].sum()
    var['csse_total_recovered'] = csse_daily_reports_df['Recovered'].sum()
    var['csse_updated'] =  csse_daily_report_latest_date
    var['csse_daily_reports_df'] = csse_daily_reports_df
    var['csse_us_confirmed'] = csse_daily_reports_df.loc[csse_daily_reports_df['Country/Region'] == 'US', 'Confirmed'].sum()
    print (var['csse_us_confirmed'])

def update_prediction_data():
    df = pd.read_csv(mailman_undoc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_undoc_total'] = df['Day14'].sum()
    df = pd.read_csv(mailman_doc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_doc_total'] = df['Day14'].sum()