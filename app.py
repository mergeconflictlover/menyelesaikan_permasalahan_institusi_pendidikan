from pathlib import Path
import json

import joblib
import pandas as pd
import streamlit as st
import altair as alt

from model_utils import IQRClipper


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "student_status_pipeline.joblib"
METRICS_PATH = BASE_DIR / "model" / "metrics_summary.json"
DATA_PATH = BASE_DIR / "data" / "data.csv"


MARITAL_STATUS_MAP = {
    1: "Single",
    2: "Married",
    3: "Widower",
    4: "Divorced",
    5: "Facto union",
    6: "Legally separated",
}

ATTENDANCE_MAP = {
    0: "Evening attendance",
    1: "Daytime attendance",
}

YES_NO_MAP = {
    0: "No",
    1: "Yes",
}

GENDER_MAP = {
    0: "Female",
    1: "Male",
}

APPLICATION_MODE_MAP = {
    1: "1st phase - general contingent",
    2: "Ordinance No. 612/93",
    5: "1st phase - special contingent (Azores Island)",
    7: "Holders of other higher courses",
    10: "Ordinance No. 854-B/99",
    15: "International student (bachelor)",
    16: "1st phase - special contingent (Madeira Island)",
    17: "2nd phase - general contingent",
    18: "3rd phase - general contingent",
    26: "Ordinance No. 533-A/99, item b2",
    27: "Ordinance No. 533-A/99, item b3",
    39: "Over 23 years old",
    42: "Transfer",
    43: "Change of course",
    44: "Technological specialization diploma holders",
    51: "Change of institution/course",
    53: "Short cycle diploma holders",
    57: "Change of institution/course (International)",
}

COURSE_MAP = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (evening attendance)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equinculture",
    9147: "Management",
    9238: "Social Service",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising and Marketing Management",
    9773: "Journalism and Communication",
    9853: "Basic Education",
    9991: "Management (evening attendance)",
}

PREVIOUS_QUALIFICATION_MAP = {
    1: "Secondary education",
    2: "Higher education - bachelor's degree",
    3: "Higher education - degree",
    4: "Higher education - master's",
    5: "Higher education - doctorate",
    6: "Frequency of higher education",
    9: "12th year of schooling - not completed",
    10: "11th year of schooling - not completed",
    12: "Other - 11th year of schooling",
    14: "10th year of schooling",
    15: "10th year of schooling - not completed",
    19: "Basic education 3rd cycle",
    38: "Basic education 2nd cycle",
    39: "Technological specialization course",
    40: "Higher education - degree (1st cycle)",
    42: "Professional higher technical course",
    43: "Higher education - master (2nd cycle)",
}

FEATURE_LABEL_MAP = {
    "Curricular_units_2nd_sem_approved": "Approved units in second semester",
    "Tuition_fees_up_to_date": "Tuition fees status",
    "Curricular_units_1st_sem_approved": "Approved units in first semester",
    "Course": "Study program",
    "Age_at_enrollment": "Age at enrollment",
}

STATUS_COPY = {
    "Dropout": {
        "label": "Dropout",
        "tone": "critical",
        "summary": "This profile should be placed on the academic intervention watchlist.",
    },
    "Enrolled": {
        "label": "Enrolled",
        "tone": "watch",
        "summary": "This profile is still active, but progress should be monitored closely.",
    },
    "Graduate": {
        "label": "Graduate",
        "tone": "positive",
        "summary": "This profile is aligned with successful completion patterns.",
    },
}


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_metrics():
    return json.loads(METRICS_PATH.read_text())


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, sep=";", encoding="utf-8-sig")
    df = df.rename(columns={"Status": "Target"})
    df["Course_name"] = df["Course"].map(COURSE_MAP)
    df["Gender_label"] = df["Gender"].map(GENDER_MAP)
    df["Tuition_label"] = df["Tuition_fees_up_to_date"].map(YES_NO_MAP)
    df["Attendance_label"] = df["Daytime_evening_attendance"].map(ATTENDANCE_MAP)
    df["Dropout_flag"] = df["Target"].eq("Dropout").astype(int)
    df["Graduate_flag"] = df["Target"].eq("Graduate").astype(int)
    df["Enrolled_flag"] = df["Target"].eq("Enrolled").astype(int)
    return df


def pretty_feature_name(raw_name):
    return FEATURE_LABEL_MAP.get(raw_name, raw_name.replace("_", " "))


def build_age_band(frame):
    age_frame = frame.copy()
    age_frame["Age_band"] = pd.cut(
        age_frame["Age_at_enrollment"],
        bins=[0, 18, 21, 25, 30, 100],
        labels=["<=18", "19-21", "22-25", "26-30", ">30"],
    )
    return age_frame


def select_code(label, options_map, default_value, help_text=None):
    options = list(options_map.keys())
    default_index = options.index(int(default_value))
    format_func = lambda value: f"{value} - {options_map[value]}"
    return st.selectbox(label, options, index=default_index, format_func=format_func, help=help_text)


def yes_no_select(label, default_value):
    return select_code(label, YES_NO_MAP, default_value)


def format_pct(value):
    return f"{value:.1f}%"


def risk_segment(dropout_rate):
    if dropout_rate >= 35:
        return "High risk"
    if dropout_rate >= 25:
        return "Moderate risk"
    return "Controlled"


def compact_bar_chart(frame, x_col, y_col, color="#2563EB", height=240):
    return (
        alt.Chart(frame)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color=color)
        .encode(
            x=alt.X(
                x_col,
                title=None,
                sort="-y",
                axis=alt.Axis(labelLimit=140, labelPadding=10, ticks=False, domain=False),
            ),
            y=alt.Y(
                y_col,
                title=None,
                axis=alt.Axis(labelPadding=10, ticks=False, domain=False, grid=True),
            ),
            tooltip=[x_col, y_col],
        )
        .properties(
            height=height,
            padding={"left": 18, "right": 18, "top": 10, "bottom": 10},
        )
    )


def horizontal_bar_chart(frame, x_col, y_col, color="#2563EB", height=240):
    return (
        alt.Chart(frame)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, color=color)
        .encode(
            x=alt.X(
                x_col,
                title=None,
                axis=alt.Axis(labelPadding=10, ticks=False, domain=False, grid=True),
            ),
            y=alt.Y(
                y_col,
                title=None,
                sort="-x",
                axis=alt.Axis(labelLimit=180, labelPadding=10, ticks=False, domain=False),
            ),
            tooltip=[y_col, x_col],
        )
        .properties(
            height=height,
            padding={"left": 24, "right": 18, "top": 10, "bottom": 10},
        )
    )


def grouped_bar_chart(frame, index_col, color_range, height=240):
    source = frame.rename_axis(index_col).reset_index()
    melted = source.melt(id_vars=index_col, var_name="Series", value_name="Value")
    return (
        alt.Chart(melted)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X(
                f"{index_col}:N",
                title=None,
                axis=alt.Axis(labelLimit=140, labelPadding=10, ticks=False, domain=False),
            ),
            xOffset=alt.XOffset("Series:N"),
            y=alt.Y(
                "Value:Q",
                title=None,
                axis=alt.Axis(labelPadding=10, ticks=False, domain=False, grid=True),
            ),
            color=alt.Color(
                "Series:N",
                legend=alt.Legend(title=None, orient="top"),
                scale=alt.Scale(range=color_range),
            ),
            tooltip=[f"{index_col}:N", "Series:N", "Value:Q"],
        )
        .properties(
            height=height,
            padding={"left": 18, "right": 18, "top": 10, "bottom": 10},
        )
    )


def stacked_bar_chart(frame, index_col, color_range, height=240):
    source = frame.rename_axis(index_col).reset_index()
    melted = source.melt(id_vars=index_col, var_name="Series", value_name="Value")
    return (
        alt.Chart(melted)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{index_col}:N",
                title=None,
                axis=alt.Axis(labelLimit=140, labelPadding=10, ticks=False, domain=False),
            ),
            y=alt.Y(
                "Value:Q",
                title=None,
                axis=alt.Axis(labelPadding=10, ticks=False, domain=False, grid=True),
            ),
            color=alt.Color(
                "Series:N",
                legend=alt.Legend(title=None, orient="top"),
                scale=alt.Scale(range=color_range),
            ),
            tooltip=[f"{index_col}:N", "Series:N", "Value:Q"],
        )
        .properties(
            height=height,
            padding={"left": 18, "right": 18, "top": 10, "bottom": 10},
        )
    )


st.set_page_config(
    page_title="Jaya Jaya Institut Prediction App",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 2rem;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 14px;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 16px 18px;
        border-radius: 18px;
        box-shadow: none;
    }
    .eyebrow {
        font-size: 0.8rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .hero {
        padding: 0.1rem 0 0.9rem 0;
    }
    .hero h1 {
        font-size: 2.15rem;
        line-height: 1.05;
        margin: 0;
        color: #111827;
    }
    .hero p {
        font-size: 0.96rem;
        line-height: 1.7;
        color: #6b7280;
        max-width: 820px;
        margin-top: 0.75rem;
    }
    .soft-copy {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .result-block {
        border-radius: 14px;
        padding: 10px 0 0 0;
    }
    .divider {
        height: 1px;
        background: #eceff3;
        margin: 0.5rem 0 0.9rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

model = load_model()
metrics = load_metrics()
defaults = metrics["sample_defaults"]
data = load_data()
top_features = metrics["feature_importance"][:5]

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Academic Executive Dashboard</div>
        <h1>Jaya Jaya Institut Student Status Predictor</h1>
        <p>Monitor student risk and academic performance trends.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

dashboard_tab, prediction_tab = st.tabs(["Monitoring Dashboard", "Prediction Prototype"])

with dashboard_tab:
    st.caption("Use the dashboard to inspect student risk patterns, academic progression, and operational warning signs.")

    top_board = st.columns([1, 3])
    with top_board[0].container(border=True, height="stretch"):
        st.markdown("#### Filters")
        selected_courses = st.multiselect(
            "Study program",
            options=sorted(data["Course_name"].dropna().unique().tolist()),
            placeholder="All study programs",
        )
        selected_genders = st.multiselect(
            "Gender",
            options=sorted(data["Gender_label"].dropna().unique().tolist()),
            placeholder="All genders",
        )
        selected_tuition = st.multiselect(
            "Tuition status",
            options=sorted(data["Tuition_label"].dropna().unique().tolist()),
            placeholder="All tuition status",
        )
        selected_attendance = st.multiselect(
            "Attendance",
            options=sorted(data["Attendance_label"].dropna().unique().tolist()),
            placeholder="All attendance types",
        )

    filtered_data = data.copy()
    if selected_courses:
        filtered_data = filtered_data[filtered_data["Course_name"].isin(selected_courses)]
    if selected_genders:
        filtered_data = filtered_data[filtered_data["Gender_label"].isin(selected_genders)]
    if selected_tuition:
        filtered_data = filtered_data[filtered_data["Tuition_label"].isin(selected_tuition)]
    if selected_attendance:
        filtered_data = filtered_data[filtered_data["Attendance_label"].isin(selected_attendance)]
    if filtered_data.empty:
        st.warning("No records match the current filters. Showing the full dataset instead.")
        filtered_data = data.copy()

    dropout_rate = filtered_data["Dropout_flag"].mean() * 100
    graduate_rate = filtered_data["Graduate_flag"].mean() * 100
    tuition_issue_rate = filtered_data["Tuition_fees_up_to_date"].eq(0).mean() * 100
    filtered_age = build_age_band(filtered_data)

    status_counts = (
        filtered_data["Target"]
        .value_counts()
        .rename_axis("Student status")
        .to_frame("Students")
        .reset_index()
    )
    fee_chart = pd.crosstab(
        filtered_data["Tuition_label"],
        filtered_data["Target"],
        normalize="index",
    )
    at_risk_course = (
        filtered_data[filtered_data["Target"] == "Dropout"]
        .groupby("Course_name")
        .size()
        .sort_values(ascending=False)
        .head(8)
        .to_frame("Dropout cases")
        .reset_index()
    )
    approval_chart = (
        filtered_data.groupby("Target")[["Curricular_units_1st_sem_approved", "Curricular_units_2nd_sem_approved"]]
        .mean()
        .sort_values("Curricular_units_2nd_sem_approved", ascending=False)
    )
    age_dropout = (
        filtered_age.groupby("Age_band", observed=False)["Dropout_flag"]
        .mean()
        .fillna(0)
        .to_frame("Dropout rate")
        .reset_index()
    )
    course_risk = (
        filtered_data.groupby("Course_name")
        .agg(
            total_students=("Target", "size"),
            dropout_count=("Dropout_flag", "sum"),
            avg_approved_2nd_sem=("Curricular_units_2nd_sem_approved", "mean"),
        )
        .assign(dropout_rate=lambda d: d["dropout_count"] / d["total_students"])
        .sort_values("dropout_rate", ascending=False)
        .head(8)
    )

    with top_board[0].container():
        metric_a, metric_b = st.columns(2)
        metric_a.metric("Dropout", format_pct(dropout_rate))
        metric_b.metric("Graduate", format_pct(graduate_rate))
        metric_c, metric_d = st.columns(2)
        metric_c.metric("Tuition issue", format_pct(tuition_issue_rate))
        metric_d.metric("Risk", risk_segment(dropout_rate))

    with top_board[1].container(border=True, height="stretch"):
        st.markdown("#### Student status distribution")
        st.caption("How the current filtered population is split across final student outcomes.")
        st.altair_chart(
            compact_bar_chart(status_counts, "Student status:N", "Students:Q", color="#2563EB", height=320),
            use_container_width=True,
        )

    row_one = st.columns(3)
    with row_one[0].container(border=True, height="stretch"):
        st.markdown("#### Student outcome by tuition status")
        st.caption("This view highlights how tuition discipline is associated with student outcomes.")
        st.altair_chart(
            stacked_bar_chart(fee_chart, "Tuition status", ["#2563EB", "#60A5FA", "#BFDBFE"], height=240),
            use_container_width=True,
        )

    with row_one[1].container(border=True, height="stretch"):
        st.markdown("#### Top programs to watch")
        st.caption("Programs with the highest number of dropout cases in the current view.")
        st.altair_chart(
            horizontal_bar_chart(at_risk_course, "Dropout cases:Q", "Course_name:N", color="#3B82F6"),
            use_container_width=True,
        )

    with row_one[2].container(border=True, height="stretch"):
        st.markdown("#### Dropout rate by age band")
        st.caption("Older entry cohorts can show a different risk profile than younger cohorts.")
        st.altair_chart(
            compact_bar_chart(age_dropout, "Age_band:N", "Dropout rate:Q", color="#60A5FA"),
            use_container_width=True,
        )

    row_two = st.columns(2)
    with row_two[0].container(border=True, height="stretch"):
        st.markdown("#### Approved units by student status")
        st.caption("Comparing first-semester and second-semester approved units across status groups.")
        st.altair_chart(
            grouped_bar_chart(
                approval_chart,
                "Student status",
                ["#2563EB", "#93C5FD"],
                height=240,
            ),
            use_container_width=True,
        )

    with row_two[1].container(border=True, height="stretch"):
        st.markdown("#### Top features in the current model")
        st.caption(
            "The strongest drivers in the current model are dominated by academic progression and tuition discipline."
        )
        for item in top_features:
            st.write(f"- {pretty_feature_name(item['feature'])}")
        st.markdown("")
        st.markdown("#### Executive reading")
        st.caption("Use these points as a quick interpretation layer for the dashboard above.")
        st.markdown(
            """
            - Keep a close watch on students with low approved units in the second semester.
            - Combine academic monitoring with tuition follow-up.
            - Prioritize study programs with the highest dropout load.
            - Review transition cases that remain in the `Enrolled` segment.
            """
        )

    with st.container(border=True):
        st.markdown("#### Course risk table")
        st.caption("A compact operational view for identifying where intervention should start.")
        st.dataframe(
            course_risk.rename(
                columns={
                    "total_students": "Total students",
                    "dropout_count": "Dropout count",
                    "avg_approved_2nd_sem": "Avg approved 2nd sem",
                    "dropout_rate": "Dropout rate",
                }
            ),
            use_container_width=True,
        )

    with st.container(border=True):
        st.markdown("#### Filtered student preview")
        st.caption("A quick row-level preview for reviewers and business users.")
        preview_cols = [
            "Target",
            "Course_name",
            "Gender_label",
            "Tuition_label",
            "Attendance_label",
            "Age_at_enrollment",
            "Curricular_units_1st_sem_approved",
            "Curricular_units_2nd_sem_approved",
        ]
        st.dataframe(filtered_data[preview_cols].head(15), use_container_width=True, hide_index=True)

with prediction_tab:
    intro_cols = st.columns([1.35, 1])
    with intro_cols[0]:
        st.markdown("#### Prediction studio")
        st.caption(
            "Enter a student profile to estimate whether the current pattern is closer to Dropout, Enrolled, or Graduate."
        )
    with intro_cols[1]:
        st.markdown("#### Model guidance")
        st.caption(
            "Use this prediction as an early-warning signal. Final intervention decisions should still consider adviser notes and the latest operational context."
        )

    with st.form("prediction_form"):
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            marital_status = select_code("Marital status", MARITAL_STATUS_MAP, defaults["Marital_status"])
            application_mode = select_code("Application mode", APPLICATION_MODE_MAP, defaults["Application_mode"])
            course = select_code("Course", COURSE_MAP, defaults["Course"])
            daytime_evening_attendance = select_code("Attendance", ATTENDANCE_MAP, defaults["Daytime_evening_attendance"])
            previous_qualification = select_code(
                "Previous qualification",
                PREVIOUS_QUALIFICATION_MAP,
                defaults["Previous_qualification"],
            )
            application_order = st.number_input(
                "Application order",
                min_value=0,
                max_value=9,
                value=int(defaults["Application_order"]),
                step=1,
            )
            age_at_enrollment = st.number_input(
                "Age at enrollment",
                min_value=16,
                max_value=80,
                value=int(defaults["Age_at_enrollment"]),
                step=1,
            )

        with col_b:
            previous_qualification_grade = st.number_input(
                "Previous qualification grade",
                min_value=0.0,
                max_value=200.0,
                value=float(defaults["Previous_qualification_grade"]),
                step=0.1,
            )
            admission_grade = st.number_input(
                "Admission grade",
                min_value=0.0,
                max_value=200.0,
                value=float(defaults["Admission_grade"]),
                step=0.1,
            )
            displaced = yes_no_select("Displaced", defaults["Displaced"])
            debtor = yes_no_select("Debtor", defaults["Debtor"])
            tuition_fees_up_to_date = yes_no_select("Tuition fees up to date", defaults["Tuition_fees_up_to_date"])
            gender = select_code("Gender", GENDER_MAP, defaults["Gender"])
            scholarship_holder = yes_no_select("Scholarship holder", defaults["Scholarship_holder"])

        with col_c:
            curricular_units_1st_sem_enrolled = st.number_input(
                "1st semester enrolled units",
                min_value=0,
                max_value=30,
                value=int(defaults["Curricular_units_1st_sem_enrolled"]),
                step=1,
            )
            curricular_units_1st_sem_approved = st.number_input(
                "1st semester approved units",
                min_value=0,
                max_value=30,
                value=int(defaults["Curricular_units_1st_sem_approved"]),
                step=1,
            )
            curricular_units_1st_sem_grade = st.number_input(
                "1st semester grade",
                min_value=0.0,
                max_value=20.0,
                value=float(defaults["Curricular_units_1st_sem_grade"]),
                step=0.1,
            )
            curricular_units_2nd_sem_enrolled = st.number_input(
                "2nd semester enrolled units",
                min_value=0,
                max_value=30,
                value=int(defaults["Curricular_units_2nd_sem_enrolled"]),
                step=1,
            )
            curricular_units_2nd_sem_approved = st.number_input(
                "2nd semester approved units",
                min_value=0,
                max_value=30,
                value=int(defaults["Curricular_units_2nd_sem_approved"]),
                step=1,
            )
            curricular_units_2nd_sem_grade = st.number_input(
                "2nd semester grade",
                min_value=0.0,
                max_value=20.0,
                value=float(defaults["Curricular_units_2nd_sem_grade"]),
                step=0.1,
            )

        macro_col1, macro_col2, macro_col3 = st.columns(3)
        with macro_col1:
            unemployment_rate = st.number_input(
                "Unemployment rate",
                min_value=0.0,
                max_value=30.0,
                value=float(defaults["Unemployment_rate"]),
                step=0.1,
            )
        with macro_col2:
            inflation_rate = st.number_input(
                "Inflation rate",
                min_value=-5.0,
                max_value=20.0,
                value=float(defaults["Inflation_rate"]),
                step=0.1,
            )
        with macro_col3:
            gdp = st.number_input(
                "GDP",
                min_value=-10.0,
                max_value=10.0,
                value=float(defaults["GDP"]),
                step=0.01,
            )

        submitted = st.form_submit_button("Predict student status", use_container_width=True)

    input_frame = pd.DataFrame(
        [
            {
                "Marital_status": marital_status,
                "Application_mode": application_mode,
                "Application_order": application_order,
                "Course": course,
                "Daytime_evening_attendance": daytime_evening_attendance,
                "Previous_qualification": previous_qualification,
                "Previous_qualification_grade": previous_qualification_grade,
                "Admission_grade": admission_grade,
                "Displaced": displaced,
                "Debtor": debtor,
                "Tuition_fees_up_to_date": tuition_fees_up_to_date,
                "Gender": gender,
                "Scholarship_holder": scholarship_holder,
                "Age_at_enrollment": age_at_enrollment,
                "Curricular_units_1st_sem_enrolled": curricular_units_1st_sem_enrolled,
                "Curricular_units_1st_sem_approved": curricular_units_1st_sem_approved,
                "Curricular_units_1st_sem_grade": curricular_units_1st_sem_grade,
                "Curricular_units_2nd_sem_enrolled": curricular_units_2nd_sem_enrolled,
                "Curricular_units_2nd_sem_approved": curricular_units_2nd_sem_approved,
                "Curricular_units_2nd_sem_grade": curricular_units_2nd_sem_grade,
                "Unemployment_rate": unemployment_rate,
                "Inflation_rate": inflation_rate,
                "GDP": gdp,
            }
        ]
    )

    with st.expander("Preview input data"):
        st.dataframe(input_frame, use_container_width=True)

    if submitted:
        prediction = model.predict(input_frame)[0]
        probabilities = model.predict_proba(input_frame)[0]
        proba_df = (
            pd.DataFrame({"Status": model.classes_, "Probability": probabilities})
            .sort_values("Probability", ascending=False)
        )
        current_status = STATUS_COPY[prediction]

        result_cols = st.columns(3)
        with result_cols[0].container(border=True, height="stretch"):
            st.markdown("#### Prediction Result")
            st.markdown(f"##### {current_status['label']}")
            st.caption(current_status["summary"])
            st.caption(f"Highest class probability: {proba_df.iloc[0]['Probability'] * 100:.1f}%")

        with result_cols[1].container(border=True, height="stretch"):
            st.markdown("#### Probability By Class")
            st.altair_chart(
                horizontal_bar_chart(proba_df, "Probability:Q", "Status:N", color="#2563EB", height=220),
                use_container_width=True,
            )

        with result_cols[2].container(border=True, height="stretch"):
            st.markdown("#### Top Features To Monitor")
            for item in top_features:
                st.write(f"- {pretty_feature_name(item['feature'])}")

        scenario_rows = []
        for approved_units in [0, 2, 4, 6, 8]:
            scenario_frame = input_frame.copy()
            scenario_frame["Curricular_units_2nd_sem_approved"] = approved_units
            scenario_prediction = model.predict(scenario_frame)[0]
            dropout_probability = float(
                model.predict_proba(scenario_frame)[0][list(model.classes_).index("Dropout")]
            )
            scenario_rows.append(
                {
                    "2nd semester approved units": approved_units,
                    "Predicted status": scenario_prediction,
                    "Dropout probability": round(dropout_probability, 4),
                }
            )

        scenario_df = pd.DataFrame(scenario_rows)
        st.markdown("#### What-If Simulation")
        st.caption(
            "This simulation shows how the predicted outcome shifts when second-semester approved units improve."
        )
        sim_cols = st.columns(2)
        with sim_cols[0].container(border=True, height="stretch"):
            st.markdown("#### Simulation Table")
            st.dataframe(scenario_df, use_container_width=True, hide_index=True)
        with sim_cols[1].container(border=True, height="stretch"):
            st.markdown("#### Simulation Chart")
            st.bar_chart(
                scenario_df.set_index("2nd semester approved units")[["Dropout probability"]]
            )
