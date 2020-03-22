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
import blogLib
import assetGenLib

import string
import random

#VAR
mailman_undoc_predictions = "county_undoc.csv"
mailman_doc_predictions = "county_doc.csv"
csse_daily_reports_folder = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"
blog_file = "blog.pkl"

blog_user="miso"
blog_pass='-905124903459320104'




app = Flask(__name__, static_url_path='/static')

var = {
    'csse_total_confirmed':0,
    'csse_total_deaths':0,
    'csse_total_recovered':0,
    'csse_updated':"0",
    'csse_daily_reports_df':[],
    'csse_us_confirmed':0,
    'mailman_14_day_undoc_total':0,
    'mailman_14_day_doc_total':0,
    'mailman_14_day_date':"04-02-2020"
}

posts=[]



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








hopkins_pull()
update_csse_data()
update_prediction_data()
assetGenLib.write_counter(var)
posts = blogLib.load_blog()

assetGenLib.generate_UpdatesTemplate()









@app.route("/gitpullc0pXalg2YTPY1QaN")
def gitpull():
    hopkins_pull()


@app.route("/updates")
@app.route("/")
def updates():
    return render_template('UpdatesTemplate.html')


@app.route("/dashboardtemplate")
def dashboardtemplate():
    return render_template("DashboardTemplate.html")

@app.route("/dashboard")
@app.route("/experiment")
def experimental():
    return render_template('ExperimentTemplate.html')

@app.route("/14dayforecast")
def forecase():
    return render_template("14dayforecast.html")

@app.route("/videoselection")
def videoselection():
    return render_template("videoselection.html")

@app.route("/counters")
def counters():
    return render_template("counters.html")

@app.route("/addpost")
def addpost():
    return render_template("addpost.html")

@app.route('/addpost', methods=['POST'])
def add_post_return():
    user = request.form['username']
    password = request.form['password']
    author = request.form['author']
    title = request.form['title']
    content = request.form['content']
    if (user == blog_user) and (str(hash(password)) == blog_pass):
        blogLib.add_blog_post(author,title,content,date.today())
    generate_UpdatesTemplate()
    return content

@app.route("/deletepost")
def deletepost():
    return render_template("deletepost.html")

@app.route('/deletepost', methods=['POST'])
def delete_post_return():
    user = request.form['username']
    password = request.form['password']
    title = request.form['title']
    if (user == blog_user) and (str(hash(password)) == blog_pass):
        blogLib.delete_blog_post(title)
    generate_UpdatesTemplate()
    return title

if __name__ == '__main__':
    app.run(debug=True)
    
