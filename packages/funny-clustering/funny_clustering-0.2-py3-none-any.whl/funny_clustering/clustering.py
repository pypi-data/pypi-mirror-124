

from sklearn.mixture import GaussianMixture as GMM

def GaussianMixture_clustering(dataset, cluster_count):

    embeddings = dataset.to_numpy()

    gmm = GMM(cluster_count, n_init=2).fit(embeddings)
    labels = gmm.predict(embeddings)

    dataset['clusters'] =  labels.tolist()


    return dataset
