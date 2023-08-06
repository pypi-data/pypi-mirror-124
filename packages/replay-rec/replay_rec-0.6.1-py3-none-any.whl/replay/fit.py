from rs_datasets import MovieLens
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from replay.models import MultVAE


def encode(df):
    ue = preprocessing.LabelEncoder()
    ie = preprocessing.LabelEncoder()
    df["user_id"] = ue.fit_transform(df["user_id"])
    df["item_id"] = ie.fit_transform(df["item_id"])
    return df, ue, ie


version = "10m"
df = MovieLens(version).ratings
df, ue, ie = encode(df)
train, test = train_test_split(
    df, test_size=0.2, random_state=1, stratify=df["user_id"]
)
model = MultVAE(epochs=30, latent_dim=64)
model.fit(train)
