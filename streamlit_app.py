import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pandasql as pdsql
import requests
import streamlit as st

# get profile from query params
# query_params = st.experimental_get_query_params()

# profile = query_params['id_alumno'][0] if 'id_alumno' in query_params else 'A0'

# add credentials to the account
keyfile_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
database = client.open('club_fiction')

# movies
movies_table = database.get_worksheet(1)
movies_df = pd.DataFrame(movies_table.get_all_records())
st.set_page_config(layout="wide")
st.markdown('## Club fiction')

movie_df = pdsql.sqldf(
    f'''
    select 
        fecha_limite,
        poster_url,
        pelicula,
        año,
        CC,
        recomendador,
        plataforma,
        Adrián,
        Alonso,
        Ana,
        Mamen,
        (Adrián + Alonso + Ana + Mamen) / 4 as media
    from movies_df
    where nr != '' and pelicula != ''
    '''
)
    
# cols = st.columns(12)
# cols[0].markdown('**Fecha**')
# cols[1].markdown('**Poster**')
# cols[2].markdown('**Título**')
# cols[3].markdown('**Año**')
# cols[4].markdown('**País**')
# cols[5].markdown('**Recomendador**')
# cols[6].markdown('**Plataforma**')
# cols[7].markdown('**ADRIÁN**')
# cols[8].markdown('**ALONSO**')
# cols[9].markdown('**ANA**')
# cols[10].markdown('**MAMEN**')
# cols[11].markdown('**MEDIA**')

for movie in movie_df.values:
    movie_details = list(movie)

    cols = st.columns(11)
    cols[0].markdown(f'**{movie_details[2]}**')
    response = requests.get(movie_details[1])
    cols[1].image(response.content, use_column_width='auto')
    cols[2].markdown(f'**Fecha review:** {movie_details[0]}')
    cols[3].write(f'**Año:** {movie_details[3]}')
    response = requests.get(f'https://countryflagsapi.com/png/{movie_details[4].lower()}')
    cols[4].image(response.content, width=30)
    cols[5].write(f'**Recomendador:** {movie_details[5]}')
    try:
        cols[6].write(int(movie_details[7]) / 100)
        cols[7].write(int(movie_details[8]) / 100)
        cols[8].write(int(movie_details[9]) / 100)
        cols[9].write(int(movie_details[10]) / 100)
        cols[10].write(int(movie_details[11]) / 100)
    except:
        pass
    