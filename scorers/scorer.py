from abc import ABC, abstractmethod

import pandas as pd
import pyspark.pandas as ps
from pyspark.ml import Pipeline
from pyspark.ml.feature import BucketedRandomProjectionLSH, RFormula, StandardScaler
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


class LshScorer(ABC):

    def __init__(self, model_provider, dataset, company_id):
        self.model_provider = model_provider
        self.dataset = dataset
        self.company_id = company_id

    @abstractmethod
    def train_and_score(self, dataset: pd.DataFrame):
        pass


class PandasLshScorer(LshScorer, ABC):
    def __init__(self, model_provider, dataset, company_id):
        super().__init__(model_provider, dataset, company_id)
        self.model_provider = model_provider

    def train_and_score(self, dataset: pd.DataFrame):
        pass


class SparkLshScorer(LshScorer, ABC):
    def __init__(self, model_provider, dataset, company_id):
        super().__init__(model_provider, dataset, company_id)
        self.model_provider = model_provider
        self.dataset = dataset
        self.company_id = company_id
        self.spark = SparkSession.builder.appName('lsh-scoring') \
            .config("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()

    def train_and_score(self, model_path, save_model):
        # name  accepted  id  revenue
        df_spark = self.spark.createDataFrame(self.dataset).drop("name", "id")
        df_spark.show()

        rf = RFormula(formula="accepted ~ revenue",
                      featuresCol="features",
                      labelCol="label")

        scaler = StandardScaler(inputCol="features", outputCol="scaled_features",
                                withStd=True, withMean=False)

        brp = BucketedRandomProjectionLSH(inputCol="scaled_features",
                                          outputCol="hashes",
                                          bucketLength=2.0,
                                          numHashTables=3)

        pipeline = Pipeline(stages=[rf, scaler, brp])
        pipeline_model = pipeline.fit(df_spark)

        if save_model:
            pipeline_model.write().overwrite().save(model_path)

        query = df_spark.where(col("id") == self.company_id).select(col("accepted"), col("revenue"))
        query_vector = pipeline_model.transform(query).select(col("scaled_features")).collect()[0][0]
        transformed = pipeline_model.transform(df_spark)

        brp = pipeline_model.stages[-1]

        neighbors = brp.approxNearestNeighbors(transformed.select("scaled_features"), query_vector, 3)

        neighbors.show()

        # TODO develop some logic to decide like majority vote ?

        return "Yes"

    def process_sink_delta_feature_store(self, delta_dataset_path) -> None:
        psdf = ps.from_pandas(self.dataset)
        psdf.to_delta(delta_dataset_path)
        # TODO return delta version for logging ?
