import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans

# def my_kmeans(data, K, max_iterations=1000, threshold=0.001):
#     N = data.shape[0]
#     cols = data.shape[1]

#     np.random.seed(240)

#     cluster = np.random.choice(K, size=N, replace=True)
#     data['cluster'] = cluster

#     centroids = np.zeros((K, cols + 1))
#     colnames = [f"v{i}" for i in range(cols)] + ['cluster']

#     for k in range(K):
#         data_cluster_k = data[data['cluster'] == k]
#         centroids[k, :cols] = data_cluster_k.mean(axis=0)
#         centroids[k, cols] = k

#     for i in range(max_iterations):
#         d = np.linalg.norm(data.iloc[:, :cols].values[:, None] - centroids[:, :cols], axis=2)
#         cluster_assignment = np.argmin(d, axis=0)
#         data['cluster'] = cluster_assignment

#         if np.all(d < threshold):
#             break

#         for k in range(K):
#             data_cluster_k = data[data['cluster'] == k]
#             centroids[k, :cols] = data_cluster_k.mean(axis=0)
#             centroids[k, cols] = k

#     return centroids, data['cluster']

df = pd.read_csv("data/simulated_data.csv")

st.title("K-Means Visualizer", )
st.markdown("infooo")
st.markdown("info2")

st.subheader('Simulated Data')
st.dataframe(df)

# Display the scatter plot of the simulated data
st.subheader('Scatter Plot of Simulated Data')
fig, ax = plt.subplots()
ax.scatter(df['x'], df['y'], c='blue')
ax.set_xlabel('x')
ax.set_ylabel('y')

st.pyplot(fig)

original_data = pd.read_csv('data/simulated_data.csv')
data2 = original_data.iloc[:, :-1]

if st.button('Execute k-means algorithm'):
    # Perform K-means clustering using scikit-learn
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(data2)
    cluster_assignments = kmeans.labels_

    # Update the original dataset with the cluster assignments
    original_data['cluster'] = cluster_assignments

    # Display the scatter plot with colored clusters
    fig, ax = plt.subplots()
    ax.scatter(original_data['x'], original_data['y'], c=original_data['cluster'])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    st.subheader('K-means Clustering (scikit-learn)')
    st.pyplot(fig)
