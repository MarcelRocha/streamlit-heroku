import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt


def ct_hist(col, df):
    hist = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(col, bin=True),
        y='count()', tooltip=[col, 'count()']
    ).interactive()
    return hist

def ct_correlation(df, cols):
    cor_data = (df[cols]).corr().stack().reset_index().rename(
        columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode(x='variable2:O', y='variable:O')
    text = base.mark_text().encode(text='correlation_label',
                                   color=alt.condition(alt.datum.correlation > 0.5, alt.value('white'),
                                                       alt.value('black')))

    # The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
        color='correlation:Q')

    return cor_plot + text


def main():
    st.image('logo.png', width=200)
    st.title('Exploratory Data Analysis')
    st.subheader('Example of data analysis and visualization\n'
                 '* Source: http://mlr.cs.umass.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv')
    st.sidebar.image('cn.png', width=200)
    st.sidebar.title('Challenge by:')
    st.sidebar.markdown('* AceleraDev Data Science')
    st.sidebar.title('Author:')
    st.sidebar.markdown('* Marcel Rocha Nascimento')
    st.sidebar.title('Contact me:')
    st.sidebar.markdown('* marcel.nanoufrj@gmail.com')
    st.sidebar.title('Find out more:')
    st.sidebar.markdown('* [LinkedIn](https://www.linkedin.com/in/marcel-rocha-nascimento-8185a6148/) - '
                        '[GitHub](https://github.com/MarcelRocha)')
    #dataset_url = 'http://mlr.cs.umass.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'
    df = pd.read_csv('winequality-red.csv')
    data_col = list(df.columns)
    st.markdown('**Dataframe visualization**')
    number = st.slider('Choose the number of rows you want to see', min_value=1, max_value=20)
    st.dataframe(df.head(number))
    st.title('Statistics')
    col = st.selectbox('Select the feature:', data_col)
    if col is not None:
        st.markdown('Select analysis:')
        mean = st.checkbox('Mean')
        if mean:
            st.markdown(df[col].mean())
        median = st.checkbox('Median')
        if median:
            st.markdown(df[col].median())
        data_std = st.checkbox('Standard Deviation')
        if data_std:
            st.markdown(df[col].std())
        describe = st.checkbox('Statistics (summary)')
        if describe:
            st.dataframe(df[col].describe())
    st.title('Data Visualization')
    st.markdown('Select your visualization')
    histogram = st.checkbox('Histogram')
    if histogram:
        col_num = st.selectbox('Select a column: ', data_col, key='unique')
        st.markdown('Histogram')
        st.write(ct_hist(col_num, df))
    distribution = st.checkbox('Distribution Chart')
    if distribution:
        col_dist = st.selectbox('Select a column: ', data_col, key='unique')
        sns.distplot(df[col_dist])
        plt.xlabel('')
        plt.title(col_dist, {'fontsize': 20})
        st.pyplot()
    correlation = st.checkbox('Correlation')
    if correlation:
        st.markdown('Correlation Heatmap')
        st.write(ct_correlation(df, data_col))


if __name__ == '__main__':
    main()
