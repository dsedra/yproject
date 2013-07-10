import svmlight

training_data = __import__('data').train0
test_data = __import__('data').test0

train = [ 
((1,0),[(1,0.5),(2,0.125)]),
((1,0),[(1,0.25),(2,0.125)]),
((1,0),[(1,1.75),(2,0.0)]),
((0,1),[(1,0.125),(2,0.25)]),
((0,1),[(1,0.5),(2,1)]),
((0,1),[(1,0.3),(2,0.4)])]
#(3,[(1,0.125),(2,0.2)]),
#(3,[(1,0),(2,0)]),
#(3,[(1,1),(2,1.1)])]


test = [
(1,[(1,1.0),(2,0.1)]),
(2,[(1,0.1),(2,2.1)])]

# train a model based on the data
model = svmlight.learn(train, type='ranking', verbosity=0)

# model data can be stored in the same format SVM-Light uses, for interoperability
# with the binaries.
svmlight.write_model(model, 'my_model.dat')

# classify the test data. this function returns a list of numbers, which represent
# the classifications.
predictions = svmlight.classify(model, test)
for p in predictions:
    print '%.8f' % p
