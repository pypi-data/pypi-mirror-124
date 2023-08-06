from delta.tables import DeltaTable
from featurestorebundle.entity.Entity import Entity
from featurestorebundle.feature.FeatureList import FeatureList
from featurestorebundle.metadata.MetadataWriter import MetadataWriter
from logging import Logger
from pyspark.sql import SparkSession, DataFrame


class FeatureDataMerger:
    def __init__(self, metadata_api_enabled: bool, logger: Logger, spark: SparkSession, metadata_writer: MetadataWriter):
        self.__metadata_api_enabled = metadata_api_enabled
        self.__logger = logger
        self.__spark = spark
        self.__metadata_writer = metadata_writer

    def merge(
        self,
        entity: Entity,
        feature_list: FeatureList,
        features_data: DataFrame,
        pk_columns: list,
        target_table_path: str,
        metadata_table_path: str,
    ):
        feature_names = feature_list.get_names()
        data_column_names = [
            field.name for field in features_data.schema.fields if field.name not in [entity.id_column, entity.time_column]
        ]

        if len(data_column_names) != len(feature_names + [entity.time_column]):
            raise Exception(
                f"Number or dataframe columns ({len(data_column_names)}) != number of features instances matched ({len(feature_names)})"
            )

        def source_wrap(column: str):
            return f"source.{column}"

        update_set = {feature_name: source_wrap(data_col_name) for data_col_name, feature_name in zip(data_column_names, feature_names)}

        if entity.time_column in pk_columns:
            update_set = {entity.time_column: source_wrap(entity.time_column), **update_set}

        insert_set = {pk_col: f"source.{pk_col}" for pk_col in pk_columns}

        merge_conditions = " AND ".join(f"target.{pk_col} = source.{pk_col}" for pk_col in pk_columns)

        delta_table = DeltaTable.forPath(self.__spark, target_table_path)

        self.__logger.info(f"Writing feature data into {target_table_path}")

        (
            delta_table.alias("target")
            .merge(features_data.alias("source"), merge_conditions)
            .whenMatchedUpdate(set=update_set)
            .whenNotMatchedInsert(values={**insert_set, **update_set})
            .execute()
        )

        self.__metadata_writer.write(metadata_table_path, feature_list)
