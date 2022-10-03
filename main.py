import streamlit as st
from io import StringIO
import pandas as pd
import plotly_express as px
st.markdown("# WhatsApp Chat Analyzer")
st.markdown("##### Analyze your chat with others on WhatsApp, know which one of you is **`رغاى`** 😂 ")
# sidebar
st.sidebar.markdown("""
# Options
بص يابا هتتبع الخطوات دى 👇:
1) Open the individual chat `only with one person`.
2) Tap options > More > Export chat.
3) Choose export without media.
 هيقوم فاتحلك اختيارات كده ف الافضل ارفعه درايف وحمله ع الموقع بعدها😃
""")
st.sidebar.markdown("## Upload the text file")
st.sidebar.markdown("#### Choose whats type")
type = st.sidebar.selectbox("WhatsApp Type",["سالك","غير سالك"])
file = st.sidebar.file_uploader("The file",type="txt")
st.sidebar.markdown("متخفش وربنا مفيش حد هيشوف الداتا 😂 ")
# start working with the file
# convert and get the final data
#----------------------------------helper functions --------------------------------
def get_final(df,month):
    d = df[df["date"].dt.month == month]
    dates = d["date"].unique()
    d = d.groupby([d["date"],d["sender"]])["sender"].count().to_frame()
    senders = list(df.sender.unique())
    sender_1_messages = []
    sender_2_messages =[]
    for i in dates:
        if len(d.loc[i].index) == 2:
            sender_1_messages.append(d.loc[i].loc[senders[0]].values[0])
            sender_2_messages.append(d.loc[i].loc[senders[1]].values[0])
        else :
            # get the sender :
            sender = d.loc[i].index[0]
            index = sender.index(sender)
            if index == 0 :
                sender_1_messages.append(d.loc[i].loc[senders[0]].values[0])
                sender_2_messages.append(0)
            elif index ==1:
                sender_2_messages.append(d.loc[i].loc[senders[1]].values[0])
                sender_1_messages.append(0)
    ms = pd.DataFrame({
        "date":dates,
        f"{senders[0]}":sender_1_messages,
        f"{senders[1]}":sender_2_messages
    })
    final = ms.melt(id_vars=["date"],value_vars=senders)
    return final
#-----------------------------------------------------------------------------------
@st.cache
def get_data_salek(file_name):
    stringio = StringIO(file_name.getvalue().decode("utf-8"))
    lines = stringio.readlines()
    #choose only the linse that start with the dataes
    lines = ( line for line in lines[1:] )
    chat_lines = []
    for l in lines:
        if len(l) >10 :
            if (l[0].isdigit()) & ( "/" in l[0:10]):
                chat_lines.append((l))
    df = pd.Series(chat_lines).str.split("-",expand=True).iloc[:,0:2]
    df[["sender","message"]] = df[1].str.split(":",expand=True).iloc[:,0:2]
    df.drop([1],axis=1,inplace=True)
    df.columns = ["date","sender","message"]
    df[["date","hour"]] = df["date"].str.split(",",expand=True).iloc[:,0:2]
    df["date"] = pd.to_datetime(df["date"])
    def fucn(s):
        return s.strip().split(":")[0]+ " "+ s.strip().split(" ")[-1]
    df["hour"] = df["hour"].apply(fucn)
    return df

@st.cache
def get_data_not_salek(file_name):
    stringio = StringIO(file_name.getvalue().decode("utf-8"))
    lines = stringio.readlines()
    # choose only the linse that start with the dataes
    lines = (line for line in lines[1:])
    chat_lines = []
    for l in lines:
        if len(l) > 10:
            if (l[0].isdigit()) & ("/" in l[0:10]):
                chat_lines.append((l))
    df = pd.Series(chat_lines).str.split("-", expand=True).iloc[:, 0:2]
    df[["sender", "message"]] = df[1].str.split(":", expand=True).iloc[:, 0:2]
    df.drop([1], axis=1, inplace=True)
    df.columns = ["date", "sender", "message"]
    df[["date", "hour"]] = df["date"].str.split(",", expand=True).iloc[:, 0:2]
    df["date"] = pd.to_datetime(df["date"],format = "%d/%m/%Y")
    def fucn(s):
        return s.strip().split(":")[0] + " " + s.strip().split(" ")[-1]

    df["hour"] = df["hour"].apply(fucn)
    return df

try:
    if file :
        if type == "سالك":
            df = get_data_salek(file)
        elif type == "غير سالك":
            df = get_data_not_salek(file)
        st.write("**Sample data** from the chat")
        st.write(df.head())
        st.write("### Which one how send more message ?")
        b = df["sender"].value_counts()
        # draw a pie plot for the users count of message
        fig = px.pie(names=b.index, values=b.values,labels ={"names":"sender ","values":"num of messages "},)
        fig.update_traces(textposition='inside', textinfo='percent+label'
                            , hoverinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
        fig.update_layout(
            title_text="Sender & Num of Messages ", legend_title_text="Sender",
            title_x=.5,showlegend=False,margin={"l":0,"r":0})
        st.plotly_chart(fig, use_container_width=True)
        st.write("### Which hour most chats happen at ?")
        h = df["hour"].value_counts().to_frame()
        h["text"] = h["hour"].astype(str)
        fig = px.bar(data_frame=h,x=h.index,y= "hour",labels={"index":"Hour ","hour":"","text":"messages "},text="text" ,title="Messages in each hour")
        fig.update_traces(textposition='inside')
        fig.update_yaxes(showgrid=False,visible=False)
        fig.update_layout(title_x=.5,margin={"l":0,"r":0})
        st.plotly_chart(fig, use_container_width=True)

        # -------------------- the month question -------------------------------
        st.write("### What month most chats happen at ?")
        m = df.groupby(df["date"].dt.month)["sender"].count().to_frame()
        m["text"] = m["sender"].astype(str)
        fig = px.bar(data_frame=m, x=m.index, y="sender",  text="text",
                     labels={"date": "Month ", "sender": "", "text": "messages "},
                     title="Messages in each hour")
        fig.update_traces(textposition='inside')
        fig.update_yaxes(showgrid=False,visible=False)
        fig.update_layout(title_x=.5,margin={"l":0,"r":0})
        st.plotly_chart(fig, use_container_width=True)
        if st.checkbox("Analyze number of messages through a month ?"):
            month = st.selectbox("Choose the Month",df.date.dt.month.unique())
            c = st.checkbox("Show messages by each user ?")
            d = df[df["date"].dt.month ==  month]
            d = d.groupby(d["date"])["sender"].count()
            if not c:
                fig = px.line(x=d.index, y=d.values,title=f"Messages in each day in month { month}",labels={"x":"Date","y":"","text":"messages "})
            if c :
                # prepare the data
                final = get_final(df,month)
                fig = px.line(data_frame=final, x="date",y="value",color="variable", title=f"Messages in each day in month {month} for each sender",
                              labels={"x": "Date", "value": ""})
            fig.update_layout(title_x=.5,legend_title_text="",legend_orientation="h",legend_y=-.2,legend_x=.3,legend_font_size=10,margin={"l":0,"r":0})
            st.plotly_chart(fig, use_container_width=True)
        st.info("Made With love ❤ Ahmed Elsayed")
except:
    st.error("There is error happend please inform me and make sure you choosed the right WhatsApp type, idiot!")

