'''
 # @ Create Time: 2022-06-22 19:16:27.681139
'''
import dash
import pandas as pd
from dash import dash_table,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np
import base64
import datetime
import io
from dash_bootstrap_templates import ThemeSwitchAIO

template_theme1 = "united"
template_theme2 = "solar"
url_theme1 = dbc.themes.UNITED
url_theme2 = dbc.themes.SOLAR
option1={'label': 'Scatter Chart', 'value': 'scatter'},{'label': 'Line Chart', 'value': 'line'},{'label': 'Bar Chart', 'value': 'bar'}, {'label': 'Pie Chart', 'value': 'pie'},{'label': 'Box Chart', 'value': 'box'},{'label': 'Histogram Chart', 'value': 'hist'},
   
option2={'label': 'Scatter Plot', 'value': 'scattermap'},{'label': 'Heatmap Plot', 'value': 'heatmap'}

option3={'label': 'Scatter Animation', 'value': 'scatterA'},{'label': 'Line Animation', 'value': 'lineA'}

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
)

app = dash.Dash(__name__, title="Graphgen", external_stylesheets=[url_theme1, dbc_css])
server=app.server

color_list=['blue','red','black','yellow','green','orange','brown','white']
card_user=dbc.Card([
    dbc.CardHeader(html.H5("Data User", className="card-title"),),
    html.Div("kosong",id="node_detail"),
    ],className="mt-3",
)

card_tweet=dbc.Card([
    dbc.CardHeader(html.H5("Data interaksi", className="card-title "),className="bg-primary"),
  
    html.Div("kosong",id="edge_detail"),

],inverse=True)
summary=dbc.Card([
    dbc.CardHeader(html.H5("Rangkuman Data", className="card-title"),),
    dbc.CardBody(
        [
        ],id="rangkuman_data"
    ),
    ],className="mt-3",
)
tab1_content = dbc.Card([
    dbc.CardHeader(html.H5("Upload Data Disini", className="card-title"),),
    dbc.CardBody([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
            ),
        ])
    ],className="mt-3"
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [	
        	dbc.Row([
        		dbc.Col(
                    [
                        dbc.Label("Jenis Graph"),
                        dcc.Dropdown(
                            id="group-variable",
                            options=[
                               {'label': 'Basic Chart', 'value': 'basic'},
                               {'label': 'Mapping Chart', 'value': 'map'},
                               #{'label': 'Animation', 'value': 'animation'},
                           ],
                            className="dash-bootstrap",
                            value='basic'
                        ),
                    ],md=4
                ),
        	]),
        	html.Hr(),
            dbc.Row([
                
                dbc.Col(
                    [
                        dbc.Label("Tipe Graph"),
                        dcc.Dropdown(
                            id="graph-variable",
                            options=[
                               {'label': 'Scatter Chart', 'value': 'scatter'},
                               {'label': 'Line Chart', 'value': 'line'},
                               {'label': 'Bar Chart', 'value': 'bar'},
                               {'label': 'Pie Chart', 'value': 'pie'},
                               {'label': 'Box Chart', 'value': 'box'},
                               {'label': 'Histogram Chart', 'value': 'hist'},
                           ],
                           className="dash-bootstrap",
                           value='scatter'
                        ),
                    ],md=4
                ),
                dbc.Col(
                    [
                        dbc.Label("Warna"),
                        dcc.Dropdown(
                            id="color-variable",   
                            options=[
                               {'label': 'Default', 'value': 'Plotly'},
                               {'label': 'Pastel', 'value': 'Pastel'},
                               {'label': 'Dark', 'value': 'Prism'},
                               {'label': 'Vivid', 'value': 'Vivid'},
                           ],
                           className="dash-bootstrap", 
                           value='Plotly'
                        ),
                    ],md=4
                ),
                
                ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Label("X variable",id="x-name"),
                        dcc.Dropdown(
                            id="x-variable",
                            className="dash-bootstrap",
                        ),
                        dbc.Checkbox(
                            id="checkbox",
                            label="Hitung kolomnya",
                            value=False,
                        ),

                    ],md=4
                ),
                dbc.Col(
                    [
                        dbc.Label("Y variable",id="y-name"),
                        dcc.Dropdown(
                            id="y-variable", 
                            className="dash-bootstrap",   
                            multi = True,
                        ),
                        dbc.Checkbox(
                            id="checkbox2",
                            label="Grup kesamping",
                            value=False,
                        ),
                        
                    ],md=4
                ),
                dbc.Col(
                    [
                        dbc.Label("Z variable"),
                        dcc.Dropdown(
                            id="z-variable",
                            className="dash-bootstrap",
                        ),
                    ],md=4
                ),
                ]),
            html.Hr(),
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Label("Kelas/Kategori"),
                        dcc.Dropdown(
                            id="category-variable",
                            className="dash-bootstrap",
                        ),
                    ],md=4
                ),
            ]),
        ]
    ),
    className="mt-3"
)

card = dbc.Card(
    [
        dbc.CardBody(
            dbc.Tabs(
                [
                    dbc.Tab(tab2_content,label="Konfigurasi Chart", tab_id="tab-2"),
                ],
                id="card-tabs",
                active_tab="tab-2",
            )
        ),
    ]
)


app.layout = html.Div([
    dbc.Row(
        html.H2("Graph Builder",className="text-center bg-primary text-white p-2",)
    ),
    ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2],),
    dbc.Row([
        dbc.Col([
            tab1_content,
            card,
            
        ],lg=4,width=12),
        dbc.Col([
            
            dbc.Row(dcc.Loading(dcc.Graph(id="cluster-graph"), type="cube")),
            dbc.Row([
            

            ]),
        ],lg=8,width=12),
    ]),
    html.Hr(),
    dbc.Row([
        dcc.Loading(type="dot",id='output-data-upload')
        ])
    
])



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' or 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        dash_table.DataTable(
            id="temp_table",
            style_cell={'textAlign': 'left'},
            columns=[{"name": i, "id": i,
                      'deletable': True,
                      'renamable': True} for i in df.columns],
            data=df.to_dict("records"),
            style_table={'overflowX': 'auto'},
            page_size=20,
            page_action="native",

        ),
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



@app.callback(
    Output("x-variable", "placeholder"),
    Output("x-variable", "disabled"),
    Output("y-variable", "disabled"),
    Output("z-variable", "disabled"),
    Output("checkbox", "style"),
    Output("checkbox2", "style"),
    [
        Input("graph-variable", "value"),
        Input("checkbox", "value"),

    ],
)
def disable_list(x,y):
    if x == "scatter":
        return "None",False,False,False,{'display': 'none'},{'display': 'none'}
    elif y:
        return dash.no_update,False,True,True,{'visibility': 'visible'},dash.no_update
    elif x == "line":
        return "Harus berupa waktu",False,False,True,{'visibility': 'visible'},{'visibility': 'hidden'}
    elif x == "bar":
        return "None",False,False,True,{'visibility': 'visible'},{'visibility': 'visible'}
    elif x == "box":
        return "None",False,False,True,{'display': 'none'},{'display': 'none'}
    elif x == "scattermap":
        return "None",False,False,True,{'display': 'none'},{'display': 'none'}
    elif x == "pie":
        return "Harus berupa angka",False,True,True,{'display': 'none'},{'display': 'none'}
    elif x == "hist":
        return "None",False,True,True,{'display': 'none'},{'display': 'none'}
    else:
        dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,

@app.callback(
    Output("graph-variable", "options"),
    Output("x-name", "children"),
    Output("y-name", "children"),
    [
        Input("group-variable", "value"),

    ],
)
def change_graph_list(x):
    if x == "basic":
        return option1,"X variable","Y variable"
    elif x == "map":
        return option2,'Latitude',"Longtitude"
    elif x == "animation":
        return option3,"X variable","Y variable"
    


@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("graph-variable", "value"),
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("z-variable", "value"),
        Input("category-variable", "value"),
        Input("color-variable", "value"),
        Input('temp_table', 'data'),
        Input('temp_table', 'columns'),
        Input("checkbox", "value"),
        Input("checkbox2", "value"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    ],
)
def make_graph(graph,x,y,z,category,color,data,cols,checkbox,checkbox2,toggle):
    # minimal input validation, make sure there's at least one cluster
    df = pd.DataFrame(data, columns=[c['name'] for c in cols])
    template = template_theme1 if toggle else template_theme2
    mapbox= "carto-positron"if toggle else 'carto-dark'
    warna1 = color_list
    warna2="plotly3"
    if color =="Default":
        warna1 = px.colors.qualitative.Plotly;
        warna2 ="plotly3"
    elif color == "Pastel":
        warna1 = px.colors.qualitative.Pastel;
        warna2 ="tealgrn"
    elif color == "Prism":
        warna1 = px.colors.qualitative.Prism;
        warna2 ="jet"
    elif color == "Vivid":
        warna1 = px.colors.qualitative.Vivid;
        warna2 ="magma"
    if category == None:
        colour=None
    else:
        colour=category
    fig = None
    if graph == "scatter":
        if z== None:
            fig= px.scatter(
                df, x=x, y=y,color=colour, 
                render_mode="webgl", height = 800,template=template,
                color_discrete_sequence=warna1,color_continuous_scale=warna2
            )
            fig.update_traces(marker_size=10)
            fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False)
        else:
            fig= px.scatter_3d(
                df, x=x, y=y,z=z,color=colour,height = 800,template=template,
                color_discrete_sequence=warna1,color_continuous_scale=warna2,
            )
            fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False)
    elif graph =="line":
        if checkbox:
            if category != None:
                df_temp = df.groupby([x,category]).count()
                df_temp['counts'] = df_temp[df_temp.columns[0]]
                df=df_temp.reset_index()
            else:
                df_temp = df.groupby([x]).count()
                df_temp['counts'] = df_temp[df_temp.columns[0]]
                df=df_temp.reset_index()
            fig= px.line(
                df, x=x, y="counts",color=colour, 
                render_mode="webgl", height = 600,
                color_discrete_sequence=warna1,template=template,
            )
        else:
            fig= px.line(
                    df, x=x, y=y,color=colour, 
                    render_mode="webgl", height = 800,
                    color_discrete_sequence=warna1,template=template,
                )
    elif graph == "bar":
        if checkbox:
            if category != None:
                df_temp = df.groupby([x,category]).count()
                df_temp['counts'] = df_temp[df_temp.columns[0]]
                df=df_temp.reset_index()
            else:
                df_temp = df.groupby([x]).count()
                df_temp['counts'] = df_temp[df_temp.columns[0]]
                df=df_temp.reset_index()
            fig= px.bar(
                df, x=x, y="counts",color=colour,height = 800,
                color_discrete_sequence=warna1,template=template,
            )
        else:
            fig= px.bar(
                    df, x=x, y=y,color=colour, height = 800,
                    color_discrete_sequence=warna1,template=template,
                )
        if checkbox2:
            fig.update_layout(barmode='group')
    elif graph == "box":
        fig= px.box(
                df, x=x, y=y,color=colour,  height = 800,
                color_discrete_sequence=warna1,template=template,
            )
    elif graph == "pie":
        if x==None:
            df_temp = df.groupby([colour]).count()
            df_temp['counts'] = df_temp[df_temp.columns[0]]
            df=df_temp.reset_index()
            fig= px.pie(
                    df, values="counts",names=colour,  height = 800,
                    color_discrete_sequence=warna1,template=template,
                )
        else:
            fig= px.pie(
                    df, values=x,names=colour,  height = 800,
                    color_discrete_sequence=warna1,template=template,
                )
    elif graph == "hist":
        fig= px.histogram(
                df, x=x,color=colour,  height = 800,
                color_discrete_sequence=warna1,template=template,
            )
    elif graph == "scattermap":
        fig = px.scatter_mapbox(df, lat=x, lon=y, color=colour,height = 800,color_discrete_sequence=warna1,color_continuous_scale=warna2, zoom=3)
        fig.update_layout(mapbox_style=mapbox)
    elif graph == "heatmap" and z != None:
        fig = px.density_mapbox(df, lat=x, lon=y, z=z, radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style=mapbox)
    else:
        fig = dash.no_update
    return fig



# make sure that x and y values can't be the same variable
def filter_ilang(col,x,y,z):
    if col == x:
        return True
    elif col == y:
        return True
    elif col == z:
        return True
    else:
        return False
    
def filter_options(x,y,z,data,cols):
    """Disable option v"""
    df = pd.DataFrame(data, columns=[c['name'] for c in cols])
    return [
       {"label": col, "value": col, "disabled": filter_ilang(col,x,y,z)}
        for col in df
    ]



app.callback(Output("x-variable", "options"), 
             [Input("y-variable", "value"),
             Input("category-variable", "value"),
              Input("z-variable", "value"), 
              Input('temp_table', 'data'),
        Input('temp_table', 'columns')])(
    filter_options
)
app.callback(Output("z-variable", "options"), 
             [Input("y-variable", "value"),
             Input("category-variable", "value"),
              Input("x-variable", "value"), 
              Input('temp_table', 'data'),
        Input('temp_table', 'columns')])(
    filter_options
)
app.callback(Output("y-variable", "options"), 
             [Input("z-variable", "value"),
             Input("category-variable", "value"),
              Input("x-variable", "value"), 
              Input('temp_table', 'data'),
        Input('temp_table', 'columns')])(
    filter_options
)

app.callback(Output("category-variable", "options"), 
             [Input("z-variable", "value"),
             Input("y-variable", "value"),
              Input("x-variable", "value"), 
              Input('temp_table', 'data'),
        Input('temp_table', 'columns')])(
    filter_options
)        
if __name__ == '__main__':
    app.run_server(debug=True)



