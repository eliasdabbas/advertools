from itertools import product

import pandas as pd
import requests

if int(pd.__version__[0]) >= 1:
    from pandas import json_normalize
else:
    from pandas.io.json import json_normalize


def _dict_product(d):
    items = list(d.items())
    keys = [x[0] for x in items]
    values = [x[1] for x in items]
    dicts = []
    for prod in product(*values):
        tempdict = dict(zip(keys, prod))
        dicts.append(tempdict)
    return dicts


def _json_to_df(json_resp, params):
    json = json_resp.json()
    resp_types = [(type(json[key]).__name__, key) for key in json]
    df = pd.DataFrame()
    for typ, key in resp_types:
        if typ == "list":
            df = json_normalize(json[key])
        if len(df) == 0:
            df = pd.DataFrame([0], columns=["delete_me"])

    for typ, key in resp_types:
        if typ == "str":
            df[key] = json[key]
        if typ == "dict":
            df = df.assign(**json[key])
    for col in df:
        if "Count" in col:
            try:
                df[col] = df[col].astype("int64")
            except ValueError:
                continue
        if ("published" in col) or ("updated" in col):
            try:
                df[col] = pd.to_datetime(df[col])
            except ValueError:
                continue
    df = df.assign(**{"param_" + key: val for key, val in params.items()})
    if "delete_me" in df:
        df = df.drop(columns=["delete_me"])
    df["queryTime"] = pd.Timestamp.now(tz="UTC")
    return df


def _combine_requests(params, base_url, count, max_allowed):
    supplied_params = {k: v for k, v in params.items() if params[k] is not None}
    for p in supplied_params:
        if (not isinstance(supplied_params[p], int)) and len(supplied_params[p]) == 0:
            raise ValueError("please make sure you supply a value for {}".format(p))
        if isinstance(supplied_params[p], (str, int)):
            supplied_params[p] = [supplied_params[p]]

    params_list = _dict_product(supplied_params)

    if count not in [None, 0]:
        max_count_div_mod = divmod(count, max_allowed)
        last_iter = [] if max_count_div_mod[1] == 0 else [max_count_div_mod[1]]
        iteration_list = [max_allowed] * max_count_div_mod[0] + last_iter
    elif count == 0:
        iteration_list = [0]
    else:
        iteration_list = [None]
    responses = []
    for param in params_list:
        for i, count in enumerate(iteration_list):
            param["maxResults"] = count
            param["pageToken"] = (
                None if i == 0 else responses[-1]["nextPageToken"].values[-1]
            )
            resp = requests.get(base_url, params=param)
            responses.append(_json_to_df(resp, param))
            if "errors" in responses[-1]:
                continue
            if iteration_list != [None]:
                if responses[-1]["totalResults"].values[-1] < sum(
                    iteration_list[: i + 1]
                ):
                    break
    return pd.concat(responses, ignore_index=True, sort=False).drop(
        columns=["param_key"]
    )
