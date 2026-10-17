
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EduRisk Analytics - Lab 03",
    page_icon="🎓",
    layout="wide"
)

def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()

#laod the student data
student_df = load_student_data()

#added custom css

st.markdown("""
<style>
.stApp { background-color: #0E1A2B; }
.block-container { padding-top: 2.5rem; max-width: 1200px; }

h1, h2, h3 { color: #FFFFFF !important; }
.stApp p, .stApp label, .stApp span { color: #E8EEF7; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #091321;
    border-right: 1px solid #26406B;
}
 /* DESIGN: white sidebar title with a teal underline */
    section[data-testid="stSidebar"] h1 {
        color: #FFFFFF;
        border-bottom: 2px solid #1E7A5F;
        padding-bottom: 6px;
    }

section[data-testid="stSidebar"] * { color: #E8EEF7 !important; }

/* Metric boxes */
div[data-testid="stMetric"] {
    background-color: #162640;
    border: 1px solid #26406B;
    border-top: 4px solid #2EC4B6;
    border-radius: 12px;
    padding: 16px 20px;
}
div[data-testid="stMetricLabel"] * { color: #9FB0C7 !important; }
div[data-testid="stMetricValue"] * { color: #FFFFFF !important; }

/* Form box */
div[data-testid="stForm"] {
    background-color: #162640;
    border: 1px solid #26406B;
    border-radius: 12px;
    padding: 1rem;
}

/* Buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    background-color: #2EC4B6;
    color: #04201D !important;
    border: none;
    border-radius: 8px;
    font-weight: 700;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    background-color: #5FE0D4;
}

/* Table */
div[data-testid="stDataFrame"] {
    border: 1px solid #26406B;
    border-radius: 10px;
}
    /* DESIGN: navy download button, different from the teal action buttons */
    .stDownloadButton button {
        background-color: #0F2238;
        color: #FFFFFF;
        border: 1px solid #0F2238;
    }
 /* DESIGN: rounded message boxes (success / info / warning / error) */
    [data-testid="stAlert"] {
        border-radius: 8px;
    }


#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)



def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

#add the risk level column

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# ------------------------------------------------------------
# 6. DESIGN: RISK LEVEL COLOURS
# green = Low, yellow = Medium, red = High
# ------------------------------------------------------------
risk_colors = {
    "Low Risk": "background-color: #DCFCE7; color: #166534",
    "Medium Risk": "background-color: #FEF3C7; color: #92400E",
    "High Risk": "background-color: #FEE2E2; color: #991B1B"
}

# DESIGN: paint only the "Risk Level" column of a table
def color_risk(df):
    return df.style.map(
        lambda value: risk_colors.get(value, ""),
        subset=["Risk Level"]
    )

total_students = len(student_df)
average_score = student_df["Score"].mean()
average_attendance = student_df["Attendance"].mean()
low_score_students = student_df[student_df["Score"] < 60].shape[0]

#sidebar menu
with st.sidebar:
    st.title("EduRisk Menu")
    selected_page = st.radio(
        "Select Page",
        ["Home", "Dashboard", "Student Data", "Risk Checker", "About"]
    )

#Home Page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Frontend Prototype with CSV Data Loading")
    st.write("Welcome to Lab 03.")
    st.write(
        "In this lab, the app loads student data from students.csv "
        "using Pandas instead of storing data directly inside app.py."
    )
    st.success("Lab 03 app is running successfully!")
    
#Dashboard Page
elif selected_page == "Dashboard":
    st.title("Dashboard Prototype")

    st.write(
        "This dashboard gives a quick overview of student performance "
        "using data loaded from students.csv."
    )

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", total_students)

    with col2:
        st.metric("Average Score", round(average_score, 2))

    with col3:
        st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        st.metric("High Risk", high_risk_students)

    st.subheader("Student Records")
    st.write("This table shows student data loaded from students.csv.")
    st.dataframe(student_df)

    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Score Chart")
        score_chart = student_df.set_index("Student Name")["Score"]
        st.bar_chart(score_chart)

    with chart_col2:
        st.write("Course Count")
        course_count = student_df["Course"].value_counts()
        st.bar_chart(course_count)

        st.info(
        "Ethics Reminder: Academic monitoring should support students, "
        "not label or punish them."
    )


#Update the Student Data page to show the full dataset with risk levels.
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

#Create a page where users can enter one student's score and attendance to check risk level.
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Use this page to check the risk level of one student based on" \
        "score and attendance."
    )

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

#Update the About page with Lab 02 information and an ethics reminder.

else:
    st.title("About")

    st.write("This app is part of Lab 03.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Data Loading, Layout, and Frontend Prototype")

    st.info(
        "This frontend prototype loads real data from students.csv "
        "and displays it using Streamlit and Pandas."
    )

    st.warning(
        "Ethics Reminder: Student risk information should be used responsibly "
        "to support learning and student success."
    )