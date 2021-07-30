from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class mongo:
    
    def __init__(self,host,username,password,dbname):
        self.host = host
        self.username = username
        self.password = password

        try:
            db = MongoClient('mongodb://{}:{}@{}/{}'.format(username,password,host,dbname))
            self.db = db[dbname]
            
        except ConnectionFailure:
            print("Fail to connect to MongoDB Server!")
        
    def mongo_insert(self,db_collection,data):
        col_name = self.db[db_collection]
        res = col_name.insert_one(data)
        return res

    def mongo_return_all(self,db_collection):
        data = []
        col_name = self.db[db_collection]
        dts = col_name.find()
        
        for dt in dts:
            data.append(dt)
        
        return data
    
    def mongo_count_stats(self,db_collection,reference_keys):
        stats = {}
        """
        docstring
        """
        col_name = self.db[db_collection]
        pri_dist_keys = col_name.distinct(reference_keys[0])
        sec_dist_keys = col_name.distinct(reference_keys[1])

        for pKey in pri_dist_keys:
            tmp = {}
            for sKey in sec_dist_keys:                
                count = col_name.find({reference_keys[0]:pKey, reference_keys[1]:sKey}).count()

                tmp[int(sKey)] = count

            stats[int(pKey)] = tmp

        return stats