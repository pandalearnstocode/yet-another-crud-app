import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
DATA_PATH = "https://raw.githubusercontent.com/elleobrien/wine/master/wine_quality.csv"

async def train_model(
    data_path=DATA_PATH,
    y_var="quality",
    split_ratio=0.2,
    seed=42,
):
    df = pd.read_csv(data_path)
    y = df.pop(y_var)
    X_train, X_test, y_train, y_test = train_test_split(
        df, y, test_size=split_ratio, random_state=seed
    )
    regr = RandomForestRegressor(max_depth=2, random_state=seed)
    regr.fit(X_train, y_train)
    train_score = regr.score(X_train, y_train) * 100
    test_score = regr.score(X_test, y_test) * 100
    importances = regr.feature_importances_
    labels = df.columns
    feature_df = pd.DataFrame(
        list(zip(labels, importances)), columns=["feature", "importance"]
    )
    feature_df = feature_df.sort_values(by="importance", ascending=False,)
    y_pred = regr.predict(X_test) + np.random.normal(0, 0.25, len(y_test))
    y_jitter = y_test + np.random.normal(0, 0.25, len(y_test))
    res_df = pd.DataFrame(list(zip(y_jitter, y_pred)), columns=["true", "pred"])
    return await {
        "residuals_data": res_df.to_dict(orient="list"),
        "feature_importance_data": feature_df.to_dict(orient="list"),
        "train_score": train_score,
        "test_score": test_score,
    }

