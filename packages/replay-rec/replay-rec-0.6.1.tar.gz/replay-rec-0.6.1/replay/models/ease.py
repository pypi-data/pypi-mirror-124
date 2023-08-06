#
# import pandas as pd
# from pyspark.ml.clustering import KMeans
#
# from pyspark.sql import functions as sf
# from replay.utils import convert2spark
# %config IPCompleter.use_jedi = False
#
# from rs_datasets import MovieLens
# ml = MovieLens('100k')
# r = ml.ratings
# u = ml.users
# u.drop('zip_code', axis=1, inplace=True)
# u = pd.get_dummies(u)
#
# from pyspark.ml.feature import VectorAssembler
# def transform_features(df):
#     feature_columns = df.drop('user_id').columns
#     vec = VectorAssembler(inputCols=feature_columns, outputCol="features")
#     return vec.transform(df).select('user_id', 'features')
#
# k = 10
# log = convert2spark(r)
# user_features = convert2spark(u)
# df = transform_features(user_features)
# kmeans = KMeans().setK(k).setFeaturesCol("features")
# model = kmeans.fit(df)
# df = model.transform(df).select('user_id', 'prediction').withColumnRenamed('prediction', 'cluster')
# log = log.join(df, on='user_id', how='left')
# log = log.groupBy(['cluster', 'item_id']).agg(sf.count('item_id').alias('count'))
# m = log.groupby('cluster').agg(sf.max('count').alias('max'))
# log = log.join(m, on='cluster', how='left')
# log = log.withColumn('relevance', sf.col('count') / sf.col('max')).drop('count', 'max')
#
# from replay.models import ALSWrap
# rec = ALSWrap()
# rec.fit(log)
