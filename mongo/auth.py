import certifi

from pymongo import MongoClient


class Cluster:
    def __init__(self, uri: str) -> None:
        self.client = MongoClient(uri, tlsCAFile=certifi.where())


class Collection:
    def __init__(self, cluster: Cluster, database: str, collection: str) -> None:
        self.database = cluster.connection[database]
        self.collection = self.database[collection]


class Client:
    def __init__(self, username: str, password: str, database: str) -> None:
        self.uri = f"mongodb+srv://{username}:{password}@cluster0.ehaeufa.mongodb.net/?retryWrites=true&w=majority"
        self.cluster = Cluster(self.uri)
        self.databases = {
            "voice": Collection(self.cluster, database, "queue_detail_voice"),
            "video": Collection(self.cluster, database, "queue_detail_video"),
            "chat": Collection(self.cluster, database, "queue_detail_chat"),
            "queue_report_voice": Collection(
                self.cluster, database, "queue_report_voice"
            ),
        }
