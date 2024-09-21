import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as pt
import requests
import json
from PIL import Image

#Creating DATAFRAME
#PostgreSQL connection

conn = psycopg2.connect(host='localhost',
                        database= 'PhonePe',
                        user= 'postgres',
                        password= 'Tk0407', 
                        port= 5432 )
cursor=conn.cursor()

#Aggreated_Insurance_DATAFRAME

cursor.execute("select * from aggregated_insurance")
conn.commit()
table1=cursor.fetchall()

agg_insurance=pd.DataFrame(table1,columns=("states", "Years", "Quarter", "Transaction_type",
                                          "Transaction_count", "Transaction_amount"))

#Aggreated_Transaction_DATAFRAME

cursor.execute("select * from aggregated_transaction")
conn.commit()
table2=cursor.fetchall()

agg_transaction=pd.DataFrame(table2,columns=("states", "Years", "Quarter", "Transaction_type",
                                              "Transaction_count", "Transaction_amount"))

#Aggreated_User_DATAFRAME

cursor.execute("select * from aggregated_user")
conn.commit()
table3=cursor.fetchall()

agg_user=pd.DataFrame(table3,columns=("states", "Years", "Quarter", "Brands",
                                              "Transaction_count", "Percentage"))

#MAP_Insurance_DATAFRAME

cursor.execute("select * from map_insurance")
conn.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4, columns=("states", "Years", "Quarter", "Districts",
                                          "Transaction_count", "Transaction_amount"))

#MAP_Transaction_DATAFRAME

cursor.execute("select * from map_transaction")
conn.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5, columns=("states", "Years", "Quarter", "Districts",
                                          "Transaction_count", "Transaction_amount"))


#MAP_User_DATAFRAME

cursor.execute("select * from map_user")
conn.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6, columns=("states", "Years", "Quarter", "Districts",
                                          "Registered_Users", "App_Opens"))

#TOP_Insurance_DATAFRAME

cursor.execute("select * from top_insurance")
conn.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7, columns=("states", "Years", "Quarter", "Pincodes",
                                          "Transaction_count", "Transaction_amount"))

#TOP_Transaction_DATAFRAME

cursor.execute("select * from top_transaction")
conn.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8, columns=("states", "Years", "Quarter", "Pincodes",
                                          "Transaction_count", "Transaction_amount"))


#TOP_User_DATAFRAME

cursor.execute("select * from top_user")
conn.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9, columns=("states", "Years", "Quarter", "Pincodes",
                                          "RegisteredUsers"))


def Transaction_amount_count(df, year):

    tran_amt_ct_yr = df[df["Years"] == year]
    tran_amt_ct_yr.reset_index(drop=True,inplace=True)

    tran_amt_ct_yr_grp = tran_amt_ct_yr.groupby("states")[["Transaction_count","Transaction_amount"]].sum()
    tran_amt_ct_yr_grp.reset_index(inplace= True)
    
    col1,col2=st.columns(2)
    
    with col1:
        fig_ct = pt.bar(tran_amt_ct_yr_grp, x="states", y="Transaction_count", title=f" TRANSACTION COUNT OF {year}",
                    color_discrete_sequence=pt.colors.sequential.Agsunset, height=600, width=600)
        st.plotly_chart(fig_ct)
    
    with col2:
        fig_amt= pt.bar(tran_amt_ct_yr_grp, x="states", y="Transaction_amount", title=f" TRANSACTION AMOUNT OF {year}",
                    color_discrete_sequence=pt.colors.sequential.Bluered_r, height=600, width=600)
        st.plotly_chart(fig_amt)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        India_figure_ct=pt.choropleth(tran_amt_ct_yr_grp, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tran_amt_ct_yr_grp["Transaction_count"].min(), tran_amt_ct_yr_grp["Transaction_count"].max()),
                                    hover_name= "states", title=f"TRANSACTION COUNT OF {year}", fitbounds= "locations", height=600, width=600)
        India_figure_ct.update_geos(visible=False)
        st.plotly_chart(India_figure_ct)
        

    with col2:

        India_figure_amt=pt.choropleth(tran_amt_ct_yr_grp, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color= (tran_amt_ct_yr_grp["Transaction_amount"].min(), tran_amt_ct_yr_grp["Transaction_amount"].max()),
                                    hover_name= "states", title=f"TRANSACTION AMOUNT OF {year}", fitbounds= "locations", height=600, width=600)
        India_figure_amt.update_geos(visible=False)
        st.plotly_chart(India_figure_amt)

    return tran_amt_ct_yr 

def Transaction_amount_count_qua(df, quarter):

    tran_amt_ct_yr = df[df["Quarter"] == quarter]
    tran_amt_ct_yr.reset_index(drop=True,inplace=True)

    tran_amt_ct_yr_grp = tran_amt_ct_yr.groupby("states")[["Transaction_count","Transaction_amount"]].sum() 
    tran_amt_ct_yr_grp.reset_index(inplace= True)

    col1,col2=st.columns(2)
    
    with col1:

        fig_ct = pt.bar(tran_amt_ct_yr_grp, x="states", y="Transaction_count", title=f" TRANSACTION COUNT OF {tran_amt_ct_yr['Years'].min()} YEAR Quarter-{quarter}",
                        color_discrete_sequence=pt.colors.sequential.Agsunset, height=600, width=600)
        st.plotly_chart(fig_ct)

    with col2:
        fig_amt= pt.bar(tran_amt_ct_yr_grp, x="states", y="Transaction_amount", title=f" TRANSACTION AMOUNT OF {tran_amt_ct_yr['Years'].min()} YEAR Quarter-{quarter}",
                    color_discrete_sequence=pt.colors.sequential.Bluered_r, height=600, width=600)
        st.plotly_chart(fig_amt)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
 
        states_name.sort()

        India_figure_ct=pt.choropleth(tran_amt_ct_yr_grp, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color= (tran_amt_ct_yr_grp["Transaction_count"].min(), tran_amt_ct_yr_grp["Transaction_count"].max()),
                                    hover_name= "states", title=f" TRANSACTION COUNT OF {tran_amt_ct_yr['Years'].min()} YEAR Quarter-{quarter}", fitbounds= "locations", height=600, width=600)
        India_figure_ct.update_geos(visible=False)
        
        st.plotly_chart(India_figure_ct)
        

    with col2:

        India_figure_amt=pt.choropleth(tran_amt_ct_yr_grp, geojson= data1, locations= "states", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color= (tran_amt_ct_yr_grp["Transaction_amount"].min(), tran_amt_ct_yr_grp["Transaction_amount"].max()),
                                    hover_name= "states", title=f" TRANSACTION COUNT OF {tran_amt_ct_yr['Years'].min()} YEAR Quarter-{quarter}", fitbounds= "locations", height=600, width=600)
        India_figure_amt.update_geos(visible=False)
        
        st.plotly_chart(India_figure_amt)

    return tran_amt_ct_yr

def Agg_Transaction_Type(df,state):

    tran_amt_ct_yr = df[df["states"] == state]
    tran_amt_ct_yr.reset_index(drop=True,inplace=True)

    tran_amt_ct_yr_grp = tran_amt_ct_yr.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum() 
    tran_amt_ct_yr_grp.reset_index(inplace= True)

    col1,col2=st.columns(2)
            
    with col1:

        fig_pie_amt = pt.pie(data_frame = tran_amt_ct_yr_grp,names="Transaction_type", values="Transaction_amount",
                            width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_amt)
    with col2:

        fig_pie_ct = pt.pie(data_frame = tran_amt_ct_yr_grp,names="Transaction_type", values="Transaction_count",
                            width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_ct)


#Aggregated user data analysis-1
def agg_user_year_fig1(df, year):

    agg_user_yr = df[df["Years"]==year]
    agg_user_yr.reset_index(drop=True, inplace=True) 

    agg_user_yr_grp = pd.DataFrame(agg_user_yr.groupby("Brands")[["Transaction_count"]].sum())
    agg_user_yr_grp.reset_index(inplace=True) 

    agg_user_fig1 = pt.bar(agg_user_yr_grp, x="Brands", y="Transaction_count" ,title=f" Brands and Transaction count of {years} Year",
                        width=1000, color_discrete_sequence= pt.colors.sequential.Aggrnyl,hover_name = "Brands")
    st.plotly_chart(agg_user_fig1)

    return agg_user_yr

#Aggregated user data analysis-2
def agg_user_year_fig2(df, quarter):

    agg_user_yr_qua = df[df["Quarter"]==quarter]
    agg_user_yr_qua.reset_index(drop=True, inplace=True) 


    agg_user_yr_Qua_grp = pd.DataFrame(agg_user_yr_qua.groupby("Brands")[["Transaction_count"]].sum())
    agg_user_yr_Qua_grp.reset_index(inplace=True) 

    agg_fig_user2 = pt.bar(agg_user_yr_Qua_grp, x="Brands", y="Transaction_count" ,title=f"Brands and Transaction count for Quarter-{quarter}",
                            width=1000, color_discrete_sequence= pt.colors.sequential.Aggrnyl,hover_name="Brands")
    st.plotly_chart(agg_fig_user2)

    return agg_user_yr_qua

#Aggregated user data analysis-3
def agg_user_year_fig3(df, state ):

    agg_user_yr_qua_sta = df[df["states"]== state]
    agg_user_yr_qua_sta.reset_index(drop=True, inplace=True)

    agg_fig_user3=pt.line(agg_user_yr_qua_sta, x="Brands", y="Transaction_count" ,title=f"Brands , Transaction and Percentage analysis of {state}",
                                width=1000, color_discrete_sequence= pt.colors.sequential.Aggrnyl, hover_data="Percentage",markers=True )

    st.plotly_chart(agg_fig_user3)

#map_insurance District
def map_insurance_Dist(df,state):

    tran_amt_ct_yr = df[df["states"] == state]
    tran_amt_ct_yr.reset_index(drop=True,inplace=True)

    tran_amt_ct_yr_grp = tran_amt_ct_yr.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum() 
    tran_amt_ct_yr_grp.reset_index(inplace= True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_amt = pt.bar(tran_amt_ct_yr_grp, x ="Transaction_amount",y ="Districts", orientation="h", height=600,
                                title=f"{state.upper()}-DISTRICT & TRANSACTION AMOUNT",color_discrete_sequence=pt.colors.sequential.Bluered)
        st.plotly_chart(fig_bar_amt)

    with col2:

        fig_bar_ct = pt.bar(tran_amt_ct_yr_grp, x ="Transaction_count", y ="Districts", orientation="h",height=600,
                            title=f"{state.upper()}-DISTRICT & TRANSACTION COUNT",color_discrete_sequence=pt.colors.sequential.Plasma)
        st.plotly_chart(fig_bar_ct)   

#map_user_analysis 
def map_user_fig1(df,year):

    map_user_yr = df[df["Years"]== year ]
    map_user_yr.reset_index(drop=True, inplace=True) 

    map_user_yr_grp = map_user_yr.groupby("states")[["Registered_Users","App_Opens"]].sum()
    map_user_yr_grp.reset_index(inplace=True) 

    
    map_fig_user=pt.line(map_user_yr_grp, x="states", y=["Registered_Users","App_Opens"] ,title=f"Registered Users & App opens of {year} year",
                        width=1000, height=800, color_discrete_sequence= pt.colors.sequential.Bluered_r,markers=True)

    st.plotly_chart(map_fig_user)

    return map_user_yr   


#map_user_analysis2
def map_user_fig2(df,quarter):

    map_user_yr_qua = df[df["Quarter"]== quarter]
    map_user_yr_qua.reset_index(drop=True, inplace=True) 

    map_user_yr_qua_grp = map_user_yr_qua.groupby("states")[["Registered_Users","App_Opens"]].sum()
    map_user_yr_qua_grp.reset_index(inplace=True) 

    map_fig_user1=pt.line(map_user_yr_qua_grp, x="states", y=["Registered_Users","App_Opens"] ,title=f"Registered Users & App opens of {df['Years'].min()} Quarter-{quarter}",
                            width=1000, height=800, color_discrete_sequence= pt.colors.sequential.Bluered_r,markers=True)

    st.plotly_chart(map_fig_user1)

    return map_user_yr_qua

#map User analysis 3
def map_user_fig3(df,states):

    map_user_yr_qua_st = df[df["states"]== states]
    map_user_yr_qua_st.reset_index(drop=True, inplace=True) 

    col1,col2=st.columns(2)
    with col1:
        map_fig_bar1=pt.bar(map_user_yr_qua_st, x="Registered_Users", y="Districts",orientation="h",
                        title=f"Registered_Users of {states.upper()} Districts",height=800, color_discrete_sequence=pt.colors.sequential.RdBu)
        st.plotly_chart(map_fig_bar1) 

    with col2:
        map_fig_bar2=pt.bar(map_user_yr_qua_st, x="App_Opens", y="Districts",orientation="h",
                        title=f"App_opens of {states.upper()} Districts",height=800, color_discrete_sequence=pt.colors.sequential.RdBu_r)
        st.plotly_chart(map_fig_bar2)


def Top_insurance_fig1(df,state):
    Top_insur_yr_qua = df[df["states"]== state]
    Top_insur_yr_qua.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1: 

        Top_insur_fig_bar1=pt.bar(Top_insur_yr_qua, x="Quarter", y="Transaction_amount",hover_data="Pincodes",
                                    title="Transaction Amount", height=600, color_discrete_sequence=pt.colors.sequential.RdBu)
        st.plotly_chart(Top_insur_fig_bar1)  

    with col2: 

        Top_insur_fig_bar2=pt.bar(Top_insur_yr_qua, x="Quarter", y="Transaction_count",hover_data="Pincodes",
                                    title="Transaction Count", height=600, color_discrete_sequence=pt.colors.sequential.RdPu_r)
        st.plotly_chart(Top_insur_fig_bar2)

def top_user_fig1(df,year):

    top_user_yr = df[df["Years"]==year]
    top_user_yr.reset_index(drop=True, inplace=True) 

    top_user_yr_grp = pd.DataFrame(top_user_yr.groupby(["states","Quarter"])[["RegisteredUsers"]].sum())
    top_user_yr_grp.reset_index(inplace=True) 

    top_user_bar=pt.bar(top_user_yr_grp, x="states", y="RegisteredUsers", color="Quarter", height=800,
                        width=1000, color_discrete_sequence= pt.colors.sequential.Viridis_r,hover_name="states", title=f"Registered Users of {year}")

    st.plotly_chart(top_user_bar)

    return top_user_yr

#TOP User figure2
def Top_user_fig2(df,state):

    top_user_yr_st = df[df["states"]== state]
    top_user_yr_st.reset_index(drop=True, inplace=True) 

    top_user_bar2=pt.bar(top_user_yr_st, x="Quarter", y="RegisteredUsers",hover_name="Pincodes",title="Registered user,pincodes,quarter",
                        height=800, width=1000, color ="RegisteredUsers", color_continuous_scale= pt.colors.sequential.Magenta)

    st.plotly_chart(top_user_bar2)


def Top_chart_Transaction_amount(table_name):

    conn = psycopg2.connect(host='localhost',
                            database= 'PhonePe',
                            user= 'postgres',
                            password= 'Tk0407', 
                            port= 5432 )
    cursor=conn.cursor()

    query1=f'''select states,sum(transaction_amount)as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount
                desc limit 10;'''

    cursor.execute(query1)
    table_1 =cursor.fetchall()
    conn.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount1 = pt.bar(df_1, x="states", y="transaction_amount", title=f"TOP 10 OF TRANSACTION AMOUNT",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #Figure2
    query2=f'''select states,sum(transaction_amount)as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount
                limit 10;'''

    cursor.execute(query2)
    table_2 =cursor.fetchall()
    conn.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_amount"))
    with col2:
        fig_amount2 = pt.bar(df_2, x="states", y="transaction_amount", title=f"LAST 10 OF TRANSACTION AMOUNT",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #Figure3
    query3=f'''select states,AVG(transaction_amount)as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount'''

    cursor.execute(query3)
    table_3 =cursor.fetchall()
    conn.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_amount"))

    fig_amount3 = pt.bar(df_3, x="transaction_amount", y="states",orientation="h", title=f" AVERAGE OF TRANSACTION AMOUNT",hover_name="states",
                    color_discrete_sequence=pt.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount3)

def Top_chart_Transaction_count(table_name):

    conn = psycopg2.connect(host='localhost',
                            database= 'PhonePe',
                            user= 'postgres',
                            password= 'Tk0407', 
                            port= 5432 )
    cursor=conn.cursor()

    query1=f'''select states,sum(transaction_count)as transaction_count 
                from {table_name}
                group by states
                order by transaction_count
                desc limit 10;'''

    cursor.execute(query1)
    table_1 =cursor.fetchall()
    conn.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount1 = pt.bar(df_1, x="states", y="transaction_count", title=f"TOP 10 OF TRANSACTION COUNT",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount1)

    #Figure2
    query2=f'''select states,sum(transaction_count)as transaction_count 
                from {table_name}
                group by states
                order by transaction_count
                limit 10;'''

    cursor.execute(query2)
    table_2 =cursor.fetchall()
    conn.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_count"))
    with col2:
        fig_amount2 = pt.bar(df_2, x="states", y="transaction_count", title=f"LAST 10 OF TRANSACTION COUNT",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #Figure3
    query3=f'''select states,AVG(transaction_count)as transaction_count
                from {table_name}
                group by states
                order by transaction_count'''

    cursor.execute(query3)
    table_3 =cursor.fetchall()
    conn.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_count"))

    fig_amount3 = pt.bar(df_3, x="transaction_count", y="states",orientation="h", title=f" AVERAGE OF TRANSACTION COUNT",hover_name="states",
                    color_discrete_sequence=pt.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount3)


def Top_chart_Registered_User(table_name,state):

    conn = psycopg2.connect(host='localhost',
                            database= 'PhonePe',
                            user= 'postgres',
                            password= 'Tk0407', 
                            port= 5432 )
    cursor=conn.cursor()

    query1=f'''select districts, sum(registered_users) as registered_users from {table_name}  
                where states= '{state}'
                group by districts
                order by registered_users desc
                limit 10'''

    cursor.execute(query1)
    table_1 =cursor.fetchall()
    conn.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","registered_users"))

    col1,col2=st.columns(2)
    with(col1):
         
        fig_amount1 = pt.bar(df_1, x="districts", y="registered_users", title=f"TOP 10 of REGISTERED USER",hover_name="districts",
                        color_discrete_sequence=pt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount1) 

    #Figure2
    query2=f'''select districts, sum(registered_users) as registered_users from {table_name} 
                where states= '{state}'
                group by districts
                order by registered_users
                limit 10'''

    cursor.execute(query2)
    table_2 =cursor.fetchall()
    conn.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","registered_users"))
    with(col2):

        fig_amount2 = pt.bar(df_2, x="districts", y="registered_users", title=f"Last 10 Registered Users",hover_name="districts",
                        color_discrete_sequence=pt.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #Figure3
    query3=f'''select districts, Avg(registered_users) as registered_users from {table_name} 
                where states= '{state}'
                group by districts
                order by registered_users'''

    cursor.execute(query3)
    table_3 =cursor.fetchall()
    conn.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","registered_users"))

    fig_amount3 = pt.bar(df_3, x="registered_users", y="districts",orientation="h", title=f" Average of Registered Users",hover_name="districts",
                    color_discrete_sequence=pt.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount3)


def Top_chart_appopens(table_name,state):

    conn = psycopg2.connect(host='localhost',
                            database= 'PhonePe',
                            user= 'postgres',
                            password= 'Tk0407', 
                            port= 5432 )
    cursor=conn.cursor()

    query1=f'''select districts, sum(app_opens) as app_opens from {table_name}  
                where states= '{state}'
                group by districts
                order by app_opens desc
                limit 10'''

    cursor.execute(query1)
    table_1 =cursor.fetchall()
    conn.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","app_opens"))
   
    col1,col2=st.columns(2)
    with(col1):

        fig_amount1 = pt.bar(df_1, x="districts", y="app_opens", title=f"TOP 10 of App_opens",hover_name="districts",
                        color_discrete_sequence=pt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount1) 

    #Figure2
    query2=f'''select districts, sum(app_opens) as app_opens from {table_name} 
                where states= '{state}'
                group by districts
                order by app_opens
                limit 10'''

    cursor.execute(query2)
    table_2 =cursor.fetchall()
    conn.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","app_opens"))
    with(col2):
    
        fig_amount2 = pt.bar(df_2, x="districts", y="app_opens", title=f"Last 10 App_opens",hover_name="districts",
                        color_discrete_sequence=pt.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #Figure3
    query3=f'''select districts, Avg(app_opens) as app_opens from {table_name} 
                where states= '{state}'
                group by districts
                order by app_opens'''

    cursor.execute(query3)
    table_3 =cursor.fetchall()
    conn.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","app_opens"))

    fig_amount3 = pt.bar(df_3, x="app_opens", y="districts",orientation="h", title=f" Average of App_opens ",hover_name="districts",
                    color_discrete_sequence=pt.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount3)


def Top_chart_Registered_Users (table_name):

    conn = psycopg2.connect(host='localhost',
                            database= 'PhonePe',
                            user= 'postgres',
                            password= 'Tk0407', 
                            port= 5432 )
    cursor=conn.cursor()

    query1=f'''select states, sum(registeredusers) as registeredusers from {table_name}
                group by states
                order by registeredusers desc
                limit 10'''

    cursor.execute(query1)
    table_1 =cursor.fetchall()
    conn.commit()

    df_1=pd.DataFrame(table_1, columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with(col1):
        fig_amount1 = pt.bar(df_1, x="states", y="registeredusers", title=f"TOP 10 of Registered users",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset,height=650,width=600)
        st.plotly_chart(fig_amount1) 

    #Figure2
    query2=f'''select states, sum(registeredusers) as registeredusers from {table_name} 
                group by states
                order by registeredusers 
                limit 10'''

    cursor.execute(query2)
    table_2 =cursor.fetchall()
    conn.commit()

    df_2=pd.DataFrame(table_2, columns=("states","registeredusers"))
    with col2:

        fig_amount2 = pt.bar(df_2, x="states", y="registeredusers", title=f"Last 10 Registered users",hover_name="states",
                        color_discrete_sequence=pt.colors.sequential.Agsunset_r,height=650,width=600)
        st.plotly_chart(fig_amount2)

    #Figure3
    query3=f'''select states, avg(registeredusers) as registeredusers from {table_name} 
                group by states
                order by registeredusers'''

    cursor.execute(query3)
    table_3 =cursor.fetchall()
    conn.commit()

    df_3=pd.DataFrame(table_3, columns=("states","registeredusers"))

    fig_amount3 = pt.bar(df_3, x="registeredusers", y="states",orientation="h", title=f" Average of Registered users ",hover_name="states",
                    color_discrete_sequence=pt.colors.sequential.Bluered,height=800,width=1000)
    st.plotly_chart(fig_amount3)


#starting Streamlit app page

# CSS for custom styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://cdn.dribbble.com/users/1902890/screenshots/15619502/media/4110e14facc720955ac1ad0ae1589477.gif");
        background-position: center;
        background-size: cover;
    }

    .title {
        color: #FFFFFF;
        font-size: 36px;
        font-weight: bold;
    }
    /* Tab headers color */
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important;  /* Set tab text color to white */
    }
        /* Ensure all radio button labels are white */
    div[data-baseweb="radio"] > div {
        color: #FFFFFF !important;
    }
    
    /* Make the radio button itself white when selected */
    div[data-baseweb="radio"] input:checked + div > div {
        background-color: #FFFFFF !important;
    }

    /* Change the color of the labels inside the radio options */
    div[data-baseweb="radio"] > div > label {
        color: #FFFFFF !important;
    }
    
    /* Change text of the header inside the radio label */
    div[data-baseweb="radio"] > div > div {
        color: #FFFFFF !important;
    }

    /* Radio button labels and selected option color */
    body {
        color: #FFFFFF !important;
    }
    .stRadio label {
        color: #FFFFFF !important;  /* Set radio button labels to white */
    }
    .stRadio div[role='radiogroup'] > label {
        color: #FFFFFF !important;  /* Ensure all radio button labels are white */
    }
    .stRadio div[role='radiogroup'] > label div[aria-checked="true"] > div:first-child {
        background-color: #FFFFFF !important;  /* Set the radio button selection dot to white */
    }
    .stRadio div[role='radiogroup'] > label div[aria-checked="true"] > div:first-child:hover {
        background-color: #FFFFFF !important;  /* Maintain white color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st
from PIL import Image

# Title of the app with white text color
st.markdown("<h1 style='color: white;'>PhonePe Data Visualization and Exploration</h1>", unsafe_allow_html=True)

# Sidebar with navigation menu
with st.sidebar:
    select = st.selectbox("Main Menu", ["Home", "Data Exploration", "Top Charts"])

# Home page content
if select == "Home":
    
    # Main content with two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Header and subheader with white text color
        st.markdown("<h2 style='color: white;'>PHONEPE</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: white;'>INDIA'S BEST TRANSACTION APP</h3>", unsafe_allow_html=True)
        
        # Paragraph text with white color
        st.markdown("""
        <p style='color: white;'>
        PhonePe Group is India’s leading fintech company. Its flagship product, the PhonePe digital payments app, was launched in Aug 2016. **PhonePe** is an Indian digital payments and financial technology company offering a seamless experience for all your transactions.
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: white;'>Features</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Credit & Debit card linking</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Bank Balance check</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Money Storage</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- PIN Authorization</p>", unsafe_allow_html=True)
        
        st.download_button("Download the App Now", "https://www.phonepe.com/app-download/")
    
    with col2:
        # Displaying image in second column
        video_file = open(r"C:\Users\Ramachandran T\Desktop\phonepe\home-fast-secure-v3.mp4","rb")
        video_bytes = video_file.read()
        st.video(video_bytes,autoplay=True,loop=True)

    # Second row with two columns for additional content
    col3, col4 = st.columns([1, 1], gap="large")
    
    with col3:
        phonepe_logo = Image.open(r"C:\Users\Ramachandran T\Desktop\phonepe\phonepe1.png")
        st.image(phonepe_logo, width=350)
    
    with col4:
        st.markdown("<div style='margin-left: 40px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: white;'>Why Choose PhonePe?</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Easy Transactions</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- One App For All Your Payments</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Your Bank Account Is All You Need</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Multiple Payment Modes</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- PhonePe Merchants Network</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Multiple Ways to Pay</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>  1. Direct Transfer & More</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>  2. QR Code Payments</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Third row with two columns for additional images and features
    col5, col6 = st.columns(2)

    with col5:
        st.write(" ")
        st.markdown("<h4 style='color: white;'>Benefits of Using PhonePe</h4>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Earn Great Rewards</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- No Wallet Top-Up Required</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Pay Directly From Any Bank Account</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: white;'>- Instant and Free Transactions</p>", unsafe_allow_html=True)

    with col6:
        phonepe_benefits_image = Image.open(r"C:\Users\Ramachandran T\Desktop\phonepe\phonepe2.png")
        st.image(phonepe_benefits_image, width=600)


elif select == "Data Exploration":
    
    Tab1,Tab2,Tab3 = st.tabs(["Aggreated Data","Map Data","Top Data"])

    with Tab1:
        
        Data_Analysis1= st.radio("Select one Aggreated Data",[":red[Aggreated Insurance Data]",":red[Aggreated Transaction Data]",":red[Aggreated User Data]"])

        if Data_Analysis1 == ":red[Aggreated Insurance Data]":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the year]",agg_insurance["Years"].min(),agg_insurance["Years"].max(),agg_insurance["Years"].min())
            Tra_amt_count=Transaction_amount_count(agg_insurance, years)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider(":red[select the Quarter]",Tra_amt_count["Quarter"].min(),Tra_amt_count["Quarter"].max(),Tra_amt_count["Quarter"].min())
            Transaction_amount_count_qua(Tra_amt_count,quarters)
    
        elif Data_Analysis1 == ":red[Aggreated Transaction Data]":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the year]",agg_transaction["Years"].min(),agg_transaction["Years"].max(),agg_transaction["Years"].min())
            Agg_Tra_amt_count=Transaction_amount_count(agg_transaction, years)

            col1,col2=st.columns(2)
            with col1:

                states =st.selectbox(":red[Select the States]", Agg_Tra_amt_count['states'].unique())
            Agg_Transaction_Type(Agg_Tra_amt_count, states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the Quarter]",Agg_Tra_amt_count["Quarter"].min(),Agg_Tra_amt_count["Quarter"].max(),Agg_Tra_amt_count["Quarter"].min())
            Agg_Tra_amt_count_qua = Transaction_amount_count_qua(Agg_Tra_amt_count,quarters)

            col1,col2=st.columns(2)
            with col1:

                states1 =st.selectbox(":red[Select the State]", Agg_Tra_amt_count_qua['states'].unique())
            Agg_Transaction_Type(Agg_Tra_amt_count_qua, states1)

        elif Data_Analysis1 == ":red[Aggreated User Data]":
            
            col1,col2=st.columns(2)
            with col1:

                years = st.slider(":red[select the year]",agg_user["Years"].min(),agg_user["Years"].max(),agg_user["Years"].min())
            Agg_user_brd_count_yr= agg_user_year_fig1(agg_user, years)

            col1,col2=st.columns(2)
            with col1:

                quarters=st.slider("select the Quarter",Agg_user_brd_count_yr["Quarter"].min(),Agg_user_brd_count_yr["Quarter"].max(),Agg_user_brd_count_yr["Quarter"].min())
            Agg_user_brd_count_qua=agg_user_year_fig2(Agg_user_brd_count_yr ,quarters) 

            col1,col2=st.columns(2)
            with col1:

                states =st.selectbox(":red[Select the State]", Agg_user_brd_count_qua['states'].unique())
            agg_user_year_fig3(Agg_user_brd_count_qua, states) 


    with Tab2:
        
        Data_Analysis2= st.radio("Select one Map Data",[":red[Map Insurance Data]",":red[Map Transaction Data]",":red[Map User Data]"])

        if Data_Analysis2 == ":red[Map Insurance Data]":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years]",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
            map_insr_tran_amt_ct=Transaction_amount_count(map_insurance, years)

            col1,col2=st.columns(2)
            with col1:

                states =st.selectbox(":red[Select the map State]", map_insr_tran_amt_ct['states'].unique())
            map_insurance_Dist(map_insr_tran_amt_ct, states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the map Quarter]",map_insr_tran_amt_ct["Quarter"].min(),map_insr_tran_amt_ct["Quarter"].max(),map_insr_tran_amt_ct["Quarter"].min())
            map_Insur_amt_count_qua = Transaction_amount_count_qua(map_insr_tran_amt_ct,quarters)

            col1,col2=st.columns(2)
            with col1:

                states1 =st.selectbox(":red[Select the map State]", map_Insur_amt_count_qua['states'].unique())
            map_insurance_Dist(map_Insur_amt_count_qua, states1)

        elif Data_Analysis2 == ":red[Map Transaction Data]":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years]",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            map_trans_tran_amt_ct=Transaction_amount_count(map_transaction, years)

            col1,col2=st.columns(2)
            with col1:

                states =st.selectbox(":red[Select the State]", map_trans_tran_amt_ct['states'].unique())
            map_insurance_Dist(map_trans_tran_amt_ct, states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the map Quarters]",map_trans_tran_amt_ct["Quarter"].min(),map_trans_tran_amt_ct["Quarter"].max(),map_trans_tran_amt_ct["Quarter"].min())
            map_trans_amt_count_qua = Transaction_amount_count_qua(map_trans_tran_amt_ct,quarters)

            col1,col2=st.columns(2)
            with col1:

                states1 =st.selectbox(":red[Select the map States]", map_trans_amt_count_qua['states'].unique())
            map_insurance_Dist(map_trans_amt_count_qua, states1)

        elif Data_Analysis2 == ":red[Map User Data]":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years for Map User]",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            map_user_year=map_user_fig1(map_user, years)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the Quarter for Map User]",map_user_year["Quarter"].min(),map_user_year["Quarter"].max(),map_user_year["Quarter"].min())
            map_user_year_qua = map_user_fig2(map_user_year,quarters)

            col1,col2=st.columns(2)
            with col1:

                states1 =st.selectbox(":red[Select the States for Map User]", map_user_year_qua['states'].unique())
            map_user_fig3(map_user_year_qua, states1)

    with Tab3:
        
        Data_Analysis3= st.radio("Select one Top Data",[":red[Top Insurance Data]",":red[Top Transaction Data]",":red[Top User Data]"])

        if Data_Analysis3 == ":red[Top Insurance Data]":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years for Top Insurance]",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            Top_Insur_tran_amt_ct_year=Transaction_amount_count(top_insurance, years)
            
            col1,col2=st.columns(2)
            with col1:
            
                states1 =st.selectbox(":red[Select the States for Top Insurance]", Top_Insur_tran_amt_ct_year['states'].unique())
            Top_insurance_fig1(Top_Insur_tran_amt_ct_year, states1)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the Quarter for Top_Trans]",Top_Insur_tran_amt_ct_year["Quarter"].min(),Top_Insur_tran_amt_ct_year["Quarter"].max(),Top_Insur_tran_amt_ct_year["Quarter"].min())
            Top_Insur_year_qua = Transaction_amount_count_qua(Top_Insur_tran_amt_ct_year,quarters)

            
        elif Data_Analysis3 == ":red[Top Transaction Data]":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years for Top_Trans]",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            Top_transaction_amt_ct_year=Transaction_amount_count(top_transaction, years)
            
            col1,col2=st.columns(2)
            with col1:
            
                states1 =st.selectbox(":red[Select the States for Top_Trans]", Top_transaction_amt_ct_year['states'].unique())
            Top_insurance_fig1(Top_transaction_amt_ct_year, states1)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider(":red[select the Quarter for Top_Trans]",Top_transaction_amt_ct_year["Quarter"].min(),Top_transaction_amt_ct_year["Quarter"].max(),Top_transaction_amt_ct_year ["Quarter"].min())
            Top_Trans_year_qua = Transaction_amount_count_qua(Top_transaction_amt_ct_year,quarters)

        elif Data_Analysis3 == ":red[Top User Data]":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider(":red[select the years for Top_user]",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_year = top_user_fig1(top_user,years)

            col1,col2=st.columns(2)
            with col1:
            
                states =st.selectbox(":red[Select the States for Top_users]", top_user_year['states'].unique())
            Top_user_fig2(top_user_year, states)       


elif select == "Top Charts":
    
    question=st.selectbox("1.select the Question", ["1.Transaction Amount and Count of Aggregated Insurance",
                                                   "2.Transaction Amount and Count of MAP Insurance",
                                                   "3.Transaction Amount and Count of TOP Insurance",
                                                   "4.Transaction Amount and Count of Aggregated Transaction",
                                                   "5.Transaction Amount and Count of MAP Transaction",
                                                   "6.Transaction Amount and Count of TOP Transaction",
                                                   "7.Transaction Count of Aggregated user",
                                                   "8.Registered users of MAP user",
                                                   "9.APP opens of MAP User",
                                                  "10.Registered users of TOP user", 
                                                    ])
    
    if question == "1.Transaction Amount and Count of Aggregated Insurance":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("aggregated_insurance")

        st.subheader("Transaction Count")
        Top_chart_Transaction_count("aggregated_insurance")

    elif question == "2.Transaction Amount and Count of MAP Insurance":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("map_insurance")
        
        st.subheader("Transaction Count")
        Top_chart_Transaction_count("map_insurance")
    
    elif question == "3.Transaction Amount and Count of TOP Insurance":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("top_insurance")
        
        st.subheader("Transaction Count")
        Top_chart_Transaction_count("top_insurance")

    elif  question == "4.Transaction Amount and Count of Aggregated Transaction":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("Aggregated_transaction")
        
        st.subheader("Transaction Count")
        Top_chart_Transaction_count("Aggregated_transaction")
    
    elif  question == "5.Transaction Amount and Count of MAP Transaction":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("map_transaction")
        
        st.subheader("Transaction Count")
        Top_chart_Transaction_count("map_transaction")

    elif  question == "6.Transaction Amount and Count of TOP Transaction":

        st.subheader("Transaction Amount")
        Top_chart_Transaction_amount("top_transaction")
        
        st.subheader("Transaction Count")
        Top_chart_Transaction_count("top_transaction")
    
    elif  question == "7.Transaction Count of Aggregated user":

        st.subheader("Transaction Count")
        Top_chart_Transaction_count("aggregated_user")
    
    elif  question == "8.Registered users of MAP user":

        states=st.selectbox("select the states",map_user["states"].unique())
        st.subheader("Registered user")
        Top_chart_Registered_User("map_user",states)
    
    elif  question == "9.APP opens of MAP User":

        states=st.selectbox("select the states",map_user["states"].unique())
        st.subheader("APP_OPENS")
        Top_chart_appopens("map_user",states)
    
    elif  question == "10.Registered users of TOP user":

        st.subheader("Registered Users")
        Top_chart_Registered_Users("top_user")