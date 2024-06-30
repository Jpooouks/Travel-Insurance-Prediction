import pandas as pd

def find_outliers(df):
    outlier_indices = []
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            column_outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
            
            outlier_indices.extend(column_outliers)
    
    unique_outlier_indices = list(set(outlier_indices))
    
    return df.loc[unique_outlier_indices]


def shorten_param(param_name):
    if "__" in param_name:
        return param_name.rsplit("__", 1)[1]
    return param_name


def get_result_df(param_dist, pipeline):
    column_results = [f"param_{name}" for name in param_dist.keys()]
    column_results += ["mean_test_score", "std_test_score", "rank_test_score"]

    cv_results = pd.DataFrame(pipeline.cv_results_)
    cv_results = cv_results[column_results].sort_values(
    "mean_test_score", ascending=False
    )
    return cv_results.rename(shorten_param, axis=1)