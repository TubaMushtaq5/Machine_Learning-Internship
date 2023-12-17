# #pip install streamlit
# #streamlit run techelectro_customer_data.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the preprocessed DataFrame
df = pd.read_csv('TechElectroCustomerData.csv')

# Apply K-means clustering
optimal_clusters = 3
num_cols = ['Age', 'AnnualIncome (USD)', 'TotalPurchases']
data_scaled = StandardScaler().fit_transform(df[num_cols])
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
df['Cluster'] = kmeans.fit_predict(data_scaled)

# Perform one-hot encoding for categorical columns
categorical_cols = ['Gender', 'MaritalStatus', 'PreferredCategory']
transformer = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_cols)],
    remainder='passthrough'
)
data_encoded = transformer.fit_transform(df)
df_encoded = pd.DataFrame(data_encoded, columns = transformer.get_feature_names_out(df.columns))

# Streamlit Dashboard
st.title('TechElectro Customer Segmentation Dashboard')

# Sidebar filters
st.sidebar.title('Filters')
selected_cluster = st.sidebar.selectbox('Select a Cluster', df['Cluster'].unique())
selected_gender = st.sidebar.selectbox('Select Gender', df['Gender'].unique())
selected_category = st.sidebar.selectbox('Select Preferred Category', df['PreferredCategory'].unique())

# ... (previous code)

# Display EDA Visualizations
st.header('Exploratory Data Analysis')



# Count plot of Preferred Category by Gender
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='PreferredCategory', hue='Gender')
plt.title('Preferred Category by Gender')
plt.xlabel('Preferred Category')
plt.ylabel('Count')
plt.legend(title='Gender', loc='upper right', labels=['Male', 'Female'])
# Pass the figure to st.pyplot()
st.pyplot(plt.gcf())  # Get the current figure

# Correlation heatmap
correlation_matrix = df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
# Pass the figure to st.pyplot()
st.pyplot(plt.gcf())  # Get the current figure

# Distribution plots for numerical features
plt.figure(figsize=(12, 8))
for column in num_cols:
    sns.histplot(df[column], bins=20, kde=True)
    plt.title(column)
    # Pass the figure to st.pyplot()
    st.pyplot(plt.gcf())  # Get the current figure

# Display Customer Segmentation Results
st.header('Customer Segmentation')
st.subheader('Cluster Distribution')
cluster_counts = df['Cluster'].value_counts()
st.bar_chart(cluster_counts)

