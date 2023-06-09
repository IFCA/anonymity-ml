# Copyright 2022 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import numpy as np
import pandas as pd
import typing
from pycanon.anonymity.utils.aux_anonymity import get_equiv_class

"""
Calculate metrics for measuring data utility and anonymization quality: adult dataset
"""


def calculate_cavg(
    db: pd.DataFrame,
    db_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sup=True,
) -> float:
    """Average equivalence class size when suppression is allowed.

    :param db: dataframe with the data raw under study.
    :type db: pandas dataframe

    :param db_anon: dataframe with the data anonymized.
    :type db_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sup: boolean, default to True. If true, suppression has been applied to the
            original dataset (some records may have been deleted).
    :type  sup: boolean
    """
    ec = get_equiv_class(db_anon, quasi_ident)
    if sup:
        return len(db_anon) / (len(ec) * k)
    else:
        return len(db) / (len(ec) * k)


def calculate_cm(
    db: pd.DataFrame,
    db_anon: pd.DataFrame,
    quasi_ident: typing.Union[typing.List, np.ndarray],
    sens_att: str,
) -> float:
    """Calculate the classification metric.

    :param db: dataframe with the data raw under study.
    :type db: pandas dataframe

    :param db_anon: dataframe with the data anonymized.
    :type db_anon: pandas dataframe

    :param quasi_ident: list with the name of the columns of the dataframe
            that are quasi-identifiers.
    :type quasi_ident: list of strings

    :param sens_att: sensitive attributes which will be the label
            in a classification task.
    :type sens_att: string
    """
    n = len(db)
    m = len(db_anon)
    cm = n - m
    eqs = get_equiv_class(db_anon, quasi_ident)
    for eq in eqs:
        sa_eq = db_anon.iloc[eq, :][sens_att].values
        unique, counts = np.unique(sa_eq, return_counts=True)
        for i in counts:
            if i != max(counts):
                cm += i
    return cm / n


QI = ["age", "education", "relationship", "occupation", "sex", "native-country"]
SA = "salary-class"
db = pd.read_csv("../data/adult.csv")

print("Results for C_avg")
for k in [2, 5, 10, 15, 20, 25, 50, 75, 100]:
    file = f"adult_k{k}_new.csv"
    db_anon = pd.read_csv(f"../data/{file}")
    c_avg = calculate_cavg(db, db_anon, QI, k, sup=True)
    print(f"File: {file}, C_avg: {c_avg}")

print("\nResults for CM")
files = [
    "adult_k5_new.csv",
    "adult_k5_l2_new.csv",
    "adult_k5_t07_new.csv",
    "adult_k5_delta15_new.csv",
]
for file in files:
    db_anon = pd.read_csv(f"../data/{file}")
    print(f"File: {file}, CM: {calculate_cm(db, db_anon, QI, SA)}")
