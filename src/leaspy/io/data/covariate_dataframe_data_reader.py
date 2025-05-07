import warnings

import pandas as pd

from leaspy.exceptions import LeaspyDataInputError
from leaspy.utils.typing import Dict, FeatureType, IDType, List, Optional

from .abstract_dataframe_data_reader import AbstractDataframeDataReader
from .individual_data import IndividualData
from .visit_dataframe_data_reader import VisitDataframeDataReader

__all__ = ["CovariateDataframeDataReader"]


class CovariateDataframeDataReader(AbstractDataframeDataReader):
    """
    Methods to convert :class:`pandas.DataFrame` to `Leaspy`-compliant data containers for longitudinal data with covariates.

    Parameters
    ----------
    covariate_names: List[str]
        Names of the columns in dataframe that contains the covariates

    Raises
    ------
    :exc:`.LeaspyDataInputError`
    """

    def __init__(
        self,
        *,
        covariate_names: List[str],
    ):
        super().__init__()
        if not covariate_names:
            raise LeaspyDataInputError("You must prrovide at least one covariate name.")
        self.covariate_names = covariate_names
        self.visit_reader = VisitDataframeDataReader()

    ######################################################
    #               ABSTRACT METHODS IMPLEMENTED
    ######################################################

    def _check_headers(self, columns: List[str]) -> None:
        """
        Check mendatory dataframe headers

        Parameters
        ----------
        columns: List[str]
            Names of the columns headers of the dataframe that contains patients information
        """
        self.visit_reader._check_headers(columns)

    def _set_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Set the index suited for the type of information contained in the dataframe

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with patient information

        Returns
        -------
        df: pd.DataFrame
            Dataframe with the right index
        """

        return self.visit_reader._set_index(df)

    def _clean_dataframe(
        self, df: pd.DataFrame, *, drop_full_nan: bool, warn_empty_column: bool
    ) -> pd.DataFrame:
        """
        Clean the dataframe that contains patient information

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with patient information

        drop_full_nan: bool
            If set to True, raw full of nan are droped

        warn_empty_column: bool
            If set to True, a warning is raise for columns full of nan


        Returns
        -------
        df: pd.DataFrame
            Dataframe with clean information
        """

        # Check visits
        df_visits = self.visit_reader._clean_dataframe(
            df.drop(columns=self.covariate_names),
            drop_full_nan=drop_full_nan,
            warn_empty_column=warn_empty_column,
        )

        # à compléter
        return df

    def _load_individuals_data(
        self, subj: IndividualData, df_subj: pd.DataFrame
    ) -> None:
        """
        Convert information stored in a dataframe to information stored into IndividualData

        Parameters
        ----------
        subj: IndividualData
            One patient with her/his information, potentially empty

        df_subj: pd.DataFrame
            One patient with her/his information
        """
        self.visit_reader._load_individuals_data(subj, df_subj)
        # partie covariables à changer
        self.event_reader._load_individuals_data(subj, df_subj)
