import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://pmtool-production-5b83.up.railway.app"

st.set_page_config(page_title="Product Prioritization Tool", layout="wide")
st.title("Product Prioritization Tool")

page = st.sidebar.radio("Навигация", ["Приоритизация", "Добавить фичу", "Метрики"])

if page == "Приоритизация":
    st.header("Список фич")
    sort_by = st.selectbox("Сортировать по", ["wsjf_score", "rice_score", "ice_score"])
    status_filter = st.selectbox("Статус", ["все", "backlog", "in_progress", "released"])

    response = requests.get(f"{API_URL}/features")
    if response.status_code == 200:
        features = response.json()
        if status_filter != "все":
            features = [f for f in features if f["status"] == status_filter]
        features = sorted(features, key=lambda x: x.get(sort_by) or 0, reverse=True)

        if features:
            df = pd.DataFrame(features)[["id", "name", "wsjf_score", "rice_score", "ice_score", "status"]]
            df.columns = ["ID", "Фича", "WSJF", "RICE", "ICE", "Статус"]
            st.dataframe(df, use_container_width=True)

            fig = px.bar(df, x="Фича", y="WSJF", title="WSJF Score", color="WSJF", color_continuous_scale="blues")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Фич нет")
    else:
        st.error("Не удалось подключиться к API")

elif page == "Добавить фичу":
    st.header("Новая фича")

    with st.form("add_feature"):
        name = st.text_input("Название фичи")
        description = st.text_area("Описание")

        st.subheader("WSJF (обязательно)")
        col1, col2, col3, col4 = st.columns(4)
        business_value = col1.slider("Business Value", 1, 10, 5)
        time_criticality = col2.slider("Time Criticality", 1, 10, 5)
        risk_reduction = col3.slider("Risk Reduction", 1, 10, 5)
        job_size = col4.slider("Job Size", 1, 10, 5)

        st.caption(f"WSJF = {round((business_value + time_criticality + risk_reduction) / job_size, 2)}")

        st.subheader("RICE (опционально)")
        col5, col6, col7, col8 = st.columns(4)
        rice_reach = col5.number_input("Reach", min_value=0.0, value=0.0)
        rice_impact = col6.slider("Impact", 0, 10, 0)
        rice_confidence = col7.slider("Confidence", 0, 100, 0)
        rice_effort = col8.number_input("Effort", min_value=0.0, value=1.0)

        st.subheader("ICE (опционально)")
        col9, col10, col11 = st.columns(3)
        ice_impact = col9.slider("Impact ", 1, 10, 5)
        ice_confidence = col10.slider("Confidence ", 1, 10, 5)
        ice_ease = col11.slider("Ease", 1, 10, 5)

        submitted = st.form_submit_button("Добавить")
        if submitted:
            payload = {
                "name": name,
                "description": description,
                "business_value": business_value,
                "time_criticality": time_criticality,
                "risk_reduction": risk_reduction,
                "job_size": job_size,
                "rice_reach": rice_reach or None,
                "rice_impact": rice_impact or None,
                "rice_confidence": rice_confidence or None,
                "rice_effort": rice_effort or None,
                "ice_impact": ice_impact,
                "ice_confidence": ice_confidence,
                "ice_ease": ice_ease,
            }
            res = requests.post(f"{API_URL}/features", json=payload)
            if res.status_code == 200:
                st.success(f"Фича добавлена! WSJF: {res.json()['wsjf_score']}")
            else:
                st.error("Ошибка")

elif page == "Метрики":
    st.header("Метрики фичи")

    response = requests.get(f"{API_URL}/features")
    if response.status_code == 200:
        features = response.json()
        if features:
            feature_names = {f["name"]: f["id"] for f in features}
            selected = st.selectbox("Выбери фичу", list(feature_names.keys()))
            feature_id = feature_names[selected]

            with st.form("add_metric"):
                metric_name = st.text_input("Метрика (например: DAU, конверсия)")
                value = st.number_input("Значение", value=0.0)
                note = st.text_input("Комментарий (опционально)")
                if st.form_submit_button("Добавить метрику"):
                    res = requests.post(f"{API_URL}/features/{feature_id}/metrics", json={
                        "metric_name": metric_name,
                        "value": value,
                        "note": note
                    })
                    if res.status_code == 200:
                        st.success("Метрика добавлена!")

            metrics = requests.get(f"{API_URL}/features/{feature_id}/metrics").json()
            if metrics:
                df = pd.DataFrame(metrics)
                fig = px.line(df, x="date", y="value", color="metric_name", title=f"Динамика метрик: {selected}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Метрик пока нет")
        else:
            st.info("Сначала добавь фичи")