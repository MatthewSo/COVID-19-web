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
import dataControlLib

import projectVariables

import string
import random

#USER
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


dataControlLib.update_data(var)
#assetGenLib.update_assets(var)


@app.route("/c0pXalg2YTPY1QaN")
def forceUpdate():
    dataControlLib.update_data(var)
    assetGenLib.update_assets(var)

@app.route(projectVariables.updates_directory)
@app.route("/")
def updates():
    return render_template(projectVariables.updatestemplate_html_file)

@app.route(projectVariables.dashboardtemplate_directory)
def dashboardtemplate():
    return render_template(projectVariables.dashboardtempalte_html_file)

@app.route(projectVariables.dashboard_directory)
def dashboard():
    return render_template(projectVariables.dashboard_html_file)

@app.route(projectVariables.fourteen_day_forecast_directory)
def forecase():
    return render_template(projectVariables.fourteen_day_forecast_html_file)

@app.route(projectVariables.videoselection_directory)
def videoselection():
    return render_template(projectVariables.videoselection_html_file)

@app.route(projectVariables.counters_directory)
def counters():
    return render_template(projectVariables.counters_html_file)

@app.route(projectVariables.addpost_directory)
def addpost():
    return render_template(projectVariables.addpost_html_file)

@app.route(projectVariables.addpost_directory, methods=['POST'])
def add_post_return():
    user = request.form['username']
    password = request.form['password']
    author = request.form['author']
    title = request.form['title']
    content = request.form['content']
    if (user == blog_user) and (str(hash(password)) == blog_pass):
        blogLib.add_blog_post(author,title,content,date.today())
    assetGenLib.generate_UpdatesTemplate()
    return content

@app.route(projectVariables.deletepost_directory)
def deletepost():
    return render_template(projectVariables.deletepost_html_file)

@app.route(projectVariables.deletepost_directory, methods=['POST'])
def delete_post_return():
    user = request.form['username']
    password = request.form['password']
    title = request.form['title']
    if (user == blog_user) and (str(hash(password)) == blog_pass):
        blogLib.delete_blog_post(title)
    assetGenLib.generate_UpdatesTemplate()
    return title

@app.route("/day1")
def day1():
    return render_template("dynamicTemplates/14dayforecasts/Day1.html")

@app.route("/day2")
def day2():
    return render_template("dynamicTemplates/14dayforecasts/Day2.html")

@app.route("/day3")
def day3():
    return render_template("dynamicTemplates/14dayforecasts/Day3.html")

@app.route("/day4")
def day4():
    return render_template("dynamicTemplates/14dayforecasts/Day4.html")

@app.route("/day5")
def day5():
    return render_template("dynamicTemplates/14dayforecasts/Day5.html")

@app.route("/day6")
def day6():
    return render_template("dynamicTemplates/14dayforecasts/Day6.html")

@app.route("/day7")
def day7():
    return render_template("dynamicTemplates/14dayforecasts/Day7.html")

@app.route("/day8")
def day8():
    return render_template("dynamicTemplates/14dayforecasts/Day8.html")

@app.route("/day9")
def day9():
    return render_template("dynamicTemplates/14dayforecasts/Day9.html")

@app.route("/day10")
def day10():
    return render_template("dynamicTemplates/14dayforecasts/Day10.html")

@app.route("/day11")
def day11():
    return render_template("dynamicTemplates/14dayforecasts/Day11.html")

@app.route("/day12")
def day12():
    return render_template("dynamicTemplates/14dayforecasts/Day12.html")

@app.route("/day13")
def day13():
    return render_template("dynamicTemplates/14dayforecasts/Day13.html")

@app.route("/day14")
def day14():
    return render_template("dynamicTemplates/14dayforecasts/Day14.html")



if __name__ == '__main__':
    app.run(debug=True)
    
