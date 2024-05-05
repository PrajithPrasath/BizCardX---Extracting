import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import pymysql

#FUNCTION TO CONVERT IMAGE TO  TXT
def IMG_to_TXT(path):
  img=Image.open(path)
  #converting img to array format
  img_arr=np.array(img)
  reader=easyocr.Reader(['en'])
  text=reader.readtext(img_arr,detail=0)

  return text,img

#FUNCTION TO TXT EXTRACT FROM IMAGE
def TXT_EXTRACT(text):
  dict={"NAME":[],"DESIGNATION": [],"COMPANY_NAME":[],"CONTACT":[],"EMAIL_ID":[],"WEBSITE":[],"ADDRESS":[],"PINCODE":[]}
  dict["NAME"].append(text[0])
  dict["DESIGNATION"].append(text[1])

  for i in range(2,len(text)):
    if text[i].startswith("+") or (text[i].replace("-","").isdigit() and "-" in text[i]):
      dict["CONTACT"].append(text[i])
    elif "@" in text[i] and (text[i].endswith(".com")):
      dict["EMAIL_ID"].append(text[i])
    elif "WWW" in text[i] or "www" in text[i] or "Www" in text[i] or "wWw" in text[i] or "wwW" in text[i]:
      web=text[i].lower()
      dict["WEBSITE"].append(web)
    elif "TamilNadu" in text[i] or "Tamil Nadu" in text[i] or text[i].isdigit():
      dict["PINCODE"].append(text[i])
    elif re.match (r'^[A-Z,a-z]',text[i]):
      dict["COMPANY_NAME"].append(text[i])
    else:
      remove= re.sub(r'^[,;]','',text[i])
      dict["ADDRESS"].append(remove)

  for key, value in dict.items():
    if len(value)>0:
      concate= " ".join(value)
      dict[key]=[concate]
    else:
      value= "NA"
      dict[key]=[value]

  return(dict)


#Streamlit
st.set_page_config(page_title="Bizcard",page_icon="🌍",layout="wide",initial_sidebar_state="expanded")
st.write("""<p style="font-family:Cursive, Lucida Handwriting;font-size: 45px; text-align: center; color:#FFFFF ">
         BizCardX: Extracting Business Card Data with OCR</p>""", unsafe_allow_html=True)
col1,col2,col3= st.columns([1,4,1])
with col2:
    SELECT = option_menu(menu_title=None,options = ["Home","Upload & Modify","Delete"],icons =["house","upload","delete"],
        default_index=0,orientation="horizontal",styles={"container": {"background-size":"auto", "width": "100%"},
        "icon": {"color": "black", "font-size": "20px"},"nav-link": {"font-size": "15px","font-family":"Cursive, Lucida Handwriting",
        "text-align": "center", "margin": "0px", "--hover-color": "#FF7F50"},
        "nav-link-selected": {"background-color": "#85C1E9"}})


if SELECT== "Home":
   col1,col2,col3= st.columns(3)
   with col2:
    st.image(Image.open(r"C:\Users\ELCOT\Desktop\New vs\images.png"), 
             caption=None, width=120, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    st.write("""<p style="font-family:Cursive, Lucida Handwriting;font-size: 35px; text-align: center">
             Introduction</p>""", unsafe_allow_html=True)
    with st.container(border=False,height=150):
       st.write("""<p style="font-family:Cursive, Lucida Handwriting;font-size: 18px; text-align: left"> 
                BizCardX is a Stream lit web application designed to effortlessly extract data from business 
                cards using Optical Character Recognition (OCR) technology. With BizCardX, users can easily 
                upload images of business cards,and the application leverages the powerful easyOCR library to 
                extract pertinent information from the cards.The extracted data is then presented in a 
                user-friendly format and can be stored in a SQL database for future reference 
                and management..</p>""", unsafe_allow_html=True)

elif SELECT=="Upload & Modify":
  File= st.file_uploader("Upload the file",type=["png","jpeg","jpg"]) #File upload

  if File is not None:
        st.image(File,width=400)
        text,img = IMG_to_TXT(File)
        TEXDICT= TXT_EXTRACT(text)

        if TEXDICT:
          st.success("Data Extracted")
          df= pd.DataFrame(TEXDICT)
          #Coverting Image into Bits
          Image_Bytes = io.BytesIO()
          img.save(Image_Bytes,format="PNG")
          IMG_DATA= Image_Bytes.getvalue()

          #Creating dict
          Dict={"IMAGE":[IMG_DATA]}
          df1=pd.DataFrame(Dict)

          Join=pd.concat([df,df1],axis=1)
          st.dataframe(Join)

          button1=st.button("Save")
          if button1:
            #Mysql con
            mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='bizcardx')
            cursor = mydb.cursor()
            #Table Creation
            Create_Query='''create table if not exists BIZCARD(NAME varchar(255), DESIGNATION varchar(255), 
                                                            COMPANY_NAME varchar(255), CONTACT varchar(255), 
                                                            EMAIL_ID varchar(255), WEBSITE text, ADDRESS text,
                                                            PINCODE varchar(255),IMAGE longblob)'''
            cursor.execute(Create_Query)
            mydb.commit()

            Insert_Query='''insert into BIZCARD(NAME, DESIGNATION, COMPANY_NAME, CONTACT, 
                                    EMAIL_ID, WEBSITE, ADDRESS, PINCODE,IMAGE)
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            Values=Join.values.tolist()[0]
            cursor.execute(Insert_Query,Values)
            mydb.commit()

            st.success(" Saved Successfully ")
            
  Method = st.radio("Select the method",["None","Preview","Modify"])
  if Method == "None":
      pass
  if Method == "Preview":
    #Mysql con
    mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='bizcardx')
    cursor = mydb.cursor()
    #Query 
    cursor.execute("select * from BIZCARD")
    Table= cursor.fetchall()
    mydb.commit()

    Tabledf=pd.DataFrame(Table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT",
                        "EMAIL_ID","WEBSITE","ADDRESS","PINCODE","IMAGE"))
    st.dataframe(Tabledf)
    
  if Method == "Modify":
    #Mysql con
    mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='bizcardx')
    cursor = mydb.cursor()
    #Query 
    cursor.execute("select * from BIZCARD")
    Table= cursor.fetchall()
    mydb.commit()

    Tabledf=pd.DataFrame(Table,columns=("NAME","DESIGNATION","COMPANY_NAME","CONTACT",
                        "EMAIL_ID","WEBSITE","ADDRESS","PINCODE","IMAGE"))
    col1,col2= st.columns(2)
    with col1:
        Name= st.selectbox("Select the name",Tabledf["NAME"],index=0)
    DF1= Tabledf[Tabledf["NAME"]==Name]
  
    DF2= DF1.copy()
    
    col1,col2= st.columns(2)
    with col1:
        Edit_Name= st.text_input("Name",DF1["NAME"].unique()[0])
        Edit_Desg= st.text_input("Designation",DF1["DESIGNATION"].unique()[0])
        Edit_Cmp= st.text_input("Company Name",DF1["COMPANY_NAME"].unique()[0])
        Edit_Con= st.text_input("Contact",DF1["CONTACT"].unique()[0])
        Edit_Email= st.text_input("Email_Id",DF1["EMAIL_ID"].unique()[0])

    DF2["NAME"]=Edit_Name
    DF2["DESIGNATION"]=Edit_Desg
    DF2["COMPANY_NAME"]=Edit_Cmp
    DF2["CONTACT"]=Edit_Con
    DF2["EMAIL_ID"]=Edit_Email

    with col2:
        Edit_Web= st.text_input("Website",DF1["WEBSITE"].unique()[0])
        Edit_Add= st.text_input("Address",DF1["ADDRESS"].unique()[0])
        Edit_Pin= st.text_input("Pincode",DF1["PINCODE"].unique()[0])
        Edit_Img= st.text_input("Image",DF1["IMAGE"].unique()[0])

    DF2["WEBSITE"]=Edit_Web
    DF2["ADDRESS"]=Edit_Add
    DF2["PINCODE"]=Edit_Pin
    DF2["IMAGE"]=Edit_Img

    st.dataframe(DF2)

    button2= st.button("Modify")
    if button2:
        #Mysql con
        mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='bizcardx')
        cursor = mydb.cursor()
        #Query
        cursor.execute(f"Delete from BIZCARD where NAME='{Name}'")
        mydb.commit()

        Insert_Query='''insert into BIZCARD(NAME, DESIGNATION, COMPANY_NAME, CONTACT, 
                                    EMAIL_ID, WEBSITE, ADDRESS, PINCODE,IMAGE)
                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        Values=DF2.values.tolist()[0]
        cursor.execute(Insert_Query,Values)
        mydb.commit()

        st.success("Modified successfully")

elif SELECT=="Delete":
    #Mysql con
    mydb = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='bizcardx')
    cursor = mydb.cursor()
    col1,col2= st.columns(2)
    with col1:
        #Query 
        cursor.execute("select NAME from BIZCARD")
        Table1= cursor.fetchall()
        mydb.commit()

        names=[]
        for i in Table1:
            names.append(i[0])
        
        Name1= st.selectbox("Select The Name",names)
    
    with col2:
      cursor.execute(f"SELECT DESIGNATION FROM BIZCARD WHERE NAME ='{Name1}'")
      Table2 = cursor.fetchall()
      mydb.commit()

      designation = []
      for j in Table2:
        designation.append(j[0])

      Desig = st.selectbox("Select the designation", options = designation)

    if Name1 and Desig:
      col1,col2= st.columns(2)
      with col1:
        st.write(f"Selected Name : {Name1}")
          # st.write("")
          # st.write("")
          # st.write("")
        st.write(f"Select the Designation : {Desig}")
      
      with col1:
        Remove= st.button("Delete")
        if Remove:
          cursor.execute(f"delete from BIZCARD where NAME='{Name1}' and DESIGNATION= '{Desig}'")
          mydb.commit()

          st.warning("DELETED")
