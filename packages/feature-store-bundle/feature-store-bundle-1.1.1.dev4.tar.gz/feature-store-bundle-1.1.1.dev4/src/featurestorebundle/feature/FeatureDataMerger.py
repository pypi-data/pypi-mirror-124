from delta.tables import DeltaTable
from featurestorebundle.entity.Entity import Entity
from featurestorebundle.feature.FeatureList import FeatureList
from logging import Logger
from pyspark.sql import SparkSession, DataFrame
from typing import Dict


class FeatureDataMerger:
    __source = "source"
    __target = "target"

    def __init__(self, metadata_api_enabled: bool, logger: Logger, spark: SparkSession):
        self.__metadata_api_enabled = metadata_api_enabled
        self.__logger = logger
        self.__spark = spark

    def merge(
        self,
        entity: Entity,
        feature_list: FeatureList,
        features_data: DataFrame,
        pk_columns: list,
        target_table_path: str,
    ):
        feature_names = feature_list.get_names()
        data_column_names = [
            field.name for field in features_data.schema.fields if field.name not in [entity.id_column, entity.time_column]
        ]

        self.__check_feature_count(data_column_names, feature_names)

        def wrap_source(column: str):
            return f"{FeatureDataMerger.__source}.{column}"

        update_set = {feature_name: wrap_source(data_col_name) for data_col_name, feature_name in zip(data_column_names, feature_names)}
        if entity.time_column not in pk_columns:
            update_set = {entity.time_column: wrap_source(entity.time_column), **update_set}

        insert_set = {pk_col: wrap_source(pk_col) for pk_col in pk_columns}
        merge_conditions = " AND ".join(f"{FeatureDataMerger.__target}.{pk_col} = {wrap_source(pk_col)}" for pk_col in pk_columns)

        self.__merge_features_into_table(features_data, target_table_path, update_set, insert_set, merge_conditions)

    def __merge_features_into_table(
        self, features_data: DataFrame, target_table_path: str, update_set: Dict, insert_set: Dict, merge_conditions: str
    ):
        delta_table = DeltaTable.forPath(self.__spark, target_table_path)

        self.__logger.info(f"Writing feature data into {target_table_path}")

        (
            delta_table.alias(FeatureDataMerger.__source)
            .merge(features_data.alias(FeatureDataMerger.__target), merge_conditions)
            .whenMatchedUpdate(set=update_set)
            .whenNotMatchedInsert(values={**insert_set, **update_set})
            .execute()
        )

    def __check_feature_count(self, data_column_names: list, feature_names: list):
        if len(data_column_names) != len(feature_names):
            raise Exception(
                f"Number or dataframe columns ({len(data_column_names)}) != number of features instances matched ({len(feature_names)})"
            )
