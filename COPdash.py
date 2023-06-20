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

big_df = pd.read_csv('MPPplusD2S.csv')

big_df['Archetypes'] = big_df['User Profile Name'].map(
    {
        'WF1': "Disinterested",
        'WF2': "Self-Conscious",
        'WF3': "Distracted",
        'WF4': "Disinterested",
        'WF5': "Self-Conscious",
        'WF6': "Distracted",
        'WF7': "Tentative",
        'WF8': "Tentative",
        'WF9': "Intuitive",
        'WF10': "Passed Clarity",
        'WF11': "Adamant",
        'WF12': "Adamant",
        'WF13': "Intuitive",
        'WF14': "Passed Clarity",
    }
)

big_df['Graduation_Year'].replace({"20267":"2026",
                                   "After 2025":"2026",
                                   "Before 2018":"2017"},inplace=True)


milestone_order = ['Clarity', 'Alignment',
                   'Search Strategy', 'Interviewing & Advancing', ]
pf_order = ['WF1', 'WF2', 'WF3', 'WF4', 'WF5', 'WF6', 'WF7',
            'WF8', 'WF9', 'WF10', 'WF11', 'WF12', 'WF13', 'WF14']

archetype_order = ["Disinterested", "Self-Conscious","Distracted", "Tentative","Intuitive","Adamant","Passed Clarity"]
salary_order = ["Honestly, I haven't thought about this",
                "Less than $40,000",
                "Between $40,000 and $59,999",
                "Between $60,000 and $79,999",
                "Between $80,000 and $99,999",
                "$100,000 +"]

ms_type = CategoricalDtype(categories=milestone_order, ordered=True)
pf_type = CategoricalDtype(categories=pf_order, ordered=True)
salary_type = CategoricalDtype(categories=salary_order, ordered=True)
arc_type = CategoricalDtype(categories=archetype_order, ordered=True)

big_df['Milestone Name'] = big_df['Milestone Name'].astype(ms_type)
big_df['User Profile Name'] = big_df['User Profile Name'].astype(pf_type)
big_df['Archetypes'] = big_df['Archetypes'].astype(arc_type)
big_df['Salary Name'] = big_df['Salary Name'].astype(salary_type)

# All data created at this point
# Milestone, Profile, Primary Interest, Top Drivers, Salary Expectations, Number of Experiences
# Grad Year, Myth Believer

st.sidebar.header("Filter by Partner")
partner = st.sidebar.multiselect(
    "Select your partner name:", options=big_df["Partner_Affiliation"].unique(), default=sorted(big_df["Partner_Affiliation"].unique()))

st.sidebar.header("Filter by Year")
gradyr = st.sidebar.multiselect(
    "Select student college graduation year:", options=big_df["Graduation_Year"].unique(), default=sorted(big_df["Graduation_Year"].unique()))

df = big_df.query(
    "`Partner_Affiliation` == @partner & `Graduation_Year` == @gradyr")


# milestone_order = ['Clarity', 'Alignment',
#                    'Search Strategy', 'Interviewing & Advancing', ]
# pf_order = ['WF1', 'WF2', 'WF3', 'WF4', 'WF5', 'WF6', 'WF7',
#             'WF8', 'WF9', 'WF10', 'WF11', 'WF12', 'WF13', 'WF14']
# salary_order = ["Honestly, I haven't thought about this",
#                 "Less than $40,000",
#                 "Between $40,000 and $59,999",
#                 "Between $60,000 and $79,999",
#                 "Between $80,000 and $99,999",
#                 "$100,000 +"]

# ms_type = CategoricalDtype(categories=milestone_order, ordered=True)
# pf_type = CategoricalDtype(categories=pf_order, ordered=True)
# salary_type = CategoricalDtype(categories=salary_order, ordered=True)


# create data for mini-charts

m = df['Milestone Name'].value_counts().sort_index()

arc = df['Archetypes'].value_counts().sort_index()

s = df['Salary Name'].value_counts().sort_index()

i = df['Interest_primary_proper'].value_counts().sort_index()

denom = df['Response ID'].count()
myth = round(100 * df.loc[df['Mythbeliever']>3]['Mythbeliever'].count() / denom)
high_conf = round( 100* df.loc[df['User Profile Name'].isin(['WF11', 'WF12', 'WF13', 'WF14'])]['User Profile Name'].count() / denom)
nointerest = round(100 * df['Interest_primary_proper'].isna().sum() / denom)
claritypct = round(100* df.loc[df['Milestone Name'] == "Clarity"]['Milestone Name'].count() / denom)
# i = df['Interest_primary_proper'].value_counts()


# create plotly figs

figure_1 = px.bar(m, y=m.index, x=m, title="Milestone",color=m.index, color_discrete_map={
    'Clarity': "#00A3E1", 'Alignment': "#85C540",
    'Search Strategy': "#D04D9D", 'Interviewing & Advancing': "#FFC507"})
figure_1.update_layout(
    xaxis_title="Number of Students", yaxis_title="Milestone",showlegend=False
)
print(pd.__version__)

figure_2 = px.bar(arc,
                  x=arc.index, y=arc, color=arc.index,title="Clarity Profiles")
figure_2.update_layout(yaxis_title="Number of Students",
                       xaxis_title="Profile",
                       showlegend=False)

# figure_6 = 


figure_3 = px.bar(s,
                  x=s.index, y=s, color=s.index,title="Salary Expectations")
figure_3.update_layout(yaxis_title="Number of Students",
                       xaxis_title="Salary Range",
                       showlegend=False)

figure_4 = px.bar(i,
                  y=i.index, x=i, color=i.index)
figure_4.update_layout(yaxis_title="Career Interest",xaxis_title="Number of Students",showlegend=False)


# figure_5 = px.bar(myth)

# figure_6 = px.histogram(df, x='Mythbeliever', nbins=5,
#                         title="alt to myth chart above")

fig_exper = px.histogram(df, x="A26 Count", nbins=6)
fig_exper.update_layout(yaxis_title="Number of Students",xaxis_title="Number of Experiences",showlegend=False)



# # display via streamlit
st.title("Seekr x Discovery Data Dashboard")

st.subheader("Welcome to the Discovery Data Dashboard! In your Community of Practice, use this tool to explore through our data and learn about your student community.")



cola, colb = st.columns([8,4])

with colb:
    # st.subheader("Number of Seekr Takers")
    # st.metric(label="",value=f"{df.shape[0]} Students")
    st.markdown("### Milestone")
    st.markdown(f"When you host a resume workshop or mock interviews, you are serving a minority of students. {claritypct}% of your student land at Clarity and are simply not ready to benefit from that kind of programming.")

with cola:
    
    st.plotly_chart(figure_1, use_container_width=True)

col1,col2 = st.columns([8,4])
with col2:
    st.markdown("### Clarity Profiles")
    st.markdown("""
        We identified 6 profiles of students at Clarity. We use this information to provide tailored guidance and a highly personalized experience to each student. Each student needs something different on their Milestones journey.
    """)
    with st.expander("Learn more about the profiles"):
        st.markdown("""
        Disinterested: This student hasn't found any interesting career options. This might be due to not knowing about enough industries, not having enough experience, or a general lack of interest in their career overall.   

        Self-Conscious: This student is most concerned with their own qualifications. They might not know the available career paths for their skillset or they might not feel qualified enough to pursue their real interest.  

        Distracted: This student is interested in many career options and is struggling to pick just one. They might have multiple passions and are trying to pursue them all at once. Or maybe they're paralyzed by the possibilities.    

        Tentative: This student has a career interest but we're concerned they might be making an uninformed decision. They haven't demonstrated enough exposure and they aren't overly committed to their interest.  
        
        Intuitive: This student is probably pursuing the right field but they're unable to articulate strong reasons for their interest. In digging deeper, students sometimes discover buried passions.  

        Adamant: This student is highly confident and committed to their interest but don't have enough exposure. We're concerned they're making an uninformed decision. We address this carefully without hurting their aspirations.  
        """)

with col1:
    st.plotly_chart(figure_2, use_container_width=True)

st.write("---")
colu1,colu2,colu3,colu4 = st.columns(4)

with colu1:
    st.subheader("Number of Seekr Takers")
    st.metric(label="",value=f"{df.shape[0]} Students")
with colu2:
    st.subheader("Mythbelievers")
    st.metric(label="",value=f"{myth} %")
    st.markdown("Students who believe a few too many myths about the job search, like thinking they can only apply to jobs related to their major.")
with colu3:
    st.subheader("No Interest")
    st.metric(label="",value=f"{nointerest} %")
    st.markdown("Students who haven't yet identified a career interest.")

with colu4:
    st.subheader("Found Passion")
    st.metric(label="",value=f"{high_conf} %")
    st.markdown("Students who are extremely confident they know what career field they want to pursue.")
    
st.write("---")
colx, coly = st.columns([8,4])

with colx:
    st.markdown("### Industry of Interest")
    st.plotly_chart(figure_4, use_container_width=True)

with coly:
    st.markdown("The field a student wants their first job in is considered their Industry of Interest. Below are these students' top 5 interests.")
    st.write(i.sort_values(ascending=False).head(5))


st.write("---")
colua,colub = st.columns([8,4])

with colua:
    st.plotly_chart(figure_3, use_container_width=True)

with colub:
    st.markdown("### Salary Expectations")
    st.markdown("Salary expectations show us what salary range students are looking for in a first job. This is a common source of misalignment between their interest and what a realistic salary in that industry can be.")


colux,coluy = st.columns([8,4])

with coluy:
    st.markdown("### Number of Experiences")
    st.markdown("We define an experience as any work or volunteer experience longer than 6 months. Most students list that they've had 2-3 experiences but we suspect that they're still undercounting what they've done.")

with colux:
    st.plotly_chart(fig_exper, use_container_width=True)
