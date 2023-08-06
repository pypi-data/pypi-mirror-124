from featurestorebundle.entity.Entity import Entity
from featurestorebundle.feature.FeatureList import FeatureList
from pyspark.sql import types as t
from gql import gql, Client
from logging import Logger


class MetadataDBSender:
    def __init__(
        self,
        logger: Logger,
        gql_client: Client,
    ):
        self.__logger = logger
        self.__gql_client = gql_client

    def send(self, schema: t.StructType(), feature_list: FeatureList, entity: Entity):
        for field in schema[2:]:
            if field.name in feature_list.get_names():
                gql_query = gql(
                    f"""
                        mutation {{
                            createFeature(entity: "{entity.name}", name: "{field.name}", description: "{field.metadata.get('comment')}", category: "{field.metadata.get('category')}") {{
                                id,
                                existing,
                            }}
                        }}
                    """
                )

                try:
                    self.__gql_client.execute(gql_query)

                except BaseException:
                    self.__logger.warning("Cannot reach metadata api server. The metadata will not be written.")
