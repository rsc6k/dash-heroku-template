import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

my_info = '''
The gender wage gap has been of great concern for a number of years. Recent data from [Pew Research](https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/) showed that in the US, women earned 84% of their male counterparts in 2020. This discrepancy is of great consequnce in a quest for gender equality. Pew cites gender discrimination and the challenges of being a mother as leading factors in the wage gap. There is hope, however. Pew Research found the gap was smaller amongst individuals aged 25-34 than those in higher age brackets. Also recent studies out of China show that FinTech is allowing for women to increasingly approach their male counterparts. This industry as examined in [China and World Economy](https://onlinelibrary.wiley.com/doi/full/10.1111/cwe.12382?casa_token=0rhhFgYpsGsAAAAA%3AWaYwq-TE1ZQizR58davx4tGVAh-4ZftJaVpiIZbVwlm_mhnP6jNUFldkkt6OJwrjaqkn6QWwWmWwa7E) has particularly high access to capital and low operating costs. This facilitates an easier path for women to meet their male counterparts head on. So while the gender wage gap is certainly still a dominant issue, there is hopes of it shrinking in the coming years.

To examine some of the data and sentiments relating to gender wage gap in the US, the [GSS] (http://www.gss.norc.org/About-The-GSS) or General Society Survey can be examined. This survey takes primarily face-to-face interview information (with some online surveying as well) on a swath of demographic and societal questions and distills it into a computer parseable dataset. In addition to survey answers, the dataset includes information about the respondants age, sex, salary, and education. The sum total of this information is extremely valuable in evaluating trends in gender, racial, and social trends across the US.
'''

gss_table = gss_clean.groupby('sex').agg({'income':'mean', 'job_prestige':'mean', 'socioeconomic_index':'mean', "education":"mean" }).round(2).reset_index()
gss_table = gss_table.rename(columns = {"income" : "Avg<br>Annual<br>Income",
                              "job_prestige" : "Avg<br>Occupational<br>Prestige",
                              "socioeconomic_index" : "Avg<br>Socioeconomic<br>Status",
                              "education" : "Avg<br>Years of<br>Education"})
table = ff.create_table(gss_table)

scatter = px.scatter(gss_clean, x="job_prestige", y="income", color = "sex",
                hover_data=['education', 'socioeconomic_index'],
                trendline='ols', labels = {"income" : "Average Annual Income",
                                          "job_prestige" : "Occupational Prestige"}, width=600, height=400)

boxplot_income = px.box(gss_clean, x="sex", y='income', color = "sex", labels={'income':'Annual Income', 'sex':''}, width=600, height=400)

boxplot_job_prestige = px.box(gss_clean, x="sex", y='job_prestige', color = "sex", labels={'job_prestige': 'Occupational Prestige', 'sex':''},
                             width=600, height=400)

mini_frame = gss_clean[["income", "sex", "job_prestige"]]
mini_frame.dropna(inplace = True)
mini_frame["job_prestige_binned"] = pd.cut(mini_frame["job_prestige"], 6, 
                                           )
mini_frame = mini_frame.sort_values(by="sex", ascending = False)
grouped = px.box(mini_frame, x='sex', y='income', color='sex', 
             facet_col='job_prestige_binned', facet_col_wrap=2, width=600, height=400)

categories_list = ["satjob", "relationship", "male_breadwinner", "men_bettersuited", "child_suffer", "men_overwork"]
group_by_list = ["sex", "region", "education"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    [    
    html.Div([    
    html.H1("An Examination of the General Social Survey (GSS)"),
    dcc.Markdown(children = my_info)],
        className = "four columns"),
        
        
    html.Div([   
        html.Div([
    html.H3("Income, Occupational Prestige, Socioeconomic Status, and Education across Gender"),
    dcc.Graph(figure = table)], style = {'width':'48%', 'float':'left'}),
        html.Div([
    html.H3("Relationship between Income and Occupational Prestige across Gender"),
    dcc.Graph(figure = scatter)],style = {'width':'48%', 'float':'right'}),
        
        html.Div([
    html.H3("Categories Dropdown"),
    dcc.Dropdown(id = "categories_dropdown",
            options = [{'label': i, 'value': i} for i in categories_list], 
                    value = "satjob")],style = {'width':'48%', 'float':'left'}),
        html.Div([
    html.H3("Group By Dropdown"),
    dcc.Dropdown(id = "groupby_dropdown",
            options = [{'label': i, 'value': i} for i in group_by_list], 
                    value = "sex")],style = {'width':'48%', 'float':'left'}),   
    html.H3("Difference in Response to Category by Grouped By"),
    dcc.Graph(id = "barplot"),
        
   
        
    html.Div([
        html.H4("Distribution of Income across Gender"),
        dcc.Graph(figure = boxplot_income)
    ], style = {'width':'48%', 'float':'left'}
    ),
    html.Div([
        html.H4("Distribution of Occupation Prestige across Gender"),
        dcc.Graph(figure = boxplot_income)
    ], style = {'width':'48%', 'float':'right'}
    ),
        
    html.H3("Income for different Occupational Prestiges across Gender"),
    dcc.Graph(figure = grouped)], className = "eight columns")
             
]
)
@app.callback(
Output("barplot", "figure"), 
Input("categories_dropdown", "value"),
Input("groupby_dropdown", "value") 
)
def createbarplot(ctg, group):
    plot = gss_clean.groupby([group, ctg]).agg({ctg : "size"})
    plot = plot.rename({ctg :'count'}, axis=1)
    plot = plot.reset_index()
    barplot2 = px.bar(plot, x=ctg, y='count', color =group, barmode='group',
      labels={ctg:'Response to' + ctg , 'count':'Response Count'}, width=600, height=400)
    return barplot2

if __name__ == '__main__':
    app.run_server(debug=True)
