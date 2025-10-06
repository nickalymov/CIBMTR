import pandas as pd
from lifelines import CoxPHFitter
from lifelines import KaplanMeierFitter

def apply_cox_model(df):

    data = df.copy()

    data['event'] = data['efs']

    cph = CoxPHFitter()

    features = [col for col in data.columns if col not in ['efs', 'efs_time', 'event']]

    cph.fit(data[features + ['efs_time', 'event']], duration_col='efs_time', event_col='event')

    data['target'] = cph.predict_partial_hazard(data[features])

    return data


def apply_kaplan_meier(df):

    kmf = KaplanMeierFitter()

    df['target'] = 0.0

    kmf.fit(durations=df['efs_time'], event_observed=df['efs'])

    for i in range(len(df)):

        df.loc[i, 'target'] = kmf.predict(df.loc[i, 'efs_time'])

    return df