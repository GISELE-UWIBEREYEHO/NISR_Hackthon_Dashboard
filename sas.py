import dash 
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import pandas as pd
external_stylesheets = ['assets/styles.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# importing data I will use from Excel to Python and i created new column
df = pd.read_excel("C:\\Users\\educa\\Desktop\\Hackthon sheet.xlsx", sheet_name="Table1", header=2)
notincluded=['Unnamed: 0','Seasonal', 'years']
newcol =[col for col in df.columns if col not in notincluded]
 
df1 = pd.read_excel("C:\\Users\\educa\\Desktop\\Hackthon sheet.xlsx", sheet_name="Table2", header=2)
df1.columns = df1.columns.str.strip()
notincluded1=['Unnamed: 0','seasons','years']
newcol1=[col for col in df1.columns if col not in notincluded1]


df2 = pd.read_excel("C:\\Users\\educa\\Desktop\\Hackthon sheet.xlsx", sheet_name="Table3", header=2)
notincluded2=['Unnamed: 0','Seasonal','years']
newcol2=[col for col in df2.columns if col not in notincluded2]
df3 = pd.read_excel("C:\\Users\\educa\\Desktop\\Hackthon sheet.xlsx", sheet_name="Table5", header=1)

df4 = pd.read_excel("C:\\Users\\educa\\Desktop\\Hackthon sheet.xlsx", sheet_name="Table4", header=2)
notincluded4=['Unnamed: 0','Seasonal','years']
newcol4=[col for col in df4.columns if col not in notincluded4]

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='SEASON AGRICULTURAL SURVEY', style={'textAlign': 'center'}),
    
    html.Div([
    
        html.Div([
            html.Div([
                html.Div([
                    # 1st indicator of seasonal Agricultural Survey layout
                    html.P('AGRICULTURE AREA'),
                    dcc.Dropdown(id="agricultural_area", style={'width': '450px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                                 options=[{'label': col, 'value': col} for col in newcol],
                                 value="Agriculture land (,000Ha)"
                                 ),
                    dcc.Graph(id='graph-with-season', style={'width': '450px', 'height': '300px', 'textAlign': 'center'}),
                ], className='graph-container'),
                html.Div([
                    # 2nd  indicator of agricultural area layout
                    html.P('AGRICULTURE INPUTS'),
                    dcc.Dropdown(id="agricultural_input", style={'width': '450px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                                 options=[{'label': col, 'value': col} for col in newcol1],
                                 value='Percentage of plots with improved seeds'
                                 ),
                    dcc.Graph(id='graph-with-seasons', style={'width': '450px', 'height': '300px'})
                ], className='graph-container')
            ], className='graph-container-wrapper'),

            html.Div([
                html.Div([
                    # 3rd indicator of agricultural area layout
                    html.P('CULTIVATED AREA'),
                    dcc.Dropdown(id="cultivated_area", style={'width': '450px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                                 options=[{'label': col, 'value': col} for col in newcol2
                                         ],
                                 value="Percentage of area by Pure cropping system"
                                 ),
                    dcc.Graph(id='graph-with-seasonal', style={'width': '450px', 'height': '300px'}),
                ], className='graph-container'),
                html.Div([
                    # 4th indicator of agricultural area layout
                    html.P('AGRICULTURE PRACTICE'),
                    dcc.Dropdown(id="Agriculture_practise", style={'width': '450px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                                 options=[{'label': col, 'value': col} for col in newcol4],
                                 value="Percentage of farmers who practiced irrigation"
                                 ),
                    dcc.Graph(id='graph-with-seasonals', style={'width': '450px', 'height': '300px', 'align': 'right'})
                ], className='graph-container-second-row')
            ], className='graph-container-second-row-wrapper'),
            # the added value of source of improved seeds

            html.P('SOURCE OF IMPROVED SEEDS'),
            dcc.RadioItems(
                id='season-radio',
                options=[
                    {'label': 'Season A', 'value': 'Season_A'},
                    {'label': 'Season B', 'value': 'Season_B'},
                    {'label': 'Season C', 'value': 'Season_C'}
                ],
                value='Season_A',
                labelStyle={'display': 'block'}
            ),
            html.Div([
                dcc.Dropdown(
                    id='year-dropdown', style={'width': '250px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                    options=[
                        {'label': '2021', 'value': '2021'},
                        {'label': '2022', 'value': '2022'}
                    ],
                    value='2021',
                    placeholder='select a year'
                ),
                dcc.Dropdown(
                    id='source-dropdown', style={'width': '450px', 'height': '50px','backgroundColor': 'white', 'color': 'black'},
                    options=[{'label': source, 'value': source} for source in df3['Source']],
                    multi=True,
                    value=['NGOs/Companies']
                ),
            ], style={'display': 'inline-block', 'display': 'flex'}),
            dcc.Graph(id='bar-chart', style={'width': '700px', 'height': '400px'})
        ], style={'width': '80%', 'display': 'inline-block', 'float': 'right'}),  # Set the width of the right column

        # Left Column (Years Dropdown)
        html.Div([
            html.P('Select year'),
        
            dcc.Dropdown(
                id='years-dropdown',style={'width': '80%','backgroundColor': 'white', 'color': 'black'},
                options=[{'label': str(year), 'value': year} for year in df['years'].unique()],
                value=df['years'].min()
            
            ),
        ], style={'width': '20%', 'display': 'inline-block'}),  # Set the width of the left column
    ]),
], style={'background_color': 'black'})


 # the callback of Agricultural area
@app.callback(
    Output('graph-with-season', 'figure'),
    [Input('years-dropdown', 'value'),
     Input('agricultural_area', 'value')]
)
def update_figure(selected_years, drop):
    filtered_df = df[df['years'] == selected_years]

    fig1 = px.bar(filtered_df, x="Seasonal", y=drop, color="Seasonal", color_discrete_sequence=['green', 'blue'],
                  labels={'Seasonal': 'Seasonal', f'{drop}': drop})
    fig1.update_layout(
        plot_bgcolor='black',  
        paper_bgcolor='black', 
        font=dict(color='white'))  

    fig1.update_layout(transition_duration=600)

    return fig1

# the callback of Agricultural input
@app.callback(
    Output('graph-with-seasons', 'figure'),
    [Input('years-dropdown', 'value'),
     Input('agricultural_input', 'value')]
)
def update_figure(selected_years, dropdown):
    filtered_df1 = df1[df1['years'] == selected_years]

    fig = px.bar(filtered_df1, x="seasons", y=f"{dropdown}", color="seasons", color_discrete_sequence=['green', 'blue', 'orange'])
    fig.update_layout(
    plot_bgcolor='black', 
    paper_bgcolor='black',  
    font=dict(color='white') ) 
    fig.update_layout(transition_duration=600)

    return fig

# the callback of agricultural cropping area
@app.callback(
    Output('graph-with-seasonal', 'figure'),
    [Input('years-dropdown', 'value'),
     Input('cultivated_area', 'value')]
)
def update_figure(selected_years, droping):
    filtered_df2 = df2[df2['years'] == selected_years]

    fig3 = px.pie(filtered_df2, names="Seasonal", values=f"{droping}", hole=0.4, color="Seasonal",
                  color_discrete_sequence=['skyblue', 'blue', 'orange'])
    fig3.update_layout(
        plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot area color to black
        font=dict(color='white') ) # Set text color to white

    fig3.update_layout(transition_duration=600)

    return fig3

# the callback of Agricultural practise
@app.callback(
    Output('graph-with-seasonals', 'figure'),
    [Input('years-dropdown', 'value'),
     Input('Agriculture_practise', 'value')]
)
def update_figure(selected_years, dropping):
    filtered_df4 = df4[df4['years'] == selected_years]

    column_name = None
    for col in filtered_df4.columns:
        if dropping in col:
            column_name = col
            break

    if column_name is None:
        raise ValueError(f"Column related to '{dropping}' not found in the DataFrame.")

    fig4 = px.histogram(filtered_df4, x=column_name, y="Seasonal", color="Seasonal",
                        color_discrete_sequence=['skyblue', 'blue', 'green'])
    fig4.update_layout(
        plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot area color to black
        font=dict(color='white'))  # Set text color to white

    fig4.update_layout(transition_duration=600)

    return fig4

# the callback of source of improved seed

@app.callback(
    Output('bar-chart', 'figure'),
    Input('season-radio', 'value'),
    Input('year-dropdown', 'value'),
    Input('source-dropdown', 'value')
)
def update_bar_chart(season, year, selected_sources):
    
    # Create a slice of the DataFrame based on selected year and season
    filtered_df3 = df3[['Source', f'{year}_{season}']]
    filtered_df3 = filtered_df3[filtered_df3['Source'].isin(selected_sources)]

    # Create a bar chart using Plotly Express
    
    fig5 = px.bar(filtered_df3, x='Source', y=f'{year}_{season}', text=f'{year}_{season}',
                 color='Source', color_discrete_sequence=px.colors.qualitative.Dark24,
                 labels={'Source': 'Source', f'{year}_{season}': 'Value'})
    fig5.update_layout(
        plot_bgcolor='black',  # Set background color to black
        paper_bgcolor='black',  # Set plot area color to black
        font=dict(color='white') ) # Set text color to white

    fig5.update_layout(transition_duration=500)

    return fig5
   

if __name__ == '__main__':
    app.run(debug=True,port=8065)
