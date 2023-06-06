from more_itertools import one
from pandas.api.types import CategoricalDtype
import pandas as pd
import streamlit as st
import plotly.express as px
from pyairtable import Table
from decouple import config
# APIKEY = config('AIRTABLE_API_KEY')
APIKEY = st.secrets["AT_KEY"]

# setting streamlit page configurations
st.set_page_config(
    page_title="Basta x Seekr Community of Practice",
    page_icon="✅",
    layout="wide",
)


# def get_data_to_df():
#     base_id = 'appFhUaPCtM80dgZY'

#     desired_fields = [
#         'Response ID',
#         'Name',
#         'Email',
#         'Milestone Name',
#         'Interest_primary_proper',
#         'A4',
#         'A26 Count',
#         'User Profile Name',
#         'Salary Name',
#         'Grad Edu Status'
#     ]

#     records = Table(APIKEY, base_id, 'Diagnostic Results')
#     data = records.all(view="COP DashView", fields=desired_fields)
#     raw_df = pd.DataFrame.from_records(data)
#     df = pd.concat([raw_df, raw_df['fields'].apply(pd.Series)],
#                    axis=1).drop(['fields'], axis=1)

#     df['Milestone Name'] = df['Milestone Name'].apply(one)
#     df['User Profile Name'] = df['User Profile Name'].apply(one)
#     df['Salary Name'] = df['Salary Name'].apply(one)

#     return df


# big_df = get_data_to_df()

big_df = pd.read_csv('compiled.csv')

# All data created at this point
# Milestone, Profile, Primary Interest, Top Drivers, Salary Expectations, Number of Experiences
# Grad Year, Myth Believer

st.sidebar.header("Filter by Partner")
partner = st.sidebar.multiselect(
    "Select your partner name:", options=big_df["Partner_Affiliation"].unique(), default=big_df["Partner_Affiliation"].unique())

df = big_df.query("`Partner_Affiliation` == @partner")


milestone_order = ['Clarity', 'Alignment',
                   'Search Strategy', 'Interviewing & Advancing', ]
pf_order = ['WF1', 'WF2', 'WF3', 'WF4', 'WF5', 'WF6', 'WF7',
            'WF8', 'WF9', 'WF10', 'WF11', 'WF12', 'WF13', 'WF14']
salary_order = ["Honestly, I haven't thought about this",
                "Less than $40,000",
                "Between $40,000 and $59,999",
                "Between $60,000 and $79,999",
                "Between $80,000 and $99,999",
                "$100,000 +"]

ms_type = CategoricalDtype(categories=milestone_order, ordered=True)
pf_type = CategoricalDtype(categories=pf_order, ordered=True)
salary_type = CategoricalDtype(categories=salary_order, ordered=True)


# create data for mini-charts

milestone_chart = df['Milestone Name'].value_counts()

profile_chart = df['User Profile Name'].value_counts()

salary_chart = df['Salary Name'].value_counts()

interests_chart = df['Interest_primary_proper'].value_counts()
myth_chart = df['Mythbeliever'].astype('float').value_counts()
# interests_chart = df['Interest_primary_proper'].value_counts()


# create plotly figs

figure_1 = px.bar(milestone_chart, y=milestone_chart.index, x=milestone_chart, color=milestone_chart.index, color_discrete_map={
    'Clarity': "#00A3E1", 'Alignment': "#85C540",
    'Search Strategy': "#D04D9D", 'Interviewing & Advancing': "#FFC507"})
figure_1.update_layout(
    xaxis_title="Number of Students", yaxis_title="Milestone"
)

figure_2 = px.bar(profile_chart,
                  x=profile_chart.index, y=profile_chart, color=profile_chart.index)
figure_2.update_layout(yaxis_title="Number of Students",
                       xaxis_title="Profile")


figure_3 = px.bar(salary_chart,
                  x=salary_chart.index, y=salary_chart, color=salary_chart.index)

figure_4 = px.bar(interests_chart.sort_index(),
                  x=interests_chart.index, y=interests_chart, color=interests_chart.index)

figure_5 = px.bar(myth_chart)

fig_exp1 = px.histogram(df, x="A26 Count", nbins=6, title="6 bins exp")
fig_exp2 = px.histogram(df, x="A26 Count", nbins=14, title="14 bins exp")


# # display via streamlit

st.metric(label="Number of Seekr Takers", value=df.shape[0])


st.plotly_chart(figure_1, use_container_width=True)
st.plotly_chart(figure_2, use_container_width=True)
st.plotly_chart(figure_3, use_container_width=True)
st.plotly_chart(figure_4, use_container_width=True)
st.plotly_chart(figure_5, use_container_width=True)
st.plotly_chart(fig_exp1, use_container_width=True)
st.plotly_chart(fig_exp2, use_container_width=True)
