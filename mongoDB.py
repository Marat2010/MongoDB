import pymongo
from settings import Mongo_URI, DB, COLLECTION
from settings import pipelines


def connect_db(mongodb=DB, collection=COLLECTION):
    client = pymongo.MongoClient(Mongo_URI)
    db = client[mongodb]
    collection = db[collection]
    return collection


def get_aggregate_data(data: dict) -> dict:
    coll_input = connect_db(collection='input')
    coll_input.replace_one({"group_type": data['group_type']}, data, upsert=True)

    coll_data = connect_db()

    pipeline = pipelines[data['group_type']]

    pipeline[0]['$match']['dt']['$gte'] = data['dt_from']
    pipeline[0]['$match']['dt']['$lte'] = data['dt_upto']
    pipeline[1]['$addFields']['start_Date'] = data['dt_from']
    pipeline[1]['$addFields']['end_Date'] = data['dt_upto']

    aggr_out = coll_data.aggregate(pipeline)

    try:
        out = list(aggr_out)[0]
    except IndexError:
        return "Нет данных для вывода!"

    coll_output = connect_db(collection='output')
    coll_output.replace_one({}, out, upsert=True)

    return out


if __name__ == '__main__':
    pass


# ================================================
# with open('pipeline_day.json', 'w') as f:
    # json.dump(pipeline_day, f, sort_keys=True,   indent=4)
# -------------------------
# with open('pipeline_month.json', 'w') as f:
#     json.dump(pipeline_month, f, indent=4)
# =================================================


