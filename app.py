import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Market Basket Analyzer", page_icon="🛒", layout="wide")
st.title("🛒 Market Basket Analyzer")
st.markdown("Upload transaction data, generate insights, visualize frequent patterns, and download results.")

# Sidebar: Upload file
st.sidebar.header("📁 Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Upload transactions.csv", type="csv")

# Sidebar: Filters
min_support = st.sidebar.slider("📊 Min Support", 0.0, 1.0, 0.5, 0.05)
min_conf = st.sidebar.slider("🔗 Min Confidence", 0.0, 1.0, 0.6, 0.05)
min_lift = st.sidebar.slider("⚖️ Min Lift", 0.0, 3.0, 1.0, 0.1)

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file, header=None, on_bad_lines='skip')
        transactions = []
        for i in range(len(data)):
            transactions.append([
                str(data.values[i, j]) for j in range(len(data.columns))
                if str(data.values[i, j]) != 'nan'
            ])

        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_items = apriori(df, min_support=min_support, use_colnames=True)
        rules = association_rules(frequent_items, metric="lift", min_threshold=min_lift)
        rules = rules[rules['confidence'] >= min_conf]

        # Layout columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Frequent Itemsets")
            st.dataframe(frequent_items)

        with col2:
            st.subheader("🔗 Association Rules")
            st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

        # 🔽 Download buttons
        st.sidebar.markdown("### 📥 Download Results")
        st.sidebar.download_button("📥 Itemsets CSV", frequent_items.to_csv(index=False).encode('utf-8'), "itemsets.csv", "text/csv")
        st.sidebar.download_button("📥 Rules CSV", rules.to_csv(index=False).encode('utf-8'), "rules.csv", "text/csv")

        # 📊 Bar Chart of top frequent items
        st.subheader("📊 Top Frequent Items")
        item_counts = frequent_items.explode('itemsets')
        item_counts['item'] = item_counts['itemsets'].astype(str).str.replace("frozenset\\(|\\)|\\{|\\}|'", "", regex=True)
        item_counts = item_counts.groupby('item')['support'].sum().reset_index().sort_values(by='support', ascending=False).head(10)
        fig = px.bar(item_counts, x='item', y='support', title='Top 10 Frequent Items')
        st.plotly_chart(fig, use_container_width=True)

        # 🔗 Network Graph of Rules
        st.subheader("🧠 Association Rule Network")
        if not rules.empty:
            G = nx.DiGraph()
            for _, row in rules.iterrows():
                antecedent = ', '.join(list(row['antecedents']))
                consequent = ', '.join(list(row['consequents']))
                G.add_edge(antecedent, consequent, weight=row['lift'])

            plt.figure(figsize=(10, 6))
            pos = nx.spring_layout(G, k=0.5)
            nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, edge_color='gray')
            st.pyplot(plt)
        else:
            st.info("No rules found based on current filters.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("👆 Upload a valid CSV file to get started.")
