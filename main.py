import streamlit as st
from io import StringIO
import pandas as pd
st.markdown("# WhatsApp Chat Analyzer")
st.markdown("##### Analyze your chat with others on WhatsApp, know which one of you is **`رغاى`** 😂 ")
# sidebar
st.sidebar.markdown("""
# Analyze
This app is use to analyze your WhatsApp Chat using the exported text file 📁.
## How to export chat text file?

بص يابا هتتبع الخطوات دى 👇:
1) Open the individual or group chat.
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
        st.bar_chart(b)
        st.write("### Which hour most chats happen at ?")
        h = df["hour"].value_counts()
        st.bar_chart(h)
        st.write("### What month most chats happen at ?")
        m = df.groupby(df["date"].dt.month)["sender"].count()
        st.bar_chart(m)
        st.info("Made With love ❤ Ahmed Elsayed")
except:
    st.error("There is error happend please inform me ")

