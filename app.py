# Gerekli Kütüphaneler ve Sayfa Ayarı
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="Knapsack Solver",
    page_icon="",
    layout="wide"
)

# -------------------------
# CSS Tasarım
# -------------------------
st.markdown("""
<style>
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 18px;
        color: #4b5563;
        margin-bottom: 25px;
    }
    .summary-card {
        background: linear-gradient(135deg, #f8fafc, #eef2ff);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        text-align: center;
    }
    .summary-card h4 {
        margin: 0;
        color: #374151;
        font-size: 16px;
    }
    .summary-card p {
        margin: 8px 0 0 0;
        font-size: 28px;
        font-weight: 700;
        color: #111827;
    }
    .winner-card {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #86efac;
        font-size: 22px;
        font-weight: 700;
        color: #14532d;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .section-box {
        background: #ffffff;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title"> Knapsack Problem Solver</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">0/1 Knapsack, Unbounded Knapsack ve Fractional Knapsack algoritmalarını karşılaştıran interaktif sistem.</div>',
    unsafe_allow_html=True
)

# -------------------------
# Algoritma Fonksiyonları
# -------------------------
def zero_one_knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                include_item = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude_item = dp[i - 1][w]
                dp[i][w] = max(include_item, exclude_item)
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    w = capacity

    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]

    selected_items.reverse()
    return dp[n][capacity], selected_items


def unbounded_knapsack(weights, values, capacity):
    n = len(weights)
    dp = [0 for _ in range(capacity + 1)]
    selected = [-1 for _ in range(capacity + 1)]

    for w in range(capacity + 1):
        for i in range(n):
            if weights[i] <= w:
                candidate_value = dp[w - weights[i]] + values[i]
                if candidate_value > dp[w]:
                    dp[w] = candidate_value
                    selected[w] = i

    selected_items = []
    w = capacity

    while w > 0 and selected[w] != -1:
        item_index = selected[w]
        selected_items.append(item_index)
        w -= weights[item_index]

    return dp[capacity], selected_items


def fractional_knapsack(weights, values, capacity):
    item_list = []

    for i in range(len(weights)):
        item_list.append({
            "index": i,
            "weight": weights[i],
            "value": values[i],
            "ratio": values[i] / weights[i]
        })

    item_list.sort(key=lambda x: x["ratio"], reverse=True)

    total_value = 0
    selected_items = []
    remaining_capacity = capacity

    for item in item_list:
        if remaining_capacity == 0:
            break

        if item["weight"] <= remaining_capacity:
            total_value += item["value"]
            remaining_capacity -= item["weight"]
            selected_items.append({"index": item["index"], "fraction": 1})
        else:
            fraction = remaining_capacity / item["weight"]
            total_value += item["value"] * fraction
            selected_items.append({"index": item["index"], "fraction": fraction})
            remaining_capacity = 0

    return total_value, selected_items


# -------------------------
# Yardımcı Fonksiyonlar
# -------------------------
def measure_time(func, weights, values, capacity):
    start = time.perf_counter()
    result = func(weights, values, capacity)
    end = time.perf_counter()
    return result, end - start


def selected_table_01(selected_items, weights, values):
    rows = []
    for i in selected_items:
        rows.append({
            "Item": f"Item {i+1}",
            "Weight": weights[i],
            "Value": values[i],
            "Fraction": 1.0,
            "Used Weight": weights[i],
            "Used Value": values[i]
        })
    return pd.DataFrame(rows)


def selected_table_unbounded(selected_items, weights, values):
    rows = []
    for i in selected_items:
        rows.append({
            "Item": f"Item {i+1}",
            "Weight": weights[i],
            "Value": values[i],
            "Fraction": 1.0,
            "Used Weight": weights[i],
            "Used Value": values[i]
        })
    return pd.DataFrame(rows)


def selected_table_fractional(selected_items, weights, values):
    rows = []
    for item in selected_items:
        i = item["index"]
        fraction = item["fraction"]
        rows.append({
            "Item": f"Item {i+1}",
            "Weight": weights[i],
            "Value": values[i],
            "Fraction": round(fraction, 2),
            "Used Weight": round(weights[i] * fraction, 2),
            "Used Value": round(values[i] * fraction, 2)
        })
    return pd.DataFrame(rows)


def summarize_selected_table(df, capacity):
    if df.empty:
        return 0, 0, 0
    total_weight = df["Used Weight"].sum()
    total_value = df["Used Value"].sum()
    usage = (total_weight / capacity) * 100
    return total_weight, total_value, usage


def parse_input_list(text):
    return [int(x.strip()) for x in text.split(",") if x.strip() != ""]


# -------------------------
# Kullanıcı Giriş Paneli
# -------------------------
st.sidebar.header(" Input Settings")

weights_input = st.sidebar.text_area(
    "Weights List",
    "12,25,8,15,30,18,22,10,28,16,14,20,26,11,19,24,17,13,21,29",
    height=90
)

values_input = st.sidebar.text_area(
    "Values List",
    "90,120,70,95,180,110,140,80,175,105,92,130,160,78,118,150,102,88,125,170",
    height=90
)

capacity = st.sidebar.slider(
    "Knapsack Capacity",
    min_value=10,
    max_value=300,
    value=100,
    step=10
)

run_button = st.sidebar.button("Solve Knapsack", use_container_width=True)

st.sidebar.info(
    "Listeleri virgülle ayrılmış tam sayılar olarak girin. Örnek: 10,20,30"
)

# -------------------------
# Ana Çalıştırma Bölümü
# -------------------------
if run_button:
    try:
        weights = parse_input_list(weights_input)
        values = parse_input_list(values_input)

        if len(weights) == 0 or len(values) == 0:
            st.error("Weights ve Values listeleri boş olamaz.")
        elif len(weights) != len(values):
            st.error("Weights ve Values listeleri aynı uzunlukta olmalıdır.")
        elif any(w <= 0 for w in weights):
            st.error("Ağırlık değerleri 0 veya negatif olamaz.")
        else:
            st.success("Input values loaded successfully!")

            input_df = pd.DataFrame({
                "Item": [f"Item {i+1}" for i in range(len(weights))],
                "Weight": weights,
                "Value": values,
                "Value/Weight": [round(v / w, 2) for v, w in zip(values, weights)]
            })

            # Algoritmaları çalıştır
            (res_01, sel_01), time_01 = measure_time(zero_one_knapsack, weights, values, capacity)
            (res_unbounded, sel_unbounded), time_unbounded = measure_time(unbounded_knapsack, weights, values, capacity)
            (res_fractional, sel_fractional), time_fractional = measure_time(fractional_knapsack, weights, values, capacity)

            selected_01_df = selected_table_01(sel_01, weights, values)
            selected_unbounded_df = selected_table_unbounded(sel_unbounded, weights, values)
            selected_fractional_df = selected_table_fractional(sel_fractional, weights, values)

            results_df = pd.DataFrame({
                "Algorithm": [
                    "0/1 Knapsack DP",
                    "Unbounded Knapsack DP",
                    "Fractional Knapsack Greedy"
                ],
                "Maximum Value": [
                    round(res_01, 2),
                    round(res_unbounded, 2),
                    round(res_fractional, 2)
                ],
                "Execution Time (seconds)": [
                    time_01,
                    time_unbounded,
                    time_fractional
                ],
                "Time Complexity": [
                    "O(n × W)",
                    "O(n × W)",
                    "O(n log n)"
                ]
            })

            # Problem özeti
            st.subheader("Problem Summary")
            s1, s2, s3, s4 = st.columns(4)
            with s1:
                st.markdown(f'<div class="summary-card"><h4>Number of Items</h4><p>{len(weights)}</p></div>', unsafe_allow_html=True)
            with s2:
                st.markdown(f'<div class="summary-card"><h4>Capacity</h4><p>{capacity}</p></div>', unsafe_allow_html=True)
            with s3:
                st.markdown(f'<div class="summary-card"><h4>Average Weight</h4><p>{round(sum(weights)/len(weights), 2)}</p></div>', unsafe_allow_html=True)
            with s4:
                st.markdown(f'<div class="summary-card"><h4>Average Value</h4><p>{round(sum(values)/len(values), 2)}</p></div>', unsafe_allow_html=True)

            # Kazanan algoritma
            best_row = results_df.loc[results_df["Maximum Value"].idxmax()]
            st.markdown(
            f"""
            <div class="winner-card" style="display:flex; justify-content:space-between;">
                <span>Best Algorithm: {best_row["Algorithm"]}</span>
                <span>Maximum Value = {best_row["Maximum Value"]}</span>
            </div>
            """,
            unsafe_allow_html=True
          )

            # Sonuç kartları
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="0/1 Knapsack", value=round(res_01, 2))
            with col2:
                st.metric(label="Unbounded Knapsack", value=round(res_unbounded, 2))
            with col3:
                st.metric(label="Fractional Knapsack", value=round(res_fractional, 2))

            tab1, tab2, tab3, tab4 = st.tabs([
                " Results ",
                " Selected Items",
                " Charts",
                " Algorithm Notes"
            ])

            with tab1:
                st.subheader(" Input Items")
                st.dataframe(input_df, use_container_width=True)

                st.subheader(" Algorithm Comparison Results")
                styled_results = results_df.style.highlight_max(
                    subset=["Maximum Value"],
                    color="#bbf7d0"
                ).format({"Execution Time (seconds)": "{:.8f}"})
                st.dataframe(styled_results, use_container_width=True)

            with tab2:
                st.subheader(" Selected Items by Algorithm")

                t1, t2, t3 = st.tabs([
                    "0/1 Knapsack",
                    "Unbounded Knapsack",
                    "Fractional Knapsack"
                ])

                with t1:
                    total_w, total_v, usage = summarize_selected_table(selected_01_df, capacity)
                    st.info(f"Used Capacity: {round(total_w,2)} / {capacity} | Total Value: {round(total_v,2)} | Usage: {round(usage,2)}%")
                    st.dataframe(selected_01_df, use_container_width=True)

                with t2:
                    total_w, total_v, usage = summarize_selected_table(selected_unbounded_df, capacity)
                    st.info(f"Used Capacity: {round(total_w,2)} / {capacity} | Total Value: {round(total_v,2)} | Usage: {round(usage,2)}%")
                    st.dataframe(selected_unbounded_df, use_container_width=True)

                with t3:
                    total_w, total_v, usage = summarize_selected_table(selected_fractional_df, capacity)
                    st.info(f"Used Capacity: {round(total_w,2)} / {capacity} | Total Value: {round(total_v,2)} | Usage: {round(usage,2)}%")
                    st.dataframe(selected_fractional_df, use_container_width=True)

            with tab3:
                fig1, ax1 = plt.subplots(figsize=(8,4))
                ax1.bar(results_df["Algorithm"], results_df["Maximum Value"])
                ax1.set_xlabel("Algorithm")
                ax1.set_ylabel("Maximum Value")
                ax1.set_title("Maximum Value Comparison")
                ax1.tick_params(axis="x", rotation=15)
                

                
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                ax2.bar(results_df["Algorithm"], results_df["Execution Time (seconds)"])
                ax2.set_xlabel("Algorithm")
                ax2.set_ylabel("Execution Time (seconds)")
                ax2.set_title("Execution Time Comparison")
                ax2.tick_params(axis="x", rotation=15)
                
                col1, col2 = st.columns(2)

                with col1:
                    st.pyplot(fig1)

                with col2:
                    st.pyplot(fig2)
            with tab4:
                st.subheader(" Algorithm Notes")
                st.markdown("""
                **0/1 Knapsack DP:** Her ürün en fazla bir kez seçilebilir. Zaman karmaşıklığı **O(n × W)**.

                **Unbounded Knapsack DP:** Aynı üründen sınırsız sayıda seçilebilir. Zaman karmaşıklığı **O(n × W)**.

                **Fractional Knapsack Greedy:** Ürünler parçalı olarak seçilebilir. Ürünler değer/ağırlık oranına göre sıralanır. Zaman karmaşıklığı **O(n log n)**.
                """)

    except ValueError:
        st.error("Lütfen ağırlık ve değer listelerini sadece virgülle ayrılmış sayılar olarak girin.")
