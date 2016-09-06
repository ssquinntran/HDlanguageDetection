from mnist import MNIST
import sklearn.metrics as metrics
import numpy as np

NUM_CLASSES = 10

def load_dataset():
    mndata = MNIST('./data/')
    X_train, labels_train = map(np.array, mndata.load_training())
    X_test, labels_test = map(np.array, mndata.load_testing())
    X_train = X_train/255.0
    X_test = X_test/255.0
    X_train = X_train[:,:,np.newaxis]
    X_test = X_test[:,:,np.newaxis]
    return (X_train, labels_train), (X_test, labels_test)


def train(X_train, y_train, reg=0):
    ''' Build a model from X_train -> y_train '''
    # data X, labels y
    print "y_train"
    #print y_train
    print y_train.shape
    
    np.reshape(X_train,(X_train.shape[0],X_train.shape[1]))
    print "X_train"
    #print X_train. there are nonzeros in X_train
    print X_train.shape
    model = np.zeros((X_train.shape[0], y_train.shape[0]))
    for row in range(0,y_train.shape[0]):
        for col in range(0,X_train.shape[1]):
            model[row][col] = X_train[row][col]

    print "model"
    print model.shape
    return model

def one_hot(labels_train):
    '''Convert categorical labels 0,1,2,....9 to standard basis vectors in R^{10} '''
    vectors = np.zeros((X_train.shape[0], NUM_CLASSES))
    for row in range(0,len(labels_train)):
        #for col in range(0,NUM_CLASSES):
        vectors[row][labels_train[row]] = 1
    return vectors


def predict(model, X):
    ''' From model and data points, output prediction vectors '''
    # sign( x.w + b)
    # classification = np.sign(np.dot(np.array(features),self.w)+self.b)
    # weights = np.ones(X.shape[0]) # row vector
    # b = 0

    print "X"
    #print X
    print X.shape
    predictions = np.zeros(X.shape[0])
    # DIMENSIONS IDK
    #for i in range(0,X.shape[0]):
    #    classification = np.dot(model,X[i])
    #    predictions[i] = classification
    
    #print predictions
    print "predictions"
    print predictions.shape
    return predictions

if __name__ == "__main__":
    (X_train, labels_train), (X_test, labels_test) = load_dataset()
    model = train(X_train, labels_train)
    # why we never use these!?
    # y_train = one_hot(labels_train)
    # y_test = one_hot(labels_test)

    pred_labels_train = predict(model, X_train)
    pred_labels_test = predict(model, X_test)


    print("Train accuracy: {0}".format(metrics.accuracy_score(labels_train, pred_labels_train)))
    print("Test accuracy: {0}".format(metrics.accuracy_score(labels_test, pred_labels_test)))
