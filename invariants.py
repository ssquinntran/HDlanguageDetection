from pylab import *
from numpy import *
import mnist_numpy

images, labels = mnist_numpy.load_mnist('training', digits=[0,1,2,3,4,5,6,7,8,9],path="data/")
# images is (60000, 28, 28)
# to get images in 1,0's...
# for i in range(0,len(images)):
#     images[i] /= 255.0
# imshow(images.mean(axis=0), cmap=cm.gray)
# imshow(images[1], cmap=cm.gray)
# show()

# isn't this the average tho?
# but we include mapping huehue
invariants = zeros((10,28,28))
# stores the indices for the actual images
reference_images = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}
for i in range(0,len(images)):
    invariants[labels[i]] += images[i]
    reference_images[labels[i]].append(i)

imshow(invariants[2], cmap=cm.gray)
show()