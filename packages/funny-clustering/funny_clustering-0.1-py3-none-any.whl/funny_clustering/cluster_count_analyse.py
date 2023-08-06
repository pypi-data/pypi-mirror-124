import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture as GMM
from sklearn import metrics
from sklearn.model_selection import train_test_split
from matplotlib import rcParams

rcParams['figure.figsize'] = 16, 8




def SelBest(arr: list, X: int) -> list:
    '''
    returns the set of X configurations with shorter distance
    '''
    dx = np.argsort(arr)[:X]
    return arr[dx]


def GaussianMixture_analyse_cluster_count(dataset,  cluster_count=10):

    embeddings = dataset.to_numpy()

    print('Silhouette Scores for {} clusters'.format(cluster_count))
    n_clusters=np.arange(2, cluster_count)
    sils=[]
    sils_err=[]
    iterations=cluster_count
    for n in n_clusters:
        tmp_sil=[]
        for _ in range(iterations):
            gmm=GMM(n, n_init=2).fit(embeddings)
            labels=gmm.predict(embeddings)
            sil=metrics.silhouette_score(embeddings, labels, metric='euclidean')
            tmp_sil.append(sil)
        val=np.mean(SelBest(np.array(tmp_sil), int(iterations/5)))
        err=np.std(tmp_sil)
        sils.append(val)
        sils_err.append(err)
        print('Iteration {} ...'.format(n))

    plt.errorbar(n_clusters, sils, yerr=sils_err)
    plt.title("Silhouette Scores", fontsize=20)
    plt.xticks(n_clusters)
    plt.xlabel("N. of clusters")
    plt.ylabel("Score")
    plt.show()

    #Courtesy of https://stackoverflow.com/questions/26079881/kl-divergence-of-two-gmms. Here the difference is that we take the squared root, so it's a proper metric

    def gmm_js(gmm_p, gmm_q, n_samples=10**5):
        X = gmm_p.sample(n_samples)[0]
        log_p_X = gmm_p.score_samples(X)
        log_q_X = gmm_q.score_samples(X)
        log_mix_X = np.logaddexp(log_p_X, log_q_X)

        Y = gmm_q.sample(n_samples)[0]
        log_p_Y = gmm_p.score_samples(Y)
        log_q_Y = gmm_q.score_samples(Y)
        log_mix_Y = np.logaddexp(log_p_Y, log_q_Y)

        return np.sqrt((log_p_X.mean() - (log_mix_X.mean() - np.log(2))
                + log_q_Y.mean() - (log_mix_Y.mean() - np.log(2))) / 2)


    print('Distance between Train and Test GMMs')
    n_clusters = np.arange(2, cluster_count)
    iterations = cluster_count
    results = []
    res_sigs = []
    for n in n_clusters:
        dist = []

        for iteration in range(iterations):
            train, test = train_test_split(embeddings, test_size=0.5)

            gmm_train = GMM(n, n_init=2).fit(train)
            gmm_test = GMM(n, n_init=2).fit(test)
            dist.append(gmm_js(gmm_train, gmm_test))
        selec = SelBest(np.array(dist), int(iterations / 5))
        result = np.mean(selec)
        res_sig = np.std(selec)
        results.append(result)
        res_sigs.append(res_sig)
        print('Iteration {} ...'.format(n))


    plt.errorbar(n_clusters, results, yerr=res_sigs)
    plt.title("Distance between Train and Test GMMs", fontsize=20)
    plt.xticks(n_clusters)
    plt.xlabel("N. of clusters")
    plt.ylabel("Distance")
    plt.show()


    print('BIC Scores')
    n_clusters = np.arange(2, cluster_count)
    bics = []
    bics_err = []
    iterations = cluster_count
    for n in n_clusters:
        tmp_bic = []
        for _ in range(iterations):
            gmm = GMM(n, n_init=2).fit(embeddings)

            tmp_bic.append(gmm.bic(embeddings))
        val = np.mean(SelBest(np.array(tmp_bic), int(iterations / 5)))
        err = np.std(tmp_bic)
        bics.append(val)
        bics_err.append(err)
        print('Iteration {} ...'.format(n))

    plt.errorbar(n_clusters,bics, yerr=bics_err, label='BIC')
    plt.title("BIC Scores", fontsize=20)
    plt.xticks(n_clusters)
    plt.xlabel("N. of clusters")
    plt.ylabel("Score")
    plt.legend()
    plt.show()


    plt.errorbar(n_clusters, np.gradient(bics), yerr=bics_err, label='BIC')
    plt.title("Gradient of BIC Scores", fontsize=20)
    plt.xticks(n_clusters)
    plt.xlabel("N. of clusters")
    plt.ylabel("grad(BIC)")
    plt.legend()
    plt.show()


