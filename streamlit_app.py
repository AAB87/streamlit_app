import gspread
import json
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import pandasql as pdsql
import requests
import streamlit as st

# get profile from query params
query_params = st.experimental_get_query_params()

profile = query_params['id_alumno'][0] if 'id_alumno' in query_params else 'A0'

# add credentials to the account
keyfile_dict = json.loads(st.secrets["GCP_SERVICE_ACCOUNT"])

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
database = client.open('josemanuel_app_database')

# students
students_table = database.get_worksheet(0)
students_df = pd.DataFrame(students_table.get_all_records()).iloc[: , :6]

# experience actions
experience_actions_table = database.get_worksheet(1)
experience_actions_df = pd.DataFrame(experience_actions_table.get_all_records()).iloc[: , :3]

# mts
mts_table = database.get_worksheet(2)
mts_df = pd.DataFrame(mts_table.get_all_records()).iloc[: , :3]

# pokedex
pokedex_table = database.get_worksheet(3)
pokedex_df = pd.DataFrame(pokedex_table.get_all_records()).iloc[: , :4]

# students experience actions
students_experience_actions_table = database.get_worksheet(4)
students_experience_actions_df = pd.DataFrame(students_experience_actions_table.get_all_records()).iloc[: , :3]

# students mts
students_mts_table = database.get_worksheet(5)
students_mts_df = pd.DataFrame(students_mts_table.get_all_records()).iloc[: , :2]

# students pokedex
students_pokedex_table = database.get_worksheet(6)
students_pokedex_df = pd.DataFrame(students_pokedex_table.get_all_records()).iloc[: , :2]

# Student details
if profile == 'A0':
    st.write('Perfil profe')

    # query = '''
    # select *
    # from students_df
    # left join students_experience_actions_df
    # using(id_alumno)
    # left join pokedex_df 
    # using(id_pokemon)
    # '''

else:
    ID_ALUMNO = profile

    try:
        student_df = pdsql.sqldf(
            f'''
            select * 
            from students_df 
            where id_alumno = "{ID_ALUMNO}"
            '''
        )
        student_course = list(student_df.values[0])[1]
        student_course_letter = list(student_df.values[0])[2]
        student_name = list(student_df.values[0])[3]
        student_surname = list(student_df.values[0])[4]
        student_initial_points = list(student_df.values[0])[5]

        student_pokemon_df = pdsql.sqldf(
            f'''
            select * 
            from students_pokedex_df 
            left join pokedex_df 
            using(id_pokemon) 
            where id_alumno = "{ID_ALUMNO}"
            '''
        )
        student_pokemon = list(student_pokemon_df.values[0])[3]
        student_pokemon_picture = list(student_pokemon_df.values[0])[4]

        student_experience_actions_df = pdsql.sqldf(
            f'''
            select * 
            from students_experience_actions_df 
            where id_alumno = "{ID_ALUMNO}"
            '''
        )

        student_points = list(pdsql.sqldf(
            f'''
            select sum(puntos_experiencia_accion) 
            from student_experience_actions_df 
            left join experience_actions_df 
            using(id_accion) 
            where id_alumno = "{ID_ALUMNO}"
            '''
        ).values[0])[0]

        student_total_points = student_initial_points + student_points

        # st.write(f'''
        # {student_course}, 
        # {student_course_letter}, 
        # {student_name}, 
        # {student_surname}, 
        # {student_initial_points}, 
        # {student_points}, 
        # {student_total_points},
        # {student_pokemon},
        # {student_pokemon_picture}
        # ''')

        html = f'''
        <html>

        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
        * {{box-sizing: border-box}}

        .container {{
        width: 100%;
        background-color: #ddd;
        }}

        .skills {{
        text-align: right;
        padding-top: 10px;
        padding-bottom: 10px;
        color: white;
        }}

        .bold {{ 
        font-weight: bold; 
        font-size:1em; 
        text-align:right; 
        }} 
        .button {{ 
        text-align:center; 
        }}

        .experiencia {{width: {student_total_points}; background-color: #04AA6D;}}

        .image {{
        height: 250px;
        width: auto;
        }}

        .image-container {{
        text-align: center;
        }}
        </style>

        </head>


        <body>
        <br> 
        Alumno: {student_name} {student_surname}
        <br> 
        <br>
        Curso: {student_course} {student_course_letter}
        <br>
        <br>
        Pokemon:
        <div class="image-container">
        <img src={student_pokemon_picture} class="image"/>
        </div>
        <p>Experiencia:</p>
        <div class="container">
        <div class="skills experiencia">{student_total_points}</div>
        </div>
        <br> 
        Medallas:
        <br> 
        <br>

        </body>

        </html>
        '''
        st.markdown(html, unsafe_allow_html=True)
    
    except:
        st.write('En desarrollo, gracias por su paciencia')
