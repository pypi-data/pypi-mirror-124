# # pylint: disable-all
#
# from replay.metrics import *
# import pandas as pd
# import numpy as np
#
# # from replay.models.ease import EASE
# from rs_datasets import MovieLens
#
# from replay.models import ALSWrap
#
# from replay.experiment import Experiment
#
# from replay.splitters import DateSplitter
# from copy import deepcopy
#
#
#
# seed = 1337
# k = 50
# ml = MovieLens("1m")
# df = ml.ratings
# df["relevance"] = df["rating"]
#
# max_date = pd.to_datetime(df.timestamp.max(), unit='s')
#
# test_date = pd.to_datetime('2002-02-01')
# train_date = pd.to_datetime('2002-01-01')
# # test_date = pd.to_datetime('2014-03-01')
# # train_date = pd.to_datetime('2014-02-01')
#
# df['timestamp'] = pd.to_datetime(df.timestamp, unit='s')
# df['timestamp'] = df.timestamp.dt.strftime('%Y-%m-%d')
#
# splitter2 = DateSplitter(test_date, True, True)
# splitter1 = DateSplitter(train_date)
#
# train1, rest = splitter1.split(df)
# _, test = splitter2.split(rest)
# train2, _ = splitter2.split(df)
#
#
# model1 = ALSWrap(seed=156)
# model2 = ALSWrap(seed=156)
#
# p1 = model1.fit_predict(train1, 50)
# p2 = model2.fit_predict(train2, 50)
#
#
# e = Experiment(
#     test,
#     [
#         NDCG(),
#         HitRate(),
#         Recall(),
#     ],
#     k,
# )
#
#
# e.add_result("base", p1)
# e.add_result("updated", p2)
# model1.model.set()
#
# old_user = model1.model.userFactors.toPandas()
# new_user = model2.model.userFactors.toPandas()
# old_item = model1.model.itemFactors.toPandas()
# new_item = model2.model.itemFactors.toPandas()
#
# np.dot(new_user.iloc[0].features, new_item.iloc[0].features)
# np.dot(old_user.iloc[0].features, old_item.iloc[0].features)
# np.dot(old_user.iloc[0].features, new_item.iloc[0].features)
# np.dot(new_user.iloc[0].features, old_item.iloc[0].features)
