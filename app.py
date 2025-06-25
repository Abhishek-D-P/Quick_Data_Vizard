import dash
from dash import html,dcc,dash_table,Input,Output
import plotly.express as px
import pandas as pd
import numpy as np

df=pd.read_csv('data/house-prices/df.csv')

img_size=200

app=dash.Dash(__name__)

info=df.dtypes.reset_index()
info.columns=['columns','dtypes']
info = info.astype(str)

cat_col=list(df.select_dtypes('object').columns)
num_col=list(df.select_dtypes(exclude='object').columns)

null_df=(df.isna().sum()[df.isna().sum()>0]/len(df)*100).reset_index()
null_df.sort_values(by=0,ascending=False,inplace=True)
null_df.columns=['columns','Null values']

null_fig = px.bar(
    null_df,
    x='columns',
    y='Null values',
    title="Null values",
 
)

null_fig.update_layout(
    xaxis_tickangle=-45,
    height=img_size*1.5,
    margin=dict(l=10, r=10, t=50, b=50),
    width=img_size*2.5,
)



app.layout=html.Div(className='my-div',children=[
    html.H1("The best EDA App",),
    html.Div(className='my-div',id='container',
        children=[html.Div(className='my-div',id='analysis',
                           children=[dcc.RadioItems(
                               id='Analysis-selector',
                               options=[ {'label': 'Univariate', 'value': 'Univariate'}, 
                                        {'label': 'Bivariate', 'value': 'Bivariate'}],
                               
                           ),
                           html.Div(className='my-div',id='Univariate_div',style={'display':'None'},
                                    children=[
                                        dcc.RadioItems(id='u_column_type_selector',className='radio',
                                                       options=[{'label':'categorical','value':'categorical'},
                                                                {'label':'Numerical','value':'numerical'}]),
                                        dcc.Dropdown(id='u_columns_selector',className='dropdown',
                                                      placeholder='Select a column',
                                                      ),
                                        dcc.Dropdown(id='u_chart_selector',className='dropdown',
                                                      placeholder='Select a chart',
                                                      ),
                                        dcc.Graph(id='univariate_graph',figure=None,style={'height':'350px','width':'95%','margin':'auto'})
                                    ]),
                           html.Div(className='my-div',id='Bivariate_div',style={'display':'None'},
                                    children=[
                                        dcc.RadioItems(id='bi_column_type_selector',
                                                       options=[{'label':'categorical vs categorical','value':'categorical vs categorical'},
                                                                {'label':'numerical vs numerical','value':'numerical vs numerical'},
                                                                {'label':'categorical vs numerical','value':'categorical vs numerical'}]),
                                        
                                        dcc.Dropdown(id='bi_columns_selector_1',className='dropdown',
                                                      placeholder='Select a column',
                                                      ),
                                        dcc.Dropdown(id='bi_columns_selector_2',className='dropdown',
                                                      placeholder='Select a column',
                                                      ),
                                        dcc.Dropdown(id='bi_chart_selector',className='dropdown',
                                                      placeholder='Select a chart',
                                                      ),
                                        dcc.Graph(id='bivariate_graph',figure=None,style={'height':'350px','width':'95%','margin':'auto'})

                                    ]),
                               



                           ] ),
                  html.Div(id='data-desc',
                           children=[html.H2('Data Description',),
                            html.P(f'shape:{df.shape[0]} rows and {df.shape[1]} columns '
                                   ,id='data-shape'),
                            dash_table.DataTable(
                                id='data-info',
                                columns=[{"name": str(i), "id": str(i)} for i in info.columns],
                                data=info.to_dict('records'),
                                style_table={     # horizontal scroll
                                                    'overflowY': 'auto',     # vertical scroll
                                                    'maxHeight': '150px',    # limit height to enable scroll
                                                    'margin': 'auto',
                                                    'width': '100%',
                                                    'border': '1px solid #ccc',
                                                    },
                                style_cell={'textAlign': 'center',
                                                'minWidth': '10px','maxWidth':'30px',
                                                'whiteSpace': 'normal','background-color':'#a181b5','color':'black'},
                                style_header={'fontWeight': 'bold', 'background-color':'#a181b5','color':'black'},
                               ),
                            dcc.Graph(figure=null_fig,id='null-plot',)
                            ])
        
            
                    ])
        
    ])
    

@app.callback(
    Output("Univariate_div",'style'),
    Output('Bivariate_div','style'),
    Input('Analysis-selector','value')
)
def show_analysis(value):
    uni_style={'display':'None'}
    bi_style={'display':'None'}
    if value=='Univariate':
        uni_style={'display':'block','margin-top':'20px'}
    elif value=='Bivariate':
        bi_style={'display':'block','margin-top':'20px'}
    
    return uni_style,bi_style



@app.callback(
    Output('u_columns_selector','options'),
    Output('u_chart_selector','options'),
    Input('u_column_type_selector','value')
)
def Univariate_column_selector_update(value):
 
    if value=='categorical':
        return  [{'label': col, 'value': col} for col in cat_col],[{'label':'barplot','value':'barplot'}]
    elif value=='numerical':
        return  [{'label': col, 'value': col} for col in num_col],[{'label':'histogram','value':'histogram'},{'label':'boxplot','value':'boxplot'}]
    else:
        return [{'label':'None','value':'none'}],[{'label':'None','value':'none'}]

@app.callback(
    Output('univariate_graph','figure'),
    Input('u_columns_selector','value'),
    Input('u_chart_selector','value')
)
def update_univariate_graph(selected_col,selected_chart):
    if selected_col is None or selected_col not in df.columns or selected_chart is None:
            return {}

    if selected_chart in ('barplot','histogram'):
        fig = px.histogram(df, x=selected_col, nbins=50, title=f"Distribution of {selected_col}",)
    elif selected_chart == 'boxplot':
        fig = px.box(df, x=selected_col, title=f"Distribution of {selected_col}",)


    return fig

####################################### bi variate ######################



@app.callback(
    Output('bi_columns_selector_1','options'),
    Output('bi_columns_selector_2','options'),
    Output('bi_chart_selector','options'),
    Input('bi_column_type_selector','value')
)
def bivariate_column_selector_update(value):
 
    if value=='numerical vs numerical':
        return  [{'label': col, 'value': col} for col in num_col],[{'label': col, 'value': col} for col in num_col],[{'label':'scatterplot','value':'scatterplot'}]
    elif value=='categorical vs numerical':
        return  [{'label': col, 'value': col} for col in num_col],[{'label': col, 'value': col} for col in cat_col],[{'label':'barplot','value':'barplot'}]
    else:
        return [{'label':'None','value':'none'}],[{'label':'None','value':'none'}],[{'label':'None','value':'none'}]

@app.callback(
    Output('bivariate_graph','figure'),
    Input('bi_columns_selector_1','value'),
    Input('bi_columns_selector_2','value'),
    Input('bi_chart_selector','value')
)
def update_bivariate_graph(selected_col1,selected_col2,selected_chart):
    if selected_col1 is None or selected_col2 is None or selected_chart is None:
            return {}

    if selected_chart == 'barplot':
        fig = px.bar(df, x=selected_col2, y=selected_col1, title=f"Distribution of {selected_col2}",)
    elif selected_chart == 'scatterplot':
        fig = px.scatter(df, x=selected_col2, y=selected_col1,title=f"Distribution of {selected_col1}",)


    return fig

    

if __name__=='__main__':
    app.run(debug=True)

