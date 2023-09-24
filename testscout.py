import streamlit as st
import pandas as pd
import datetime
import boto3
from dateutil.relativedelta import relativedelta
import altair as alt
import os
from PIL import Image
from uuid import uuid4
import io
import numpy as np
from datetime import datetime,date
import math
from PIL import ImageOps


translations = {
    "English": {
        "Welcome": "Welcome",
        "Goodbye": "Goodbye",
        "Login": "Login",
        "Username": "Username",
        "Password": "Password",
        "Language": "Language",
        "Invalid credentials": "Invalid credentials",
        "Football Player Scouting - Add Player": "Football Player Scouting - Add Player",
        "Personal Info": "Personal Info",
        "Full Name": "Full Name",
        "Gender": "Gender",
        "Date of Birth": "Date of Birth",
        "Nationality": "Nationality",
        "City/Area": "City/Area",
        "Current Club": "Current Club",
        "Contact Number": "Contact Number",
        "Estimated Value (in $EGP)": "Estimated Value (in $EGP)",
        "Physical Attributes": "Physical Attributes",
        "Height (cm)": "Height (cm)",
        "Weight (kg)": "Weight (kg)",
        "Preferred Foot": "Preferred Foot",
        "Positional Data": "Positional Data",
        "Primary Position": "Primary Position",
        "Positions":"Positions",
        "Secondary Positions": "Secondary Positions",
        "Skills Data": "Skills Data",
        "Evaluation": "Evaluation",
        "General Comments": "General Comments",
        "Strengths": "Strengths",
        "Weaknesses": "Weaknesses",
        "Injury History": "Injury History",
        "Record Date": "Record Date",
        "Add Player": "Add Player",
        "Player successfully added!": "Player successfully added!",
        "City":"City",
        "Age":"Age",
        "Personal Information":"معلومات شخصية",
        "Physical Attributes":"الصفات البدنية",
        "Positional Data":"البيانات الموضعية",
        "Skills Ratings":"تقييمات المهارات",
        "Skills Data":"بيانات المهارات",
        "Squad":"Squad"
    },
    "Arabic": {
        "Welcome": "مرحبا",
        "Goodbye": "وداعا",
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Language": "اللغة",
        "Invalid credentials": "بيانات الاعتماد غير صالحة",
        "Football Player Scouting - Add Player": "إضافة لاعب",
        "Personal Info": "معلومات شخصية",
        "Full Name": "الاسم الكامل",
        "Gender": "نوع",
        "Date of Birth": "تاريخ الميلاد",
        "Nationality": "الجنسية",
        "City/Area": "المدينة / المنطقة",
        "Current Club": "النادي الحالي",
        "Contact Number": "رقم الاتصال",
        "Estimated Value (in $EGP)": "القيمة المقدرة (بالجنيه المصري)",
        "Physical Attributes": "الصفات البدنية",
        "Height (cm)": "الطول (سم)",
        "Weight (kg)": "الوزن (كغ)",
        "Preferred Foot": "القدم المفضلة",
        "Positional Data": "البيانات الموضعية",
        "Primary Position": "الموقع الأساسي",
        "Secondary Positions": "المواقع الثانوية",
        "Skills Data": "بيانات المهارات",
        "Evaluation": "تقييم",
        "General Comments": "تعليقات عامة",
        "Strengths": "نقاط القوة",
        "Positions": "المواقع",
        "Weaknesses": "الضعف",
        "Injury History": "تاريخ الإصابة",
        "Record Date": "تاريخ التسجيل",
        "Add Player": "إضافة لاعب",
        "Save Player":"حفظ اللاعب",
        "Player successfully added!": "تمت إضافة اللاعب بنجاح!",
        "City": "مدينة",
        "Age":"العمر",
        "Personal Information":"معلومات شخصية",
        "Physical":"الصفات البدنية",
        "Physical Attributes":"الصفات البدنية",
        "Positional Data":"البيانات الموضعية",
        "Position":"البيانات الموضعية",
        "Skills Ratings":"تقييمات المهارات",
        "Skills Data":"بيانات المهارات",
        "Add Player": "أضف لاعب",
        "Player Statistics": "إحصائيات اللاعب",
        "Data Summarization": "تلخيص البيانات",
        "Full Table": "الجدول الكامل",
        "Page": "صفحة",
        "Squad": "فريق"

    }
}






AWS_ACCESS_KEY_ID = st.secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = st.secrets['AWS_SECRET_ACCESS_KEY']

# Define S3 bucket details
BUCKET_NAME = "tacticmedia"
CSV_FILE_NAME = "Scouting/players (5).csv"
CSV_FILE_NAME_USERS = "Scouting/credentials.csv"

positions = ['ST', 'RW','LW','CAM','CM','CDM', 'LB', 'RB','CB','GK','[]']
squad=['First Team/الفريق الاول','Youth/القطاع الناشيئن','Women/البنات','']
skills = ['Speed/السرعة', 'Potential/الإمكانية', 'Fitness', 'Ball Control/التحكم بالكرة', 'Dribbling/المراوغة', 'Shot/التسديد', 'Tackling/التدخلات', 'Goalkeeping Skills/مهارات حراسة المرمى', 'Heading/التمرير بالرأس', 'Vision/الرؤية', 'Passing/التمرير']

lgo = Image.open("ra2.png")
lgo = lgo.resize((150,150))
# Authenticate with AWS S3

s3 = boto3.resource("s3",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def get_string(language, english_string):
    if language=='Arabic':
        return translations[language][english_string]
    else: return english_string

def load_user_data():
    try:
        obj = s3.Object(BUCKET_NAME, CSV_FILE_NAME_USERS)
        df = pd.read_csv(obj.get()["Body"], dtype=str)
        # Read data from CSV file into a pandas DataFrame
        

        # Convert DataFrame to dictionary
        credentials = pd.Series(df.password.values, index=df.username).to_dict()
        
        return credentials
    except Exception as e:
        st.write(e)
        return pd.DataFrame()
def get_image(imagelocation):
    try:
        obj = s3.Object(BUCKET_NAME, imagelocation)
        
        image_data = obj.get()['Body'].read()
        return image_data
    except Exception as e:
        
        random_image = Image.fromarray(np.random.randint(0, 256, (150, 200, 3), dtype=np.uint8))

        return random_image

def load_player_data():
    try:
        obj = s3.Object(BUCKET_NAME, CSV_FILE_NAME)
        player_data = pd.read_csv(obj.get()["Body"], dtype=str)
        if 'date_of_birth' in player_data.columns:
            player_data['date_of_birth'] = pd.to_datetime(player_data['date_of_birth'], format="%d/%m/%Y", errors='coerce')
        if 'record_date' in player_data.columns:
            player_data['record_date'] = pd.to_datetime(player_data['record_date'])
        if 'last_modified' in player_data.columns:
            player_data['last_modified'] = pd.to_datetime(player_data['last_modified'])
        #st.write(player_data)
        return player_data
    except Exception as e:
        st.write(e)
        return pd.DataFrame()


def save_player_data(player_data):
    if 'date_of_birth' in player_data.columns:
        player_data['date_of_birth'] = pd.to_datetime(player_data['date_of_birth'])

        player_data['date_of_birth'] = player_data['date_of_birth'].dt.strftime("%d/%m/%Y")
    if 'record_date' in player_data.columns:
        player_data['record_date'] = player_data['record_date'].astype(str)
    if 'last_modified' in player_data.columns:
        player_data['last_modified'] = player_data['last_modified'].astype(str)
    st.write(player_data)
    s3.Object(BUCKET_NAME, CSV_FILE_NAME).put(Body=player_data.to_csv(index=False))

def calculate_age(birth_date):
    birth_date = pd.to_datetime(birth_date, errors='coerce')
    if pd.isnull(birth_date):
        return None
    today = pd.to_datetime('today')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age
def upload_to_s3(image, filename):
    # Initialize the S3 client
    bucket_name =BUCKET_NAME
    s3 = boto3.client('s3')
    filename=  "Scouting/images/"+filename
    # Convert PIL Image to bytes
    image_bytes_arr = io.BytesIO()
    image.save(image_bytes_arr, format='PNG')
    image_bytes = image_bytes_arr.getvalue()
    
    # Upload the image to S3
    try:
        s3.put_object(Body=image_bytes, Bucket=bucket_name, Key=filename)
        print(f"Successfully uploaded {filename} to {bucket_name}")
        
        # Return the S3 key for the uploaded image
        return filename
    except Exception as e:
        print(f"Failed to upload {filename} to {bucket_name}: {e}")
        return None

def login():
    
    with st.form('login_form'):
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
                st.image(lgo)
        credentials = load_user_data()
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if 'language' not in st.session_state:
            st.session_state['language'] = 'English'  # Set a default language
        language_options = ['English', 'Arabic']
        language = st.selectbox('Language', language_options, index=language_options.index(st.session_state['language']))
        st.session_state['language'] = language  # Update the session state
        submit_button = st.form_submit_button('Login')

    if submit_button:
        if credentials.get(username) == password:  # Replace with your actual authentication logic
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()
        else:
            st.error('Invalid credentials')

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    
    login()
else:

    player_data = load_player_data()
    if len(player_data) > 0 and 'date_of_birth' in player_data.columns:
        player_data['date_of_birth'] = pd.to_datetime(player_data['date_of_birth'])
        player_data['age'] = player_data['date_of_birth'].apply(calculate_age)

    st.sidebar.image(lgo)
    pages = ["Add Player/أضف لاعب", "Edit Player/","Player Statistics/إحصائيات اللاعب", "Data Summarization/تلخيص البيانات", "Full Table/الجدول الكامل","Players List/قائمة اللاعبين"]
    page = st.sidebar.selectbox("Page", pages)

    # Add all the required filters
    with st.sidebar.container():
        
        st.header("Filters")
        selected_positions = st.multiselect(get_string(st.session_state['language'],"Positions"), options=positions) if 'primary_position' in player_data.columns else []
        selected_genders = st.multiselect(get_string(st.session_state['language'],"Gender"), options=['Male', 'Female']) if 'gender' in player_data.columns else []
        selected_cities = st.multiselect(get_string(st.session_state['language'],"City"), options=player_data['city_area'].unique().tolist()) if 'city_area' in player_data.columns else []
        
        #selected_age = st.slider("Age", min_value=0, max_value=100, value=(player_data['age'].min(), player_data['age'].max())) if 'age' in player_data.columns else []
        #selected_age = st.slider("Age", min_value=0, max_value=100, step=1, value=(int(player_data['age'].min()), int(player_data['age'].max()))) if 'age' in player_data.columns else []
        min_age = int(player_data['age'].min()) if pd.notnull(player_data['age'].min()) else 0
        max_age = int(player_data['age'].max()) if pd.notnull(player_data['age'].max()) else 100
        selected_age = st.slider(get_string(st.session_state['language'],"Age"), min_value=0, max_value=100, step=1, value=(min_age, max_age)) if 'age' in player_data.columns else []

    # Apply filters
    if len(player_data) > 0:
        filters = (player_data['primary_position'].isin(selected_positions) if selected_positions else True) & \
                (player_data['gender'].isin(selected_genders) if selected_genders else True) & \
                (player_data['city_area'].isin(selected_cities) if selected_cities else True) & \
                (player_data['age'].between(*selected_age) if selected_age else True)
        filtered_data = player_data[filters]
    else:
        filtered_data = None

    if page == "Add Player/أضف لاعب":
        


        st.title(get_string(st.session_state['language'],'Football Player Scouting - Add Player'))

        # Define empty dictionary to hold form inputs
        player = {}
        col1, col2, col3 = st.columns(3)
        
       
        
        # Add this in your Add Player section
        uploaded_image = st.file_uploader("Choose an image.../...اختر صورة", type=["jpg", "png", "jpeg"],key=1)
        if uploaded_image is not None and 'addimage' not in st.session_state:
            # Use PIL to open the image (optional)
            image = Image.open(uploaded_image).resize((150, 200), Image.LANCZOS)
            
            image = ImageOps.exif_transpose(image)
            image = ImageOps.expand(image,border=5,fill='black')
            # Generate a unique filename based on a UUID
            st.session_state['addfilename'] = f"{uuid4().hex}.png"
            # TODO: Add any image manipulation or validation here
            st.session_state['addimage']=image
            
            

        
        if 'addimage' in st.session_state :
            st.image(st.session_state['addimage'])
            if st.button("Remove Image"):
                del st.session_state["addimage"]
                del st.session_state["addfilename"]
            
        with st.expander(get_string(st.session_state['language'],"Personal Info")):
            # Personal Information
            st.subheader(get_string(st.session_state['language'],'Personal Information'))
            player["name"] = st.text_input(get_string(st.session_state['language'],"Full Name"))
            genderoptions = ['Male', 'Female']
            player["gender"] = st.selectbox(get_string(st.session_state['language'],"Gender"), ['Male', 'Female'])
            #default_date = pd.Timestamp(player_row['date_of_birth']).to_pydatetime().date()
            min_date = date(1990, 1, 1)
            player["date_of_birth"] = st.date_input(get_string(st.session_state['language'],"Date of Birth"),min_value = min_date)
            player["nationality"] = st.text_input(get_string(st.session_state['language'],"Nationality"))
            player["city_area"] = st.text_input(get_string(st.session_state['language'],"City/Area"))
            player["current_club"] = st.text_input(get_string(st.session_state['language'],"Current Club"))
            player["contact_number"] = st.text_input(get_string(st.session_state['language'],"Contact Number"))
            player["estimated_value"] = st.number_input(get_string(st.session_state['language'],"Estimated Value (in $EGP)"))
        with st.expander(get_string(st.session_state['language'],"Physical")):
            st.subheader(get_string(st.session_state['language'],'Physical Attributes'))
            player["height"] = st.text_input(get_string(st.session_state['language'],"Height (cm)"))
            player["weight"] = st.text_input(get_string(st.session_state['language'],"Weight (kg)"))
            footoptions = [ 'Right','Left', 'Both']
            player["preferred_foot"] = st.selectbox(get_string(st.session_state['language'],"Preferred Foot"), ['Right','Left', 'Both'])
        with st.expander(get_string(st.session_state['language'],"Position")) :  
            # Positional Data
            st.subheader(get_string(st.session_state['language'],'Positional Data'))
            
            player["primary_position"] = st.selectbox(get_string(st.session_state['language'],"Primary Position"), positions)
            
            #player["secondary_positions"] = st.multiselect(get_string(st.session_state['language'],"Secondary Positions"), positions,default = player_row['secondary_positions']if mode == "Edit Existing Player" else "[]")
            
            selected_squad = st.multiselect(get_string(st.session_state['language'],"Squad"),squad)
            player["Squad"] = '|'.join(selected_squad)
        with st.expander(get_string(st.session_state['language'],"Skills Ratings")):
            # Skill Data
            st.subheader(get_string(st.session_state['language'],'Skills Data'))
            for skill in skills:
                #st.write(player_row[skill])
                player[skill] = st.slider(skill, min_value=0, max_value=10)

            st.subheader(get_string(st.session_state['language'],'Evaluation'))
            player["general_comments"] = st.text_input(get_string(st.session_state['language'],"General Comments"))
            player["strengths"] = st.text_input(get_string(st.session_state['language'],"Strengths"))
            player["weaknesses"] = st.text_input(get_string(st.session_state['language'],"Weaknesses"))
            player["injury"] = st.text_input(get_string(st.session_state['language'],"Injury History"))
            player["record_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Record Date
            player["scouted_by"] = st.session_state['username']

        if st.button(get_string(st.session_state['language'],'Add Player')):
            # Create an empty DataFrame with headers
            # Upload the image to S3 and get the S3 key'
            if player["name"] =="":
                st.error("Player name missing")
            else:
                s3_key = None
                if "addimage" in st.session_state:
                    s3_key = upload_to_s3(st.session_state["addimage"], st.session_state["addfilename"])
                    del st.session_state["addimage"]
                    del st.session_state["addfilename"]
                if s3_key != None:
                    player['image_s3_key'] =s3_key
                    
                    
                    st.success("image uploaded")
                    uploaded_image = None
                else:
                    st.error("No image")
                    uploaded_image = None

           
                player_df = pd.DataFrame([player])
                #st.write(player_df)
                # Append the player DataFrame to the player_data DataFrame
                player_data = pd.concat([player_data, player_df], ignore_index=True)
                
                save_player_data(player_data)
                st.success("Player successfully added!")
        

    
    elif page == "Edit Player/" and len(player_data)>0:
        #st.title(get_string(st.session_state['language'],'Edit Player'))

        # Define empty dictionary to hold form inputs
        player = {}
        
        
        selected_player = None
        player_row=None
        
        
        selected_player = st.selectbox("Select Player", player_data['name'].unique())
        if "player_name" in st.session_state:
            if st.session_state["player_name"] != selected_player:
                if "image" in st.session_state:
                    del st.session_state['image']
                    del st.session_state["s3_keyedit"]
                if "image_changed" in st.session_state:
                    del st.session_state["image_changed"]
        st.session_state["player_name"] = selected_player      
        player_row = player_data[player_data['name'] == selected_player].iloc[0]
        col1, col2= st.columns(2)
        with col1:
            if "image_changed" not in st.session_state:
                st.session_state['image'] = get_image(player_row['image_s3_key'])
                
            if "image" in st.session_state:
                st.image(st.session_state['image'])
                st.session_state["s3_keyedit"] = player_row['image_s3_key']
        with col2:
            uploaded_imageedit = st.file_uploader("Choose an image.../...اختر صورة", type=["jpg", "png", "jpeg"],key=2)
            if st.button("Change Image"):
                if uploaded_imageedit is not None:
                    # Use PIL to open the image (optional)
                    imagenew = Image.open(uploaded_imageedit).resize((150, 200), Image.ANTIALIAS)
                    # Generate a unique filename based on a UUID
                    
                    # TODO: Add any image manipulation or validation here
                    
                    
                    
                
                    #st.success(s3_key)
                    st.session_state['image']=imagenew
                    #st.write(s3_key)
                    #st.session_state["s3_keyedit"] = s3_key
                    st.session_state["image_changed"] = True
                    del uploaded_imageedit
                    st.experimental_rerun()
                else:
                    st.error("upload new image")
            
            
        
        with st.expander(get_string(st.session_state['language'],"Personal Info")):
            # Personal Information
            st.subheader(get_string(st.session_state['language'],'Personal Information'))
            player["name"] = st.text_input(get_string(st.session_state['language'],"Full Name"),value = player_row['name'])
            genderoptions = ['Male', 'Female']
            player["gender"] = st.selectbox(get_string(st.session_state['language'],"Gender"), ['Male', 'Female'],index = genderoptions.index(player_row['gender']))
            #default_date = pd.Timestamp(player_row['date_of_birth']).to_pydatetime().date()
            #st.write(player_row['date_of_birth'])
            min_date = date(1990, 1, 1)
            player["date_of_birth"] = st.date_input(get_string(st.session_state['language'],"Date of Birth"), value =player_row['date_of_birth'],min_value =min_date)
            player["nationality"] = st.text_input(get_string(st.session_state['language'],"Nationality"), value = player_row['nationality'])
            player["city_area"] = st.text_input(get_string(st.session_state['language'],"City/Area"),value = player_row['city_area'])
            player["current_club"] = st.text_input(get_string(st.session_state['language'],"Current Club"),value = player_row['current_club'] )
            player["contact_number"] = st.text_input(get_string(st.session_state['language'],"Contact Number"),value = player_row['contact_number'] )
            player["estimated_value"] = st.number_input(get_string(st.session_state['language'],"Estimated Value (in $EGP)"), min_value=0.0,value = float(player_row['estimated_value']))
        with st.expander(get_string(st.session_state['language'],"Physical")):
            st.subheader(get_string(st.session_state['language'],'Physical Attributes'))
            player["height"] = st.text_input(get_string(st.session_state['language'],"Height (cm)"),value = player_row['height'])
            player["weight"] = st.text_input(get_string(st.session_state['language'],"Weight (kg)"),value = player_row['weight'])
            footoptions = [ 'Right','Left', 'Both']
            player["preferred_foot"] = st.selectbox(get_string(st.session_state['language'],"Preferred Foot"), ['Right','Left', 'Both'],index = footoptions.index(player_row['preferred_foot']))
        with st.expander(get_string(st.session_state['language'],"Position")) :  
            # Positional Data
            st.subheader(get_string(st.session_state['language'],'Positional Data'))
            
            player["primary_position"] = st.selectbox(get_string(st.session_state['language'],"Primary Position"), positions,index = positions.index(player_row['primary_position']))
            
            #player["secondary_positions"] = st.multiselect(get_string(st.session_state['language'],"Secondary Positions"), positions,default = player_row['secondary_positions']if mode == "Edit Existing Player" else "[]")
            
            if not isinstance(player_row['Squad'],str) and math.isnan(player_row['Squad']):
                player_row['Squad'] = ""
            
            if pd.notna(player_row['Squad']):
                squad_list = player_row['Squad'].split('|')
            else:
                squad_list = []
            selected_squad = st.multiselect(get_string(st.session_state['language'],"Squad"),squad,default =squad_list)    
            player["Squad"] = '|'.join(selected_squad)    
        with st.expander(get_string(st.session_state['language'],"Skills Ratings")):
            # Skill Data
            st.subheader(get_string(st.session_state['language'],'Skills Data'))
            for skill in skills:
                #st.write(player_row[skill])
                player[skill] = st.slider(skill, min_value=0, max_value=10,value = int(player_row[skill]))

            st.subheader(get_string(st.session_state['language'],'Evaluation'))
            player["general_comments"] = st.text_input(get_string(st.session_state['language'],"General Comments"),value = player_row['general_comments'])
            player["strengths"] = st.text_input(get_string(st.session_state['language'],"Strengths"),value = player_row['strengths'])
            player["weaknesses"] = st.text_input(get_string(st.session_state['language'],"Weaknesses"),value = player_row['weaknesses'])
            player["injury"] = st.text_input(get_string(st.session_state['language'],"Injury History"),value = player_row['injury'])
            player["record_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Record Date
            player["scouted_by"] = st.session_state['username']
            player["age"]= player_row['age']
            player["image_s3_key"]= player_row['image_s3_key']
        if st.button(get_string(st.session_state['language'],'Save Player')):
            #player_data.reset_index(drop=True, inplace=True)
            # Check column names
            if "image_changed" in st.session_state:
                filename = f"{uuid4().hex}.png"
                s3_key = upload_to_s3(st.session_state["image"], filename)
                player['image_s3_key'] = s3_key
            
            player_df = pd.DataFrame([player])
            player_df = player_df[player_data.columns]
            # Get the data types of the selected row in player_data
            correct_dtypes = player_data.loc[player_data['name'] == st.session_state["player_name"]].dtypes

            # Convert the data types of player_df to match those of player_data
            for col in player_df.columns:
                player_df[col] = player_df[col].astype(correct_dtypes[col])
            
            
            index_to_update = player_data.index[player_data['name'] == st.session_state["player_name"]].tolist()
            if index_to_update:
                player_data.loc[index_to_update[0]] = player_df.iloc[0]
            else:
                st.write("Player name not found in player_data.")
            save_player_data(player_data)
            st.success("Player successfully Edited!")

  


    elif page == "Data Summarization/تلخيص البيانات":
        st.title('Football Player Scouting - Data Summarization')

        st.subheader('Data Summary')
        if filtered_data is not None and not filtered_data.empty:
            
            st.subheader('Positions Summary')
            if 'primary_position' in filtered_data.columns:
                positions_df = filtered_data['primary_position'].value_counts().rename_axis('Position').reset_index(name='Count')
                st.table(positions_df.set_index('Position'))

            st.subheader('Age Summary')
            if 'age' in filtered_data.columns:
                age_df = filtered_data['age'].value_counts().rename_axis('Age').reset_index(name='Count')
                st.table(age_df.set_index('Age'))

            st.subheader('Gender Summary')
            if 'gender' in filtered_data.columns:
                gender_df = filtered_data['gender'].value_counts().rename_axis('Gender').reset_index(name='Count')
                st.table(gender_df.set_index('Gender'))

            st.subheader('Skills by Position')
            for skill in skills:
                if skill in filtered_data.columns and 'primary_position' in filtered_data.columns:
                    chart = alt.Chart(filtered_data).mark_bar().encode(
                        x='primary_position:N',
                        y=f'mean({skill}):Q',
                        color='primary_position:N',
                        tooltip=['primary_position', f'mean({skill})']
                    ).properties(
                        title=f'{skill} by Position'
                    )
                    st.altair_chart(chart, use_container_width=True)

            st.subheader('Top Performers for Each Skill')
            for skill in skills:
                if skill in filtered_data.columns:
                    top_performer = filtered_data[['name', skill]].sort_values(by=[skill], ascending=False).head(1)
                    st.write(f'Top performer for {skill}: {top_performer["name"].values[0]} with score {top_performer[skill].values[0]}')

        else:
            st.write("No player data available.")


    # Page: Add Player
    elif page == "Player Statistics/إحصائيات اللاعب":
        st.title('Football Player Scouting - Player Statistics')

        st.subheader('Player List')
        if filtered_data is not None and not filtered_data.empty:
            player_to_view = st.selectbox('Select player to view', filtered_data['name'])
            indices = filtered_data[filtered_data['name'] == player_to_view].index
            st.table(filtered_data.loc[indices].T)
        else:
            st.write("No player data available.")
    elif page == "Full Table/الجدول الكامل":
        st.write(player_data)
        
