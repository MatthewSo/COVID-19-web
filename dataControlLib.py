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

import projectVariables



def hopkins_pull():
    g = git.cmd.Git("COVID-19")
    g.pull()
    print(glob.glob("COVID-19/*"))

def update_csse_data(var):
    csse_daily_reports = glob.glob(projectVariables.csse_daily_reports_folder + "/*")
    csse_daily_reports.remove(max(csse_daily_reports))

    csse_daily_report_latest_date = max(csse_daily_reports)[-14:-4]
    csse_daily_reports_df = pd.read_csv(max(csse_daily_reports))

    var['csse_total_confirmed'] = csse_daily_reports_df['Confirmed'].sum()
    var['csse_total_deaths'] = csse_daily_reports_df['Deaths'].sum()
    var['csse_total_recovered'] = csse_daily_reports_df['Recovered'].sum()
    var['csse_updated'] =  csse_daily_report_latest_date
    var['csse_daily_reports_df'] = csse_daily_reports_df
    var['csse_us_confirmed'] = csse_daily_reports_df.loc[csse_daily_reports_df['Country_Region'] == 'US', 'Confirmed'].sum()
    print (var['csse_us_confirmed'])

def update_prediction_data(var):
    df = pd.read_csv(projectVariables.mailman_undoc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_undoc_total'] = df['Day14'].sum()
    df = pd.read_csv(projectVariables.mailman_doc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_doc_total'] = df['Day14'].sum()

def update_data(var):
    hopkins_pull()
    update_csse_data(var)
    update_prediction_data(var)
    zip_fips_data(var)
    zip_state_data(var)

def zip_fips_data(var):
    var['zips_fips'] =  pd.read_csv("ZIP_FIPS.csv")[['ZIP','COUNTY']].copy()

def zip_state_data(var):
    var['zips_states'] = pd.read_csv("ZIP_STATE.csv")[['zip','state']].copy()


def fips_finder(var,zip):
    if var['zips_fips'].loc[var['zips_fips']['ZIP'] == zip].size == 0:
        return 0
    return int(var['zips_fips'].loc[var['zips_fips']['ZIP'] == zip].iloc[0]['COUNTY'])

def state_finder(var,zip):
    return var['zips_states'].loc[var['zips_states']['zip'] == zip].iloc[0]['state']


