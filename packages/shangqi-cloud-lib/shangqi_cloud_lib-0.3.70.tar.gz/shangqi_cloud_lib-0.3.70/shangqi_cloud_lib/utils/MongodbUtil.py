import logging
import traceback
from datetime import datetime, timedelta

from bson import ObjectId
from pymongo import MongoClient

from shangqi_cloud_lib.context import config
from shangqi_cloud_lib.utils.AesUtil import decrypt_oralce
from shangqi_cloud_lib.utils.CommonUtil import is_empty


def mongodb_connect_with_db(collection_name, db_name="core"):
    db = mongodb_connect(db_name)
    try:
        return db[collection_name]
    except:
        logging.warning("连接数据库异常:" + traceback.format_exc())
    return ""


# mongodb_connect('industry_knowledge_engine',host="123.57.158.203",port=27017,user="work",pwd="MhxzKhl")
def mongodb_connect(param="core", host=config.mongo_ip, port=config.mongo_port,
                    user=config.mongo_user, pwd=config.mongo_password):
    try:
        client = MongoClient(host, port, connect=False)
        db = client.admin  # 先连接系统默认数据库admin
        db.authenticate(user, pwd, mechanism='SCRAM-SHA-1')
        db = client[param]
        return db
    except:
        logging.warning("连接数据库异常:" + traceback.format_exc())
    return ""


def convert_to_mongo(value):
    if isinstance(value, str) and not is_empty(value):
        if (value[0] == "'" and value[-1] == "'") or (value[0] == '"' and value[-1] == '"'):
            return value
        else:
            return "'" + value + "'"
    elif isinstance(value, list):
        result = "[{}]"
        temp_list = []
        for item in value:
            temp_list.append(convert_to_mongo(item))
        return result.format(",".join(temp_list))
    return str(value)


def prepare_for_mongo(params: dict):
    result = {}
    for key, value in params.items():
        result[key] = convert_to_mongo(value)
    return result


def query_params_for_mongo(db, query: str, params=None):
    query = query.strip()
    if params and isinstance(params, dict):
        prepared = prepare_for_mongo(params)
        for key, value in prepared.items():
            query = query.replace("%({0})s".format(key), value)
    if "findOne" in query:
        query = query.replace("findOne", "find_one")
    if config.echo_sql:
        print(query)
    res = eval(query)
    return res


def condition_by_lookup(find_condition_list, relevance_chart_name, localField="ent_name", foreignField="ent_name"):
    lookup_dict = {
        "lookup": {
            "from": relevance_chart_name,
            "localField": localField,
            "foreignField": foreignField,
            "as": "ent_name",

        }
    }
    find_condition_list.append(lookup_dict)


def condition_by_round(aggregate_list, round_size, is_round):
    if is_round is True:
        round_dict = {
            "$sample": {"size": round_size}
        }
        aggregate_list.append(round_dict)


def condition_by_limit_skip(aggregate_list, limit, skip):
    aggregate_list.append({
        "$skip": skip
    })
    aggregate_list.append({
        "$limit": limit
    })


def condition_by_aggregate_sort(aggregate_list, sort_dict):
    for sort in sort_dict:
        aggregate_list.append({
            "$sort": {sort: sort_dict[sort]}
        })


def condition_by_find_sort(sort_dict):
    result_sort_list = []
    for sort in sort_dict:
        result_sort_list.append((sort, sort_dict[sort]))
    return result_sort_list


def condition_by_in(find_condition, column, param_list, is_object=False, _include=True, is_need_decrypt_oralce=False):
    if param_list is not None and len(param_list) > 0:
        if is_object:
            param_list = [ObjectId(id) for id in param_list]
        if is_need_decrypt_oralce:
            param_list = [int(decrypt_oralce(id)) for id in param_list]
        if _include is True:
            find_condition[column] = {"$in": param_list}
        else:
            find_condition[column] = {"$ne": {"$in": param_list}}


def condition_by_eq(find_condition, column, param, _include=True):
    if param != "":
        if _include is True:
            find_condition[column] = param
        else:
            find_condition[column] = {"$ne": param}


def condition_by_and(and_condition_list, param_list):
    if param_list is not None:
        and_condition_list = and_condition_list + param_list
    return and_condition_list


def condition_by_like(find_condition, column, data):
    if data:
        find_condition[column] = {"$regex": data}


def condition_by_right_like(find_condition, column, company_name):
    if company_name != "":
        find_condition[column] = {"$regex": '^' + company_name + ".*"}


def condition_by_city_name(find_condition, city_name, city_include):
    if city_name != "":
        if city_include is True:
            find_condition["city"] = city_name
        else:
            find_condition["city"] = {"$ne": city_name}


def condition_by_between(column, data_list, and_condition_list, is_contain_end_date=True):
    if data_list:
        if data_list[0]:
            and_condition_list.append({column: {"$gte": data_list[0]}})
        if len(data_list) == 2 and data_list[1]:
            if "-" in str(data_list[1]) and is_contain_end_date:
                end = str((datetime.strptime(data_list[1], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d"))
            else:
                end = data_list[1]
            and_condition_list.append({column: {"$lte": end}})


def condition_by_elemMatch(column, elemMatch_column, data_list, and_condition_list, is_contain_end_date=True):
    if data_list:
        if data_list[0]:
            and_condition_list.append({column: {
                '$elemMatch': {
                    elemMatch_column: {
                        '$gte': data_list[0]
                    }
                }
            }})
        if len(data_list) == 2 and data_list[1]:
            if "-" in str(data_list[1]) and is_contain_end_date:
                end = str((datetime.strptime(data_list[1], '%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d"))
            else:
                end = data_list[1]
            and_condition_list.append({column: {
                '$elemMatch': {
                    elemMatch_column: {
                        '$gte': end
                    }
                }
            }})


def mongodb_result_to_list(mongodb_data):
    result_list = []
    for data in mongodb_data:
        result_list.append(data)
    return result_list


def mongodb_sql_paging(page_size, page_number):
    limit_number = int(page_size)
    skip_number = (int(page_number) - 1) * int(page_size)

    return limit_number, skip_number


def mongodb_collection(db_name, collection):
    try:
        client = MongoClient(config.mongo_ip, config.mongo_port)
        db = client.admin  # 先连接系统默认数据库admin
        db.authenticate(config.mongo_user, config.mongo_password, mechanism='SCRAM-SHA-1')
        db = client[db_name]
        return db[collection]
    except:
        logging.warning("连接数据库异常:" + traceback.format_exc())
    return ""


class MgSession:
    def __init__(self, db="core", host=config.mongo_ip, user=config.mongo_user,
                 port=config.mongo_port,
                 pwd=config.mongo_password):
        self.db = mongodb_connect(db, host, port, user, pwd)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            logging.info(f'type:{exc_type}')
            logging.info(f'value:{exc_val}')
            logging.info(f'trace:{exc_tb}')
            logging.error(exc_tb)
            return False
        return True

    def execute(self, sql, params=None):
        return query_params_for_mongo(self.db, sql, params)

    def collection(self, table):
        return self.db[table]

    def insert(self, table, values):
        self.collection(table).insert(values)

    def update(self, table, condition, values, upsert=False):
        self.collection(table).update(condition, {"$set": values}, upsert=upsert)

    def query(self, table, condition={}, columns=None):
        columns_dict = {}
        if columns:
            if isinstance(columns, dict):
                columns_dict.update(columns)
            elif isinstance(columns, list):
                for column_name in columns:
                    columns_dict[column_name] = 1
        if columns_dict:
            cursor = self.collection(table).find(condition, columns_dict)
        else:
            cursor = self.collection(table).find(condition)
        return cursor

    def aggregate(self, table, args):
        return self.collection(table).aggregate(args)

    def query_list(self, sql, params=None, data_type="dict", columns: list = None):
        res = query_params_for_mongo(self.db, sql, params)
        if data_type == "dict":
            return list(res)
        elif data_type == "cursor":
            return res
        elif data_type == "list":
            result = []
            for item in res:
                result_item = []
                if not columns:
                    columns = item.keys()
                for column in columns:
                    result_item.append(item[column])
                result.append(result_item)
            return result

    def query_one(self, sql, params=None, data_type="dict", columns: list = None):
        res = query_params_for_mongo(self.db, sql, params)
        if data_type == "dict":
            return res
        elif data_type == "list":
            result = []
            if not columns:
                columns = res.keys()
            for column in columns:
                result.append(res[column])
            return result
