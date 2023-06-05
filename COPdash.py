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


def get_data_to_df():
    base_id = 'appFhUaPCtM80dgZY'

    desired_fields = [
        'Response ID',
        'Name',
        'Email',
        'Milestone Name',
        'Interest_primary_proper',
        'A4',
        'A26 Count',
        'User Profile Name',
        'Salary Name',
    ]

    records = Table(APIKEY, base_id, 'Diagnostic Results')
    data = records.all(view="COP DashView", fields=desired_fields)
    raw_df = pd.DataFrame.from_records(data)
    df = pd.concat([raw_df, raw_df['fields'].apply(pd.Series)],
                   axis=1).drop(['fields'], axis=1)

    df['Milestone Name'] = df['Milestone Name'].apply(one)
    df['User Profile Name'] = df['User Profile Name'].apply(one)
    df['Salary Name'] = df['Salary Name'].apply(one)

    return df


df = get_data_to_df()

# All data created at this point
# Milestone, Profile, Primary Interest, Top Drivers, Salary Expectations, Number of Experiences
# Grad Year, Myth Believer

st.sidebar.header("Filter by Partner")
partnersource = st.sidebar.multiselect(
    "Select your partner name:", options=df["A4"].unique(), default=df["A4"].unique())

# df = big_df.query("`A4` == @partnersource")


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


milestone_chart = df['Milestone Name'].value_counts().reset_index().rename(
    columns={'index': 'Milestone', "Milestone Name": "Number of Students"}
)
# milestone_chart['Milestone'] = milestone_chart['Milestone'].astype(ms_type)


profile_chart = df['User Profile Name'].value_counts().reset_index()
# profile_chart['Clarity Profile'] = profile_chart['Clarity Profile'].astype(
#     pf_type)

salary_chart = df['Salary Name'].value_counts().reset_index().sort_index().rename(
    columns={'index': 'Salary Expectation', 'Salary Name': 'Number of Students'})
# salary_chart['Salary Expectation'] = salary_chart['Salary Expectation'].astype(
#     salary_type)

interests_chart = df['Interest_primary_proper'].value_counts(
).sort_index().reset_index().rename(columns={'Interest_primary_proper': 'Number of Students', 'index': "Industry of Interest"})

print(milestone_chart)
print(interests_chart)
print(profile_chart)
# create plotly figs

figure_1 = px.bar(milestone_chart.sort_values(by='Milestone'), y='Milestone', x='Number of Students', color='Milestone',
                  color_discrete_map={
                      'Clarity': "#00A3E1", 'Alignment': "#85C540",
                      'Search Strategy': "#D04D9D", 'Interviewing & Advancing': "#FFC507"})

figure_2 = px.bar(profile_chart.sort_values(by='Clarity Profile'),
                  x='Clarity Profile', y='Number of Students')

figure_3 = px.bar(salary_chart.sort_values(by="Salary Expectation"),
                  x="Salary Expectation", y="Number of Students", color='Salary Expectation')

figure_4 = px.bar(interests_chart, y='Industry of Interest',
                  x='Number of Students', color='Industry of Interest')

fig_exp1 = px.histogram(df, x="A26 Count", nbins=6, title="6 bins exp")
fig_exp2 = px.histogram(df, x="A26 Count", nbins=4, title="4 bins exp")


# display via streamlit

st.metric(label="Number of Seekr Takers", value=df.shape[0])


st.plotly_chart(figure_1, use_container_width=True)
st.plotly_chart(figure_2, use_container_width=True)
st.plotly_chart(figure_3, use_container_width=True)
st.plotly_chart(figure_4, use_container_width=True)
st.plotly_chart(fig_exp1, use_container_width=True)
st.plotly_chart(fig_exp2, use_container_width=True)
