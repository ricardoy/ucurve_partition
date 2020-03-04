# import numpy as np
# from sklearn.preprocessing import Normalizer
# from sklearn.pipeline import make_pipeline

# from vapnik.classification import convert_partition_blocks_to_kernel, convert_X
# from vapnik.perceptron import Perceptron


# def _evaluate_cost(X_train, Y_train, X_test, Y_test, X_val, Y_val, epochs, normalize):
#     if normalize:
#         transformer = Normalizer()
#         X_train = transformer.fit_transform(X_train)
#         X_test = transformer.transform(X_test)
#         X_val = transformer.transform(X_val)
#
#     p = Perceptron(epochs=epochs)
#     p.fit(X_train, Y_train)
#     predicted = p.predict(X_train)
#     ein = np.sum(predicted != Y_train) / (Y_train.shape[0])
#
#     predicted = p.predict(X_test)
#     etest = np.sum(predicted != Y_test) / Y_test.shape[0]
#
#     predicted = p.predict(X_val)
#     eval = np.sum(predicted != Y_val) / Y_val.shape[0]
#
#     return ein, etest, eval
#
#
# def evaluate_cost(X_train, Y_train, X_test, Y_test, X_val, Y_val, partition, epochs, normalize=True, cross_validation=True):
#     kernel = convert_partition_blocks_to_kernel(partition.blocks)
#     X_train_converted = convert_X(X_train, kernel)
#     X_test_converted = convert_X(X_test, kernel)
#     X_val_converted = convert_X(X_val, kernel)
#
#     if cross_validation:
#         X_train = np.concatenate([X_train_converted, X_val_converted])
#         Y_train = np.concatenate([Y_train, Y_val])
#
#         _, etest, _ = _evaluate_cost(X_train, Y_train, X_test_converted, Y_test, X_val_converted, Y_val, epochs, normalize)
#
#         k = 10
#         n = X_train.shape[0]
#         if n < k:
#             raise AttributeError('Training dataset should have more than {} items.'.format(k))
#
#         eval = 0
#         ein = 0
#         for i in range(k):
#             X = np.concatenate([X_train[0:i * n // k], X_train[(i + 1) * n // k:]])
#             Y = np.concatenate([Y_train[0:i * n // k], Y_train[(i + 1) * n // k:]])
#
#             X_ = X_train[i*n//k:(i+1)*n//k]
#             Y_ = Y_train[i*n//k:(i+1)*n//k]
#
#             if normalize:
#                 transformer = Normalizer()
#                 X = transformer.fit_transform(X)
#                 X_ = transformer.transform(X_)
#
#             p = Perceptron(epochs=epochs)
#             p.fit(X, Y)
#             predicted = p.predict(X)
#             ein += np.sum(predicted != Y) / (Y.shape[0])
#
#             predicted = p.predict(X_)
#             eval += np.sum(predicted != Y_) / Y_.shape[0]
#         eval = eval / k
#         ein = ein / k
#     else:
#         ein, etest, eval = _evaluate_cost(X_train_converted, Y_train, X_test_converted, Y_test, X_val_converted, Y_val, epochs, normalize)
#
#     return ein, etest, eval


def convert_to_binary_tuple(x:int, n:int):
    v = []
    for _ in range(n):
        v.append(x%2)
        x = x//2
    return tuple(v[::-1])


def binary_tuple_to_key(v):
    return ''.join([str(x) for x in v])


def children_generator(x, n):
    for i in range(len(x)):
        if x[i] == 1:
            v = []
            for j in range(0, i):
                v.append(x[j])
            v.append(0)
            for j in range(i+1, n):
                v.append(x[j])
            yield v