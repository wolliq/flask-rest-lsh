import pandas as pd
from abc import ABC, abstractmethod

from pyspark.ml.feature import BucketedRandomProjectionLSH
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors


class LshScorer(ABC):

    def __init__(self, model_provider, dataset, company_id):
        self.model_provider = model_provider
        self.dataset = dataset
        self.company_id = company_id

    @abstractmethod
    def train(self, dataset: pd.DataFrame):
        pass


class PandasLshScorer(LshScorer, ABC):
    def __init__(self, model_provider, dataset, company_id):
        super().__init__(model_provider, dataset, company_id)
        self.model_provider = model_provider

    def train(self, dataset: pd.DataFrame):
        pass


class SparkLshScorer(LshScorer, ABC):
    def __init__(self, model_provider, dataset, company_id):
        super().__init__(model_provider, dataset, company_id)
        self.model_provider = model_provider
        self.spark = SparkSession.builder.appName('lsh-scoring').getOrCreate()

    def train(self):
        dataA = [(0, Vectors.dense([1.0, 1.0]),),
                 (1, Vectors.dense([1.0, -1.0]),),
                 (2, Vectors.dense([-1.0, -1.0]),),
                 (3, Vectors.dense([-1.0, 1.0]),)]

        key = Vectors.dense([1.0, 0.0])

        brp = BucketedRandomProjectionLSH(inputCol="features", outputCol="hashes", bucketLength=2.0,
                                          numHashTables=3)
        dfA = self.spark.createDataFrame(dataA, ["id", "features"])

        model = brp.fit(dfA)

        print("Approximately searching dfA for 2 nearest neighbors of the key:")
        model.approxNearestNeighbors(dfA, key, 2).show()

    def process_delta_feature_store(self, dataset_path):
        pass
