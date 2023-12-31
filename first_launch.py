import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import io
import base64
import datetime
import dash_bootstrap_components as dbc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = dash.Dash(external_stylesheets=[dbc.themes.LUMEN])#, suppress_callback_exceptions=True)

server = app.server

# Define the layout of the app
app.layout = html.Div(children = 
[
    # page title
    dbc.Row([
        dbc.Col([]),
        dbc.Col([html.H1("Clevered HR Dashboard", className="fw-bold text-decoration-underline", style={'color': 'black'})]),
        dbc.Col([html.A(dbc.Button('Refresh', color="warning"),href='/', className="d-md-flex justify-content-md-end", style={"text-decoration": "none"})])
    
    ]),
    html.Br(),

    # department radio buttons
    html.Div([
        dbc.Label("Select Department", className = "text-black fw-bold"),
        dbc.RadioItems(
            options=[
                {"label": "Sales", "value": 0},
                {"label": "IT", "value": 1},
                {"label": "Marketing", "value": 2},
                {"label": "Support", "value": 3},
                {"label": "Partnership", "value": 4},
                {"label": "Trainers", "value": 5},
                {"label": "Freelancers", "value": 6},
                {"label": "Internship", "value": 7},
            ],
            value=0,
            id="radioitems-input",
            inline = True,
            className = "text-black"
        ),
    ]
),        
    html.Br(),  
    
    # file upload container                                                   
    html.Div(id='upload-container', className='centered-container', children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([html.A('Select .xlsx File')], style={'color': 'black'}),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px auto',  # Center horizontally
                },
                multiple=False,
            ),
        ]),
    html.Br(),

    # month and name dropdowns
    html.Div([  dbc.Select( id='month-dropdown',options=[{'label': 'January', 'value': '01'},
                                                         {'label': 'February', 'value': '02'},
                                                         {'label': 'March', 'value': '03'},
                                                         {'label': 'April', 'value': '04'},
                                                         {'label': 'May', 'value': '05'},
                                                         {'label': 'June', 'value': '06'},
                                                         {'label': 'July', 'value': '07'},
                                                         {'label': 'August', 'value': '08'},
                                                         {'label': 'September', 'value': '09'},
                                                         {'label': 'October', 'value': '10'},
                                                         {'label': 'November', 'value': '11'},
                                                         {'label': 'December', 'value': '12'},],
                            placeholder='Select a month...',
                            style={'width': '90%', 'margin': '15px'},
                            className="px-2 border"# bg-white rounded-pill"
                        ),
        
                dbc.Select(id='name-dropdown',placeholder='Select a person...',style={'width': '90%', 'margin': '15px'},
                            className="px-2 bg-white border"# rounded-pill"
                        ),
    ], style={'display': 'flex'}), 

    html.Br(),

    # manual search bar with search and clear buttons
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Input(id='manual-search-input', type='text', placeholder='Enter a name to get details...'),
                dbc.ButtonGroup([
                    dbc.Button('Search', id='manual-search-button', n_clicks=0, className = "text-center", color = "success"),
                    dbc.Button('Clear', id = 'clear-button', n_clicks = 0, className = "text-center", color = "danger")])],
                    style = {'display':'flex'}),
            ]),
        dbc.Col([
            html.Div([
                dbc.Input(id='sender_password_input', type='password', placeholder='Enter your password...'), 
                dbc.Button('Send Mail', id = 'send_info_mail', n_clicks = 0, color="warning", className = 'text-center', style={'width': '150px'})],
                style = {'display':'flex'}),#, 'margin': '15px'}),     
            ])
        ]),
             
    # manual search output div
    html.Div(id='output-columns'),
    
    html.Div(id='output-person-info', style={'color': 'black'}),
    
    # current month info div
    html.Div(id='current-month-info', style={'color': 'black'}),#, className = 'text-dark'),  

    # email status div
    html.Div(id='current-month-bday-anni-info'),

],style={
        'background': 'linear-gradient(360deg, #FF5733, #FFC300)',  
        'height': '200vh',  
        'color': 'white',  
        'padding': '30px',
    })


# Function to get current month
def get_current_month():
    now = datetime.datetime.now()
    return now.strftime('%m')

#Function to get current date for bday/anni mail personalisation
def get_current_date():
    now = datetime.datetime.now()
    return now.strftime('%d')

# Function to extract month
# def extract_month(date_str):
#     try:
#         date_str = date_str.strftime('%d%m%Y')  # Convert the datetime object to a string
#         date = datetime.datetime.strptime(date_str, '%d%m%Y')
#         return date.month
#     except ValueError:
#         return None
# def extract_month(date_str):
#     try:
#         day, month, year = map(int, date_str.split('/'))
#         return month
#     except (ValueError, AttributeError):
#         return None
    
def read_file(contents, filename, Sheet):
    if contents is None:
        return ''
    content_type, content_string = contents.split(',')
    file_extension = filename.split('.')[-1].lower()

    if file_extension == 'xlsx':
        decoded = io.BytesIO(base64.b64decode(content_string))
        df = pd.read_excel(decoded, engine='openpyxl', sheet_name =Sheet)
        # print(df)
    else:
        raise ValueError(f"Unsupported File Format: {file_extension}")

    
    # df['date of birth'] = pd.to_datetime(df['date of birth'], format='%d/%m/%Y', dayfirst=True)
    # df['date of joining'] = pd.to_datetime(df['date of joining'], format='%d/%m/%Y', dayfirst=True)

    # df['date of birth'] = df['date of birth'].apply(extract_month)
    # df['date of joining'] = df['date of joining'].apply(extract_month)
    # df['date of birth'] = df['date of birth'].str.split('/').str[1].astype(int)
    # df['date of joining'] = df['date of joining'].str.split('/').str[1].astype(int)
    # df['date of birth'] = pd.to_datetime(df['date of birth'], format='%d/%m/%Y').dt.month
    # df['date of joining'] = pd.to_datetime(df['date of joining'], format='%d/%m/%Y').dt.month

    df['birth_month'] = df['date of birth'].dt.month # extract birth month from sheet
    df['joining_month'] = df['date of joining'].dt.month    
    # print("--------------------------------------------------------print all heads---------------------------------------------------------------")
    # print(df.head())
    

    # print("----------------------------------------------------print all datatypes-------------------------------------------------------------")
    # print(df.dtypes)
    return df                         

# Function to send an email
def send_email(sender_email, password, recv_email, subject, message):

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recv_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        server1 = smtplib.SMTP("smtp.gmail.com", 587)
        server1.starttls()
        login_result = server1.login(sender_email, password)
        #print("login successful")

        if login_result[0] == 235:  # Check if login was successful -> 235 is the code for successful login
            server1.sendmail(sender_email, recv_email, msg.as_string())
            server1.quit()
            return 1
        else:
            return 'Error: Incorrect password or authentication failed.'
        
    except smtplib.SMTPException as e:
        return f"Error: Unable to send email - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"


# Function with personalised email body
def email_body(bdays_today, annis_today):   
    body = ''  
    if bdays_today is not None and not bdays_today.empty:   
        body += "The following employees have their Birthdays today: \n"  
        for _, row in bdays_today.iterrows():
            today_name_b = row['name']
            today_email_b = row['email ID']
            body += f"- {today_name_b} : {today_email_b}\n"

    if annis_today is not None and not annis_today.empty:  
        body += "\nThe following employees have their Work Anniversaries today: \n"
        for _, row in annis_today.iterrows():
            today_name_a = row['name']
            today_email_a = row['email ID']
            body += f"- {today_name_a} : {today_email_a}\n"
    return body


#callback to display persons with DOB or DOJ in the current month
@app.callback(
    Output('current-month-info', 'children'), 
    Input('upload-data', 'contents'),
    Input('radioitems-input', 'value'),
    State('upload-data', 'filename')
) 
   
def display_current_month_info(contents, dept,  filename):
    if contents is None:
        return ''

    df = read_file(contents, filename, dept)
    #print(df.columns)
    # df['date of birth'] = df['date of birth'].apply(extract_month)
    # df['date of joining'] = df['date of joining'].apply(extract_month)

    current_month = get_current_month()
    birth_month_filter = df['date of birth'].dt.strftime('%m') == current_month  # make a df of records for which birth month = current month 
    joining_month_filter = df['date of joining'].dt.strftime('%m') == current_month

    # birth_month_filter = df['date of birth'] == current_month  
    # joining_month_filter = df['date of joining'] == current_month
    # print(birth_month_filter)
    
    # birth_month_filter = df['date of birth'].dt.month == current_month 
    # joining_month_filter = df['date of joining'].dt.month == current_month 
   
    birth_persons = df[birth_month_filter]
    joining_persons = df[joining_month_filter]

    # initialize empty divs to display details
    birth_person_info_divs = []
    joining_person_info_divs = []


    # for all names in the filtered dataframe, append them to the children component of person_info_div
    for _, row in birth_persons.iterrows():
        person_name = row['name']
        person_info_div = html.Div([
            html.H5(f'Details for {person_name}:')
        ])

        bday_person_email = row['email ID']
        bday_person_dob = row['date of birth']

        person_info_div.children.append(html.P(f'Email ID: {bday_person_email}'))
        person_info_div.children.append(html.P(f'Birth date: {bday_person_dob}'))

        birth_person_info_divs.append(person_info_div)
   
    # similarly for work anniversary
    for _, row in joining_persons.iterrows():
        person_name = row['name']
        person_info_div = html.Div([
            html.H5(f'Details for {person_name}:')
        ])

        anni_person_email = row['email ID']
        anni_person_doj = row['date of joining']

        person_info_div.children.append(html.P(f'Email ID: {anni_person_email}'))
        person_info_div.children.append(html.P(f'Work Anniversary: {anni_person_doj}'))


        joining_person_info_divs.append(person_info_div)

    # add these two divs within current_month_info_div to display in one row on the output window
    current_month_info_div = html.Div([
        html.H2("Current Month Analysis", className="text-center fw-bold"),# fst-italic text-decoration-line-through"),

        html.Div([
            dbc.Row(
                    [
                        dbc.Col(html.Div([html.H4('Birthdays in this month', className = "fst-italic fw-bold"),
                                          html.P(birth_person_info_divs, style={'text-align': 'justify'})])), 
                        dbc.Col(html.Div([html.H4('Work Anniversaries in this month', className = "fst-italic fw-bold"),
                                          html.P(joining_person_info_divs, style={'text-align': 'justify'})])),
                    ]
                ),
            ])])
 
    return current_month_info_div # return this div as output. it gets vreated only when a valid file is updated. else this division does not exist

# combined callback to handle person info display, name dropdown updates, and manual search
@app.callback(
    [
        Output('output-person-info', 'children'),
        Output('name-dropdown', 'options'),
        Output('manual-search-input', 'value'),
    ],
    [
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),  
        Input('radioitems-input', 'value'),      
        Input('name-dropdown', 'value'),
        Input('month-dropdown', 'value'),
        Input('manual-search-button', 'n_clicks'),
        Input('clear-button', 'n_clicks'), 
        State('manual-search-input', 'value'),
    ]
)
def update_person_info(contents, filename, dept, selected_name, selected_month, search_clicks, clear_clicks, manual_search_name):
    if contents is None:
        return '', [], manual_search_name

    df = read_file(contents, filename, dept)
    
    output_person_info = ''
    name_dropdown_options = []

    if selected_month:
        current_month = selected_month

        # filters to get records with bdays and annis in the particular month
        birth_month_filter = df['date of birth'].dt.strftime('%m') == current_month
        joining_month_filter = df['date of joining'].dt.strftime('%m') == current_month

        # join records from both filters
        filtered_persons = df[birth_month_filter | joining_month_filter]

        person_info_divs = []
        # print("-----------------------------------------------------if name in df, print all names--------------------------------------------------")
        # if 'name' in df:
        #     print(df['name'])

        for _, row in filtered_persons.iterrows():
            person_name = row['name']
            #print(person_name)
            person_info_div = html.Div([
                html.H4(f'Details for {person_name}:')
            ])

            for column_name, value in row.items():
                person_info_div.children.append(html.P(f'{column_name}: {value}'))

            person_info_divs.append(person_info_div)
            name_dropdown_options.append({'label': person_name, 'value': person_name})
    
    if selected_name:
        for person_info_div in person_info_divs:
            if person_info_div.children[0].children == f'Details for {selected_name}:':
                output_person_info = person_info_div
                break
    person_info = pd.DataFrame() 

    if search_clicks is not None and search_clicks > 0 and manual_search_name: # if a name is enteres and the search button is clicked
        manual_search_name_components = manual_search_name.split(' ') # se delimiter " " to separate parts of the name and extract the first and last name
        manual_search_name_first = manual_search_name_components[0].lower() # manual_search_name_components[0] gives the first name and .lower90 to convert to lower case for case-insensitive search
        df['name_lower'] = df['name'].str.lower()

        person_info = df[df['name_lower'].str.startswith(manual_search_name_first)].copy() ##create a copy of the original df
        person_info.drop('name_lower', axis = 1, inplace = True) #inplace true for dropping col from the same df and not making a copy of the dataframe with a col dropped. axis = 1 to delete col and not row(axis=0)
        

    if not person_info.empty:
            person_info_dict = person_info.iloc[0].to_dict()
            output_person_info = html.Div([
                html.H4(f'Details for {manual_search_name}:')
            ])

            for column_name, value in person_info_dict.items():
                output_person_info.children.append(html.P(f'{column_name}: {value}'))

            name_dropdown_options.append({'label': manual_search_name, 'value': manual_search_name})

    # if clear is pressed, return empty string 
    if clear_clicks is not None and clear_clicks >0:
            manual_search_name = ''

    return output_person_info, name_dropdown_options, manual_search_name

@app.callback(
    Output('current-month-bday-anni-info', 'children'), 
    Input('upload-data', 'contents'),
    Input('radioitems-input', 'value'),
    Input('send_info_mail', 'n_clicks'),
    State('sender_password_input', 'value'),
    State('upload-data', 'filename')
)
def send_bday_anni_info(contents, dept, n_clicks, password, filename):

    # if a file is uploaded and the password is entered and send button is pressed:
    if n_clicks > 0 and contents is not None and password is not None:

        df = read_file(contents, filename, dept)
        
        sender_email = 'sampleid987@gmail.com'
        recipient_email = 'sampleid987@gmail.com'

        current_month = get_current_month()
        current_date = get_current_date()

        birth_month_filter = (df['date of birth'].dt.strftime('%m') == current_month) & (df['date of birth'].dt.strftime('%d') == current_date) # extract employee records that have birthday on the current day
        bdays_today = df[birth_month_filter][['name', 'email ID']] # append to bdays_today if birthday is today

        anni_month_filter = (df['date of joining'].dt.strftime('%m') == current_month) & (df['date of joining'].dt.strftime('%d') == current_date)
        annis_today = df[anni_month_filter][['name', 'email ID']] 

        message = email_body(bdays_today, annis_today) # create customised message
     
        if len(bdays_today) > 0 or len(annis_today) > 0: # check if any employee has bday/anni on the present day
            send_email(sender_email, password, recipient_email, "Birthdays and Work Anniversaries today.", message) # send mail  
            if send_email(sender_email, password, recipient_email, "Birthdays and Work Anniversaries today.", message) == 1:
                return dbc.Alert('Email sent successfully!', color = 'success', style = {'width':'30vw'}) 
            else:
                return dbc.Alert('Error: Incorrect password or authentication failed.', color = 'danger', style = {'width':'30vw'}) 
        else:
            return dbc.Alert('No emails to send.', color = 'danger', style = {'width':'30vw'})   
    
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True, port=8067)