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

def write_counter(var):
    string="<!DOCTYPE html> <html><body>"
    string = string + '''  <link rel="stylesheet" href="/static/updateAssets/web/assets/mobirise-icons-bold/mobirise-icons-bold.css">
  <link rel="stylesheet" href="/static/updateAssets/web/assets/mobirise-icons/mobirise-icons.css">
  <link rel="stylesheet" href="/static/updateAssets/bootstrap/css/bootstrap.min.css">
  <link rel="stylesheet" href="/static/updateAssets/bootstrap/css/bootstrap-grid.min.css">
  <link rel="stylesheet" href="/static/updateAssets/bootstrap/css/bootstrap-reboot.min.css">
  <link rel="stylesheet" href="/static/updateAssets/dropdown/css/style.css">
  <link rel="stylesheet" href="/static/updateAssets/tether/tether.min.css">
  <link rel="stylesheet" href="/static/updateAssets/theme/css/style.css">
  <link rel="preload" as="style" href="/static/updateAssets/mobirise/css/mbr-additional.css"><link rel="stylesheet" href="/static/updateAssets/mobirise/css/mbr-additional.css" type="text/css">'''
  
    string = string + "<h1>Confirmed Cases:</h1><h1 style=\"color:red\">"+str(var["csse_total_confirmed"])+"</h1><h1>Confirmed US Cases:</h1><h1 style=\"color:red\">"+str(var["csse_us_confirmed"])+"</h1><h3>Last Updated on " + var["csse_updated"] + "</h3><h1>14 Day Predicted US Cases:</h1><h1><span style=\"color:red\">"+ str(var["mailman_14_day_doc_total"])+"</span> by <span style=\"color:green\">"+ str(var["mailman_14_day_date"])+"</span></h1>"
    
    string= string + "</body></html>"
    text_file = open("templates/counters.html", "w+")
    text_file.write(string)
    text_file.close()

def generate_UpdatesTemplate():
    page = '''{% extends "MenuTemplate.html" %}
    {% block content %}

    <section class="engine"><a href="https://mobirise.info/g">how to build a site</a></section><section class="header1 cid-rT9FvFwykj mbr-parallax-background" id="header16-b">

    

    <div class="mbr-overlay" style="opacity: 0.4; background-color: rgb(7, 59, 76);">
    </div>

    <div class="container">
        <div class="row justify-content-md-center">
            <div class="col-md-10 align-center">
                <h1 class="mbr-section-title mbr-bold pb-3 mbr-fonts-style display-1">Mailman COVID-19 Updates</h1>
                
                
                
            </div>
        </div>
    </div>

    </section>'''

    i = 0
    for post in blogLib.load_blog():
        i=i+1
        if i % 2 == 0:
            page = page + '''<section class="mbr-section content4 cid-rT9Gtgjfd0" id="content4-g">

    <div class="container">
        <div class="media-container-row">
            <div class="title col-12 col-md-8">
                <h2 class="align-center pb-3 mbr-fonts-style display-2">''' + post['title'] + '''
                </h2>
                <h5 class="align-center">
                    By ''' + post['author']+'''
                </h5>
                <!----<h3 class="mbr-section-subtitle align-center mbr-light mbr-fonts-style display-5">-->
                    '''+post['content']+'''
               <!-- </h3>-->
                
            </div>
        </div>
    </div>
    </section> 

    '''
        else:
            page = page + '''<section class="mbr-section content4 cid-rT9GyeRrJv" id="content4-e">

    

    <div class="container">
        <div class="media-container-row">
            <div class="title col-12 col-md-8">
                <h2 class="align-center pb-3 mbr-fonts-style display-2">''' + post['title'] +'''</h2>
                <h5 class="align-center">
                    By '''+post['author']+'''
                </h5>
              <!---  <h3 class="mbr-section-subtitle align-center mbr-light mbr-fonts-style display-5">-->
                    '''+post['content']+'''
              <!---  </h3>-->
                
            </div>
        </div>
    </div>
    </section>'''

    page=page+'''{% endblock %}'''
    text_file = open("templates/UpdatesTemplate.html", "w+")
    text_file.write(page)
    text_file.close()