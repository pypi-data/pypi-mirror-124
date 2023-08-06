from PyViO import visuals, methods
import pandas as pd
import numpy as np
import inspect
allowed = ['iqr_method','zs_method','hampel_method','donut','display_out']
import matplotlib.pyplot as plt
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
init_notebook_mode(connected='true')

import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

def iplot_tbl(c,ui):
    if inspect.stack()[1][3] in allowed:
        z = (c.T.values).tolist()
        x = list(c.columns)
        hover = (ui.T.values).tolist()

        colorscale=[[0.0, 'rgb(255,255,255)'], [.2, 'rgb(255, 255, 153)'],
                [.4, 'rgb(153, 255, 204)'], [.6, 'rgb(179, 217, 255)'],
                [.8, 'rgb(240, 179, 255)'],[1.0, 'rgb(255, 77, 148)']]

        w = len(list(c.index))
        h = len(list(c.columns))

        height = h
        width = ((w * 240)* 25.4 ) / 96

        fig = ff.create_annotated_heatmap(z, y=x, text=hover, colorscale=colorscale, font_colors=['black'],
                                          hoverinfo='text', xgap=1, ygap=1,
                                          hoverongaps = True) 

        title='In which rows does your outliers exist?'
        (fig.update_layout(title = title, width=width)) if (w>10) else (fig.update_layout(title = title))
        iplot(fig)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
        
def create_corr_mat(data,parameter):
    if inspect.stack()[1][3] in allowed:
        if (parameter == ""):
            z = (data.corr().values.tolist()) 
            a = []
            for i in z:
                b = []
                for j in i:
                    b.append(float("%0.2f" % j))
                a.append(b)
            z = a
            y = list(data.corr().index)
        else:
            a = list(data.corr().loc[parameter].values)
            z = ["%0.2f" % i for i in a]
            z = [[float(item) for item in z]]
            y = [parameter]

        x = list(data.corr().index)

        fig = ff.create_annotated_heatmap(z,y=y, x=x, colorscale='Viridis')

        (fig.update_layout(title = "Feature Correlation Matrix", width = 700, height = 300)) if (parameter!="") else (fig.update_layout(title = "Feature Correlation Matrix"))
        fig.layout.update(xaxis=dict(title='The features',showgrid=True,side='bottom',tickangle=-30))
        iplot(fig)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
        
def donut(store_data):
    if inspect.stack()[1][3] in allowed:
        labels = ['Outlier %', 'Non-Outlier %']
        values_iqr = methods.iqr_method(store_data,"doNotProp")
        values_zs = methods.zs_method(store_data,"doNotProp")
        values_hampel = methods.hampel_method(store_data,"doNotProp")

        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=labels, values=values_iqr, name="IQR-Method", title = "IQR-Method"),
                    1, 1)
        fig.add_trace(go.Pie(labels=labels, values=values_zs, name="ZS-Method", title = "ZS-Method"),
                    1, 2)
        fig.add_trace(go.Pie(labels=labels, values=values_hampel, name="Hampel-Method", title = "Hampel-Method"),
                    1, 3)

        fig.update_traces(hole=.6, hoverinfo="label+percent+name")

        fig.update_layout(
            title_text="Comparison between all the methods :")
        iplot(fig)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
        
def donut_outliers(out_df):
    if inspect.stack()[1][3] in allowed:   
        fig = plt.figure(figsize=(25,10))
        fig.suptitle('Which feature in the dataset holds how much outliers?', fontsize=24, ha="right")
        i = 0 
        r,c = 0,0 

        l1 = out_df.values.tolist()
        l1_ind = (out_df.index.tolist())

        def trasform_to_matrix(ip):
            div = 4
            op = []
            while ip != []:
                op.append(ip[:div])
                ip = ip[div:]
            return op

        matrix = (trasform_to_matrix(l1))
        row = (len(trasform_to_matrix(l1)))
        col = (len(trasform_to_matrix(l1)[0]))

        for data in matrix:
            c = 0
            r = matrix.index(data)
            for i in data:
                my_circle = plt.Circle((0, 0), 0.7, color='white')
                ax1 = plt.subplot2grid((row,col), (r, c))
                plt.pie(i, autopct='%.0f%%', colors=['red', 'green'])
                plt.title(l1_ind[0], fontsize=16        )
                l1_ind = l1_ind[1:]      
                p = plt.gcf()
                p.gca().add_artist(my_circle)
                c+=1  

        plt.show()
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")

def display_out(data,outlier,outlier_loc,outlier_cat,outlier_value,outlier_proportion,parameter="",outlier_count=0,df_size=0):
    if inspect.stack()[1][3] in allowed: 
        store_data = data

        outlier_value_df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in outlier_value.items()]))
 
        outlier_count_df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in outlier_loc.items()]))
        outlier_count_df = outlier_count_df.rename(index={0: 'Outlier_Count'})

        outlier_category_df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in outlier_cat.items()]))

        outlier_donut = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in outlier_proportion.items()])).T

        donut(store_data)

        fig = go.Figure()
        for col in store_data[store_data.describe().columns]:
            fig.add_trace(go.Box(y=store_data[col].values, name=store_data[col].name))
            fig.update_traces(quartilemethod="exclusive")
        fig.update_layout(title = "Box Plot")
        iplot(fig)

        if (outlier_count > 0): 
            (donut_outliers(outlier_donut), iplot_tbl(outlier_value_df.fillna(0), outlier_category_df.fillna('NA')), create_corr_mat(store_data,parameter))
        else: 
            labels = ['Non-Outliers %']
            fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
            fig.add_trace(go.Pie(labels=labels, title = "No Outlier found in data \U0001F600"))
            fig.update_traces(hole=.9)
            fig.update_layout(title = "There are no outliers in your data for this method!!")
            iplot(fig)
    else:
        msg = f"Not allowed"
        raise SystemExit(f"Error: {msg}")
        