import os
import json
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import requests

def states_correction(dataframe):
    dataframe["States"] = dataframe["States"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar")
    dataframe["States"] = dataframe["States"].str.replace("-", " ")
    dataframe["States"] = dataframe["States"].str.title()
    dataframe["States"] = dataframe["States"].str.replace("Dadra & Nagar Haveli & Daman & Diu",
                                                        "Dadra and Nagar Haveli and Daman and Diu")

    return dataframe


# Aggregated transaction
path1= "D:/phonepe/data/aggregated/transaction/country/india/state/"

agg_trans_list = os.listdir(path1)

clm1={'States':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}


for state in agg_trans_list:
    cur_state = path1+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            D = json.load(Data)
            for z in D['data']['transactionData']:
                Name = z['name']
                count = z['paymentInstruments'][0]['count']
                amount = z['paymentInstruments'][0]['amount']
                clm1['Transacion_type'].append(Name)
                clm1['Transacion_count'].append(count)
                clm1['Transacion_amount'].append(amount)
                clm1['States'].append(state)
                clm1['Year'].append(yr)
                clm1['Quater'].append(int(file.strip('.json')))


Agg_Trans=pd.DataFrame(clm1)
states_correction(Agg_Trans)
#print(Agg_Trans)


# Aggregated user
path2 = "D:/phonepe/data/aggregated/user/country/india/state/"
agg_user_list = os.listdir(path2)
clm2={'States':[], 'Year':[],'Quater':[],'Brands':[], 'Counts':[], 'Percentage':[]}


for state in agg_user_list:
    cur_state = path2+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            E = json.load(Data)

            try:
                for z in E['data']['usersByDevice']:
                    brand = z['brand']
                    count = z['count']
                    percentage = z["percentage"]
                    clm2['Brands'].append(brand)
                    clm2['Counts'].append(count)
                    clm2['Percentage'].append(percentage)
                    clm2['States'].append(state)
                    clm2['Year'].append(yr)
                    clm2['Quater'].append(int(file.strip('.json')))

            except:
                pass

Agg_user=pd.DataFrame(clm2)
states_correction(Agg_user)
#print(Agg_user)

# map transaction
path3 = "D:/phonepe/data/map/transaction/hover/country/india/state/"

map_trans_list = os.listdir(path3)

clm3={"States":[], "Years":[], "Quarter":[],"District":[], "Transaction_count":[],"Transaction_amount":[]}


for state in map_trans_list:
    cur_state = path3+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            E = json.load(Data)
            for i in E['data']["hoverDataList"]:
                name = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                clm3["District"].append(name)
                clm3["Transaction_count"].append(count)
                clm3["Transaction_amount"].append(amount)
                clm3["States"].append(state)
                clm3["Years"].append(yr)
                clm3["Quarter"].append(int(file.strip(".json")))

map_trans = pd.DataFrame(clm3)
states_correction(map_trans)
#print(map_trans)

# map user
path4="D:/phonepe/data/map/user/hover/country/india/state/"

map_user_list = os.listdir(path4)

clm4={"States":[], "Years":[], "Quarter":[], "Districts":[], "RegisteredUser":[], "AppOpens":[]}


for state in map_user_list:
    cur_state = path4+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            E = json.load(Data)

            for i in E["data"]["hoverData"].items():
                district = i[0]
                registered_user = i[1]["registeredUsers"]
                app_opens = i[1]["appOpens"]
                clm4["Districts"].append(district)
                clm4["RegisteredUser"].append(registered_user)
                clm4["AppOpens"].append(app_opens)
                clm4["States"].append(state)
                clm4["Years"].append(yr)
                clm4["Quarter"].append(int(file.strip(".json")))

map_user = pd.DataFrame(clm4)
states_correction(map_user)
#print(map_user)

# top transaction
path5 = "D:/phonepe/data/top/transaction/country/india/state/"

top_trans_list = os.listdir(path5)


clm5={"States":[], "Years":[], "Quarter":[], "Pincodes":[], "Transaction_count":[], "Transaction_amount":[]}


for state in top_trans_list:
    cur_state = path5+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            E = json.load(Data)

            for i in E["data"]["pincodes"]:
                entityName = i["entityName"]
                count = i["metric"]["count"]
                amount = i["metric"]["amount"]
                clm5["Pincodes"].append(entityName)
                clm5["Transaction_count"].append(count)
                clm5["Transaction_amount"].append(amount)
                clm5["States"].append(state)
                clm5["Years"].append(yr)
                clm5["Quarter"].append(int(file.strip(".json")))

top_trans = pd.DataFrame(clm5)
states_correction(top_trans)
#print(top_trans)

#top user

path6 = "D:/phonepe/data/top/user/country/india/state/"

top_user_list = os.listdir(path6)



clm6={"States":[], "Years":[], "Quarter":[], "Pincodes":[], "RegisteredUser":[]}


for state in top_user_list:
    cur_state = path6+state+"/"
    agg_yr = os.listdir(cur_state)

    for yr in agg_yr:
        cur_year = cur_state+yr+"/"
        agg_yr = os.listdir(cur_year)

        for file in agg_yr:
            cur_file = cur_year+file

            Data = open(cur_file, 'r')
            E = json.load(Data)

            for i in E["data"]["pincodes"]:
                pincode = i["name"]
                registeredusers = i["registeredUsers"]
                clm6["Pincodes"].append(pincode)
                clm6["RegisteredUser"].append(registeredusers)
                clm6["States"].append(state)
                clm6["Years"].append(yr)
                clm6["Quarter"].append(int(file.strip(".json")))
top_user = pd.DataFrame(clm6)
states_correction(top_user)
#print(top_user)

#sql insertion
# agg transaction table

db = pymysql.connect(
        host="localhost",
        user="root",
        password="1234"
)

mysql = "mysql+pymysql://root:1234@localhost/phonepe"
engine = create_engine(mysql)

connect = db.cursor()

connect.execute('create database if not exists phonepe')
connect.execute('use phonepe')

connect.execute('''create table if not exists aggregated_transaction(States VARCHAR(100),
                                        Year INT, Quater INT,
                                        Transacion_type VARCHAR(100), Transacion_count BIGINT,
                                        Transacion_amount BIGINT)''')

db.commit()
Agg_Trans.to_sql('aggregated_transaction',engine,if_exists='append',index=False)
#print(Agg_Trans)


# agg user table


connect.execute('''create table if not exists aggregated_user (States varchar(100),
                                                                Year int,
                                                                Quater int,
                                                                Brands varchar(50),
                                                                Counts bigint,
                                                                Percentage float)''')

db.commit()
Agg_user.to_sql('aggregated_user', engine, if_exists='append', index=False)

#map transaction table

connect.execute('''create table if not exists map_transaction(States varchar(100),
                                                                Years int,
                                                                Quarter int,
                                                                District varchar(100),
                                                                Transaction_count bigint,
                                                                Transaction_amount float)''')

db.commit()
map_trans.to_sql('map_transaction',engine,if_exists='append',index=False)

#map user table

connect.execute('''create table if not exists map_user (States varchar(100),
                                                        Years int,
                                                        Quarter int,
                                                        Districts varchar(100),
                                                        RegisteredUser bigint,
                                                        AppOpens bigint)''')

db.commit()
map_user.to_sql('map_user', engine, if_exists='append', index=False)

# top transaction table

connect.execute('''create table if not exists top_transaction(States varchar(100),
                                                                Years int,
                                                                Quarter int,
                                                                pincodes int,
                                                                Transaction_count bigint,
                                                                Transaction_amount bigint)''')

db.commit()
top_trans.to_sql('top_transaction',engine,if_exists='append',index=False)


# top user table

connect.execute('''create table if not exists top_user (States varchar(100),
                                                        Years int,
                                                        Quarter int,
                                                        Pincodes int,
                                                        RegisteredUser bigint
                                                        )''')

db.commit()
top_user.to_sql('top_user', engine, if_exists='append', index=False)

# creating Dataframe
#agg transaction
connect.execute('select * from aggregated_transaction')
agg_trans_table = pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'Transaction type', 'Transaction counts','Transaction amount'])


#agg user

connect.execute('select * from aggregated_user')
agg_user_table= pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'Brands', 'Transaction counts','Percentage'])

#map trans

connect.execute('select * from map_transaction')
map_trans_table = pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'District', 'Transaction counts','Transaction amount'])

#map user

connect.execute('select * from map_user')
map_user_table = pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'District', 'Registered user','App opens'])

# top trans

connect.execute('select * from top_transaction')
top_trans_table = pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'Pincode', 'Transaction counts','Transaction amount'])


#top user
connect.execute('select * from top_user')
top_user_table = pd.DataFrame(connect.fetchall(), columns=['States', 'Year', 'Quater', 'Pincode', 'Registered user'])


def transaction_count_year(dataframe, year):

    tac_yr = dataframe[dataframe["Year"] == year]
    tac_yr.reset_index(drop = True, inplace= True)

    tac_yr_gr = tac_yr.groupby("States")[["Transaction counts","Transaction amount"]].sum()
    tac_yr_gr.reset_index(inplace= True)

    tra_amount = px.bar(tac_yr_gr, x="States", y="Transaction amount", title="Transaction Amount", height=600)
    st.plotly_chart(tra_amount)

    tra_count = px.bar(tac_yr_gr, x="States", y="Transaction counts", title="Transaction Count", height=600)
    st.plotly_chart(tra_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1 = px.choropleth(tac_yr_gr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction amount", color_continuous_scale="turbo",
                                range_color=(tac_yr_gr["Transaction amount"].min(), tac_yr_gr["Transaction amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600)
    fig_india_1.update_geos(visible=False)
    st.plotly_chart(fig_india_1)

    fig_india_2 = px.choropleth(tac_yr_gr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction counts", color_continuous_scale="turbo",
                                range_color=(tac_yr_gr["Transaction counts"].min(), tac_yr_gr["Transaction counts"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600)
    fig_india_2.update_geos(visible=False)
    st.plotly_chart(fig_india_2)










#streamlit


st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Menu", ["Home", "Data Exploration", "Top Charts"])

if select== "Home":
    pass
elif select== "Data Exploration":

    tab1,tab2,tab3 = st.tabs(["Aggregated", "Map", "Top"])
    with tab1:
        option = st.radio("Select the option", ["Aggregated Transaction Analysis", "Aggregated User Analysis"])
        if option == "Aggregated Transaction Analysis":
            years = st.selectbox("Select a year", agg_trans_table["Year"].unique())
            transaction_count_year(agg_trans_table, years)



        elif option == "Aggregated User Analysis":
            pass

    with tab2:
        option = st.radio("Select the option", ["Map Transaction Analysis", "Map User Analysis"])
        if option == "Map Transaction Analysis":
            pass
        elif option == "Map User Analysis":
            pass

    with tab3:
        option = st.radio("Select the option", ["Top Transaction Analysis", "Top User Analysis"])
        if option == "Top Transaction Analysis":
            pass
        elif option == "Top User Analysis":
            pass

elif select== "Top Charts":
    pass



