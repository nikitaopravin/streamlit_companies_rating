import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.linear_model import LinearRegression


st.header('Restaurant tip research')

st.markdown('''This **exploration** show some **dependencies and relationships** 
            between different features of researched data set. 
            \nYou can use default data set, or your own with necessary columns. Load it below!''')

tips = pd.read_csv('tips.csv')
tips.set_index('Unnamed: 0', inplace=True)
neces_columns = tips.columns.tolist()

uploded_file = st.file_uploader(f"Necessary columns: {', '.join(neces_columns)}")
    
if uploded_file is not None:    
    try:
        temp = pd.read_csv(uploded_file)
        temp_columns = temp.columns.tolist()
        
        if set(neces_columns).issubset(temp_columns):
            tips = temp
        else:
            st.markdown(f':red[**File don\'t have necessary columns: {neces_columns}**]')

    except:
        st.markdown(':red[**Your file is not correct!**]') 

with st.expander('Current data frame'):
    st.write(tips.head(5))


st.subheader('Count of bills by bill size')

fig, ax = plt.subplots(figsize=(10, 4))
sns.histplot(tips, x='total_bill', binwidth=1)
ax.set_xlabel('bill size')
ax.set_ylabel('count')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
st.pyplot(fig)

st.subheader('Relationsips between tip and total bill')

fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(tips, x='total_bill', y='tip', hue='time')
ax.set_xlabel('total bill')
ax.set_ylabel('tip')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
st.pyplot(fig)

st.subheader('Relationship between total bill and tips based on the number of visitors')

fig, ax = plt.subplots(figsize=(10, 4))
sns.scatterplot(tips, x='total_bill', y='tip', size='size', hue='time', sizes=(10, 200))
ax.set_xlabel('total bill')
ax.set_ylabel('tip')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
ax.legend()
st.pyplot(fig)

st.subheader('Mean bill size by the week days')

fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(tips, x='day', y='total_bill', errorbar='ci', width=0.5)
ax.set_xlabel('days of the week')
ax.set_ylabel('mean bill')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{y} $'))
st.pyplot(fig)

st.subheader('Relationships between tip size and day of the week considering sex')

fig, ax = plt.subplots(figsize=(10,4))
sns.scatterplot(tips, x='tip', y='day', hue='sex')
ax.set_xlabel('tip')
ax.set_ylabel('day of the week')
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)} $'))
st.pyplot(fig)

st.subheader('Bill size by day of the week considering time')

fig, ax = plt.subplots(figsize=(10,4))
sns.boxplot(tips, x='day', y='total_bill', hue='time')
ax.set_xlabel('day of the week')
ax.set_ylabel('bill size')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x)} $'))
st.pyplot(fig)

st.subheader('Histograms for tip to lunch and dinner')

g = sns.displot(data=tips, x='tip', col='time', kde=True)
g.set_titles('{col_name}')
g.set_axis_labels('tip', 'count')
st.pyplot(g)

st.subheader('Relationships between total bill and tip for male and female (considering smokers)')

g = sns.relplot(data=tips, x='total_bill', y='tip', col='sex', hue='smoker')
g.set_titles('{col_name}')
g.set_xlabels('total bill')
st.pyplot(g)

st.subheader('Number of people by tip')

fig, ax = plt.subplots(figsize=(10, 4))
sns.boxplot(tips, x='size', y='tip', whis=[0, 100], width=.5, palette='vlag')
sns.stripplot(tips, x='size', y='tip', hue='sex', palette='dark:#5A9_r', jitter=0.1, size=3.5)
ax.set_xlabel('num of people')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)} $'))
st.pyplot(fig)

st.sidebar.subheader('Prediction of tip')
user_total_bill = st.sidebar.slider('What is your total bill?', 0, 50, 20)
user_visitors_count = st.sidebar.slider('How many of you?', 1, 6, 2)
LinearRG = LinearRegression()
result = LinearRG.fit(tips[['total_bill', 'size']].values.reshape(-1,2), y=tips['tip'].values)
predict_tip = result.predict([[user_total_bill, user_visitors_count]])
st.sidebar.markdown(f'Probably tip will be: **{round(predict_tip[0], 2)} $**')


