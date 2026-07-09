from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd
import numpy as np


def makeTrainingData(dfFeatures: pd.DataFrame, featureColumns: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series] :
    X = dfFeatures[featureColumns]
    y = dfFeatures["heavy_rain"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test

def logModel(X_train : pd.DataFrame, y_train : pd.Series) -> LogisticRegression:

    model = LogisticRegression(class_weight='balanced')
    return model.fit(X_train, y_train)

def xgbModel(X_train : pd.DataFrame, y_train : pd.Series) -> XGBClassifier:
    # Calculate ratio
    ratio = y_train.value_counts()[0] / y_train.value_counts()[1]

    xgb_model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        eval_metric="logloss",
        tree_method="hist",
        scale_pos_weight=ratio
    )

    return xgb_model.fit(X_train, y_train)

def rfModel(X_train : pd.DataFrame, y_train : pd.Series) -> RandomForestClassifier:
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_leaf=10,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    return rf_model.fit(X_train, y_train)

def rfThresholdTune(y_prob : np.ndarray, y_test : pd.Series, thresholds: list[float] = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]) -> pd.DataFrame:
    results = []

    for threshold in thresholds:
        y_pred = (y_prob >= threshold).astype(int)

        results.append({
            "Threshold": threshold,
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1": f1_score(y_test, y_pred)
        })

    return pd.DataFrame(results)