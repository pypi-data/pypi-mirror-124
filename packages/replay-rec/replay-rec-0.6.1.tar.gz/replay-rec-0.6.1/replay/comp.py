# # pylint: disable-all
# import implicit
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# from replay.metrics import *
#
# # from replay.models.ease import EASE
# from rs_datasets import MovieLens
#
# from replay.models import ImplicitWrap, ALSWrap
#
# # from replay.splitters import UserSplitter
# from replay.experiment import Experiment
#
# # from replay.scenarios import MainScenario
#
#
# def filter_num_ratings(df, min_ratings):
#     num_r = df.groupby("user_id").rating.count()
#     num_r = num_r[num_r > min_ratings]
#     df = df[df.user_id.isin(num_r.index)]
#     return df
#
#
# seed = 1337
# k = [10]
# ml = MovieLens("1m")
# df = ml.ratings
# df["relevance"] = df["rating"]
# df = df[df["rating"] >= 4]
# df = filter_num_ratings(df, 10)
#
# item_encoder = LabelEncoder()
# user_encoder = LabelEncoder()
# df.loc[:, "user_id"] = user_encoder.fit_transform(df.loc[:, "user_id"])
# df.loc[:, "item_id"] = item_encoder.fit_transform(df.loc[:, "item_id"])
#
# train, test = train_test_split(df, test_size=0.2, stratify=df.user_id)
#
# train, val = train_test_split(train, test_size=0.2, stratify=train.user_id)
#
# model = implicit.bpr.BayesianPersonalizedRanking(factors=10)
# model = ImplicitWrap(model)
#
# # splitter = UserSplitter(0.3, shuffle=True, drop_cold_items=True, seed=seed)
# # train, test = splitter.split(data)
# e = Experiment(
#     val,
#     [
#         NDCG(),
#         HitRate(),
#         # Coverage(data),
#         # MAP(),
#         # MRR(),
#         # Precision(),
#         Recall(),
#         # RocAuc(),
#         # Surprisal(data),
#         # Unexpectedness(data, RandomPop(data, seed)),
#     ],
#     k,
# )
#
# model.fit(train)
# pred = model.predict(train, 10)
# e.add_result("bpr", pred)
#
# # sc = MainScenario(splitter, ALS,)
