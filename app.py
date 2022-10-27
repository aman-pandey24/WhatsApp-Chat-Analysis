import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    #st.dataframe(df)#---> to show dataframe of whatsapp chat
    user_list=df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"All Member")
    selected_user=st.sidebar.selectbox("Show Ananlysis with respect to",user_list)
    ## stats analysis
    if st.sidebar.button("Show Analysis"):
        num_messages,total_words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        ## monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline["time"], timeline["message"],color="red")
        plt.xticks(rotation=60)
        st.pyplot(fig)


        ## Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline["only_date"],daily_timeline["message"],color="black")
        plt.xticks(rotation=60)
        st.pyplot(fig)


        ## activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            plt.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            plt.bar(busy_month.index, busy_month.values,color="orange")
            st.pyplot(fig)
        st.title("Actvity HeatMap")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)


    ## finding busiest users in group(Group lvele)
    if selected_user=="All Member":
        st.title("Most Busy Users")
        x,new_df=helper.fetch_most_busy_users(df)
        fig,ax=plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index, x.values,color="red")
            plt.xticks(rotation=60)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    ## Word Cloud
    df_wc=helper.create_wordcloud(selected_user,df)
    st.title("WordCloud")
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    ## most common words
    most_common_df=helper.most_common_word(selected_user,df)
    fig, ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation=60)
    st.title("Most Common Word")
    st.pyplot(fig)
    ## emoji analysis
    emoji_df=helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax=plt.subplots()
        palette_color = sns.color_palette('bright')
        plt.pie(emoji_df[1].head(),colors=palette_color,labels=emoji_df[0].head(),
               autopct="%0.2f",explode=[0.2,0.1,0.1,0.1,0.1])
        st.pyplot(fig)










