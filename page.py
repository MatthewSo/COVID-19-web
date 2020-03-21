from flask import Flask, render_template
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

import string
import random

#VAR
mailman_undoc_predictions = "county_undoc.csv"
mailman_doc_predictions = "county_doc.csv"
csse_daily_reports_folder = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports"

app = Flask(__name__, static_url_path='/static')

var = {
    'csse_total_confirmed':0,
    'csse_total_deaths':0,
    'csse_total_recovered':0,
    'csse_updated':"0",
    'csse_daily_reports_df':[],
    'mailman_14_day_undoc_total':0,
    'mailman_14_day_doc_total':0,
    'mailman_14_day_date':"Date Here"
}

def forecast_14_day():
        response = urllib.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') 
        counties = json.load(response)
        df = pd.read_csv("county_undoc.csv",  dtype={"FIPS": str})
        fig = go.Figure()
        max = 0.0   
        for column in df.columns:
            if (column[0:3] == "Day"):
                print(column)
                if df[column].max() > max:
                    max = df[column].max().astype(float)
                fig.add_trace(go.Choropleth(
                    zmax=1.0, zmin = 0.0,
                    zauto = False,
                    visible = False,
                    locations=df['FIPS'],
                    ids=df['County'],
                    text=df['County'],
                    hoverinfo="text+z",
                    z=df[column].astype(float),
                    zsrc="Data from Jeffery Shaman at Columbia University Mailman School of Public Health",
                    geojson = counties,
                    colorscale='jet',
                    marker_line_width=0, # line markers between states
                    
            )
            )

        
        for i in range(len(fig.data)):
            fig.data[i].update( zauto = False,zmax=max, zmin = 0)

        fig.data[0].update (visible=True)    
        
        steps = []
        for i in range(len(fig.data)):
            step = dict(
                method="restyle",
                args=["visible", [False] * len(fig.data)],
                label = str(i + 1)
                )
            step["args"][1][i] = True  # Toggle i'th trace to "visible"
            steps.append(step)
            
        sliders = [dict(
            currentvalue={"prefix": "Day: "},
            pad={"t": 50},
            steps=steps
            )]
        
        fig.update_layout(
            title_text='COVID-19 14 Day Projection',
            sliders=sliders,
            #coloraxis = {'colorscale':'reds'},
            geo = dict(
                scope='usa',
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'),
            annotations=[dict(xref='paper', yref='paper',x=0.5, y=1.1,showarrow=False, text ='Data provided by Jeffery Shaman from the Columbia University Mailman School of Public Health')]
        ) 
        pio.write_html(fig, file='templates/14dayforecast.html', auto_open=False)
        return fig

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

def update_prediction_data():
    df = pd.read_csv(mailman_undoc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_undoc_total'] = df['Day14'].sum()
    df = pd.read_csv(mailman_doc_predictions,  dtype={"FIPS": str})
    var['mailman_14_day_doc_total'] = df['Day14'].sum()

def write_counter():
    string="<!DOCTYPE html> <html><body><h1>Confirmed Cases:</h1><h1 style=\"color:red\">"+str(var["csse_total_confirmed"])+"</h1><h3>Last Updated on " + var["csse_updated"] + "</h3><h1>14 Day Predicted US Cases:</h1><h1><span style=\"color:red\">"+ str(var["mailman_14_day_doc_total"])+"</span> by <span style=\"color:green\">"+ str(var["mailman_14_day_date"])+"</span></h1>"
    
    string= string + "</body></html>"
    text_file = open("templates/counters.html", "w+")
    text_file.write(string)
    text_file.close()

hopkins_pull()
update_csse_data()
update_prediction_data()
write_counter()
#forecast_14_day()







posts = [
    {
        'author': 'Matthew So',
        'title': 'Title',
        'content': 'Here is where we will put our data',
        'date': 'Today'
        }

]


for i in range(30):
    author = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
    title = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
    date = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))
    content = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(100))
    posts.append({'author': author, 'title':title, 'content':content, 'date':date})




@app.route("/gitpullc0pXalg2YTPY1QaN")
def gitpull():
    hopkins_pull()


@app.route("/updates")
@app.route("/")
def updates():
    return render_template('UpdatesTemplate.html', posts=posts)


@app.route("/dashboard")
def dashboard():
    return render_template("SoonTemplate.html")

@app.route("/dashboardtemplate")
def dashboardtemplate():
    return render_template("DashboardTemplate.html")

@app.route("/e")
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

if __name__ == '__main__':
    app.run(debug=True)
    
