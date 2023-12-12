import numpy as np

class K_Nearest_Neighbors_Classifier:

    def __init__( self, K ) :
        self.K = K

    # Function to store training set
    def fit( self, X_train, Y_train ) :
        self.X_train = X_train
        self.Y_train = np.array(Y_train)
        self.m, self.n = X_train.shape

    # Function for prediction
    def predict( self, X_test ) :
        self.X_test = X_test
        self.m_test, self.n = X_test.shape # no_of_test_examples, no_of_features
        Y_predict = [None]*self.m_test
        # np.zeros( self.m_test ) # initialize Y_predict

        for i in range( self.m_test ) :
            x = self.X_test[i]
            # find the K nearest neighbors from current test example
            neighbors = np.zeros( self.K )

            neighbors = self.find_neighbors( x )
            bincount = {}
            for neighbor in neighbors:
                if neighbor not in bincount:
                    bincount[neighbor] = 1
                else:
                    bincount[neighbor] += 1

            # most frequent class in K neighbors
            prediction = max(bincount, key=bincount.get)
            Y_predict[i] = prediction

        return Y_predict


    def find_neighbors( self, x ) :

        euclidean_distances = np.zeros( self.m )

        for i in range( self.m ) :
            d = self.euclidean( x, self.X_train[i] )
            euclidean_distances[i] = d

        euclidean_distances = np.array(euclidean_distances)
        inds = euclidean_distances.argsort()
        Y_train_sorted = self.Y_train[inds]
        return Y_train_sorted[:self.K]


    # Function to calculate euclidean distance
    def euclidean( self, x, x_train ) :

        return np.sqrt( np.sum( np.square( x - x_train ) ) )