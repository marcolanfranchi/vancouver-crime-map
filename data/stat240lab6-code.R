# Problem 1: k-means
# a)

library(flexclust)

my.dist2 <- function(df1, df2) {
  
  n <- nrow(df1)
  k <- nrow(df2)
  
  eucl_matrix = matrix(0, n, k)
  for (i in 1:n) {
    for (j in 1:k) {
      eucl_matrix[i, j] <- sqrt(sum((df1[i,] - df2[j,])^2))
    }
  }
  return(eucl_matrix)
}



df1 = read.csv("df1.csv", header = TRUE)
df2 = read.csv("df2.csv", header = TRUE)

# my result 
result_1a = my.dist2(df1, df2)
print("My function, my.dist2, when ran with two sample data frames outputs:")
print(result_1a)

# flexcat's dist2() function result
result_flexcat = dist2(df1, df2)
print("flextcat's funcitons, dist2, when ran with the same two sample data 
      frames outputs:")
print(result_flexcat)


# -----------------------------------------------------------------------------
# b)

my.kmeans = function(data, K, max_iterations = 100, threshold = 0.001) {
  
  N = dim(data)[1]; 
  cols = ncol(data);
  
  # randomly assigning each data item in df to one of the K clusters
  set.seed(240);
  cluster = sample(K, size = N, replace = TRUE)
  data$cluster = cluster;
 
  # creating a matrix to contain the centroids of each cluster
  centroids = matrix(NA, K, cols + 1);
  colnames = rep(list(0), cols+1);
  for (c in 1:cols) {
    colnames[c] = paste0("v", c)
  }
  colnames[cols+1] = paste0("cluster");
  colnames(centroids) = colnames;
  
  # begin iterating, where iteration stops if max_iterations is reached 
  for (i in 1:max_iterations) {
  
    # computing the mean x and y coordinate of each cluster (the centroids)
    for (k in 1:K) {
      for (r in 1:cols) {
        data_cluster_k = data[data$cluster == k,]
        centroids[k,r] = mean(data_cluster_k[,r])
      }
      centroids[k,cols+1] = k
    }
    
    # Reassigning each data item to the cluster with the closest centroid
    d = my.dist2(data[,1:cols], centroids[,1:cols])
    for (n in 1:N) {
      data$cluster[n] = which.min(d[n,])
      
      # if all centroids move by only a small amount (threshold), stop
      # iterating through the main loop
      count = 0;
      for (x in 1:nrow(d)) {
        for (y in 1:ncol(d)) {
          if (d[x,y] < threshold) {
            count = count + 1;
          }
        }
      }
      if (count == dim(d)[1]*dim(d)[2]) {
        break
      }
    }
  }
  
  # return a named list containing 1) the centroids, and 2) the cluster
  # assignments from the last iteration of the algorithm
  return(list(centroids = centroids, clusters = data$cluster))
}


# -----------------------------------------------------------------------------
# c)

library(ggplot2)

stu_num = 301433830
k = as.numeric(strsplit(as.character(stu_num),"")[[1]])[1]

clust = k + 1

dataset = read.csv(file = "simulated_data.csv", header = TRUE)
data1 = dataset[,1:ncol(dataset)-1]

# running my.kmeans on the simulated data
my_kmeans = my.kmeans(data1, K = clust)


# Making a scatter plot with the results from my.kmeans
data1$cluster = my_kmeans$clusters
plot1 = ggplot(data1, aes(x = x, y = y, color = as.factor(cluster))) + 
  labs(color = "cluster") + theme_minimal() + geom_point() +
  ggtitle("k-means clustering done by my functions");
print(plot1)


# -------------------------------------------------
# now, running R's kmeans function on the same data


original_data = read.csv(file = "simulated_data.csv", header = TRUE)
data2 = original_data[,1:ncol(original_data)-1]


# running my.kmeans on the data
kmeans = kmeans(data2, centers = clust)


# Making a scatter plot with the results from my.kmeans
data2$cluster = kmeans$cluster
plot2 = ggplot(data2, aes(x = x, y = y, color = as.factor(cluster))) + 
  labs(color = "cluster") + theme_minimal() + geom_point() + 
  ggtitle("k-means clustering done by the kmeans function");
print(plot2)






