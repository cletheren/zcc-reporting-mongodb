import certifi

from pymongo import MongoClient


class Cluster:
    def __init__(self, uri: str) -> None:
        self.connection = MongoClient(uri, tlsCAFile=certifi.where())


class Collection:
    def __init__(self, cluster: Cluster, database: str, collection: str) -> None:
        self.database = cluster.connection[database]
        self.collection = self.database[collection]


class Client:
    def __init__(self, username: str, password: str, database: str) -> None:
        self.uri = f"mongodb+srv://{username}:{password}@cluster0.ehaeufa.mongodb.net/?retryWrites=true&w=majority"
        self.cluster = Cluster(self.uri)
        self.databases = {
            "queue_detail_voice": Collection(self.cluster, database, "queue_detail_voice"),
            "queue_detail_video": Collection(self.cluster, database, "queue_detail_video"),
            "queue_detail_chat": Collection(self.cluster, database, "queue_detail_chat"),
            "queue_detail_sms": Collection(self.cluster, database, "queue_detail_sms"),
            "queue_report_voice": Collection(self.cluster, database, "queue_report_voice"),
            "queue_report_video": Collection(self.cluster, database, "queue_report_video"),
            "queue_report_chat": Collection(self.cluster, database, "queue_report_chat"),
            "queue_report_sms": Collection(self.cluster, database, "queue_report_sms"),
        }
