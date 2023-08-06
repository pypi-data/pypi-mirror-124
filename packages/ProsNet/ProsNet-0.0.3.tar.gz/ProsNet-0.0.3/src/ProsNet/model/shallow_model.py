from ProsNet.model.model import Model

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import (KNeighborsClassifier)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.metrics import plot_confusion_matrix

class ShallowModel(Model):
    def __init__(self):
        super().__init__()

    def create_model(self, type_of_model, plot_results = False, save_model_results = None):
        if type_of_model == 'knn':
            
            X_train, X_test, y_train, y_test = train_test_split(self.dataset, self.postures, test_size=0.2, random_state=42)
            LABELS = ['Sedentary', 'Standing', 'Stepping', 'Lying']
            
            unique_classes_train, unique_classes_test = self.review_class_imbalance(y_train, y_test, LABELS)
            n_neighbors = 10

            pipeline = make_pipeline(Normalizer(), LinearDiscriminantAnalysis(n_components=2))
            knn = KNeighborsClassifier(n_neighbors=n_neighbors)
            pipeline.fit(X_train, y_train)
            knn.fit(pipeline.transform(X_train), y_train)

            acc_knn = knn.score(pipeline.transform(X_test), y_test)

            X_embedded = pipeline.transform(self.dataset)
            fig, ax = plt.subplots()
            scatter = ax.scatter(X_embedded[:, 0], X_embedded[:, 1], c=self.postures, s=30, cmap='Set1')
            ax.set_title("{}, {}, KNN (k={})\nTest accuracy = {:.2f}".format('Example Set',
                                                                            'Normalized',
                                                                            n_neighbors,
                                                                            acc_knn));
            # produce a legend with the unique colors from the scatter
            legend1 = ax.legend(*scatter.legend_elements(),
                                loc="upper left", title="Classes")
                    
            ax.add_artist(legend1)

            if plot_results:
                plt.grid(False)
                plt.ion()
                plt.show()
                plt.draw()
                plt.pause(0.001)
                input("Press [enter] to continue.")

            if save_model_results is not None:
                plt.savefig(save_model_results + '_plot.png', bbox_inches='tight')

            disp = plot_confusion_matrix(knn, pipeline.transform(X_test), y_test,
                                        #display_labels=LABELS,
                                        cmap=plt.cm.Blues,
                                        normalize='true');

            predicted = knn.predict(pipeline.transform(X_test))

            f = open(save_model_results + '_results.txt',"w+")
            f.write("Classification Results\n")
            f.write(classification_report(y_test, predicted) + "\n")
            f.write('-----------------------')
            f.close

            if plot_results:
                plt.grid(False)
                plt.ion()
                plt.show()
                plt.draw()
                plt.pause(0.001)
                input("Press [enter] to continue.")

            if save_model_results is not None:
                plt.savefig(save_model_results + '_conf_matrix.png', bbox_inches='tight')

        self.model = knn
        self.pipeline = pipeline        

    def compare_best_feature_combo(self):
        import matplotlib.pyplot as plt
        from sklearn.svm import SVC
        from sklearn.feature_selection import RFECV
        from sklearn.feature_selection import RFE

        breakpoint()

        pipeline = make_pipeline(Normalizer(), LinearDiscriminantAnalysis(n_components=2), KNeighborsClassifier(n_neighbors=10))

        transformer = Normalizer().fit(self.dataset)
        X = transformer.transform(self.dataset)
        #X = self.dataset
        y = self.postures

        svc = SVC(kernel="linear")

        min_features_to_select = 1  # Minimum number of features to consider
        rfecv = RFECV(svc, step=1, cv=None, scoring='f1_weighted', min_features_to_select=min_features_to_select)

        rfecv.fit(X, y)

        print(rfecv.support_)
        print(rfecv.ranking_)
        print("Optimal number of features : %d" % rfecv.n_features_)
        print([i for i, x in enumerate(rfecv.support_) if x])

        rfe = RFE(svc, 3)
        rfe = rfe.fit(X, y)
        print(rfe.support_)
        print([i for i, x in enumerate(rfe.support_) if x])

        # Plot number of features VS. cross-validation scores
        plt.figure()
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation score (nb of correct classifications)")
        plt.plot(range(min_features_to_select,
                    len(rfecv.grid_scores_) + min_features_to_select),
                rfecv.grid_scores_)
        plt.show()
        