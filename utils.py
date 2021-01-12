from elasticsearch_dsl import Document, Date, Integer, Keyword, Search
from elasticsearch import Elasticsearch

class ProbeRequestClientEntry(Document):
    ap_model = Keyword()
    ap_mac = Keyword()
    mac = Keyword()
    rssi = Integer()
    timestamp = Date()
    class Index:
        name = 'probe_clients'
        settings = {
            "number_of_shards": 2,
        }


def elastic_rssi_post(rssi_list):
    for result in rssi_list:
        try:
            new_entry = ProbeRequestClientEntry()
            new_entry.ap_model = result["ap_model"]
            new_entry.ap_mac = result["ap_mac"]
            new_entry.mac = result["mac"]
            new_entry.rssi = result["rssi"]
            new_entry.timestamp = result["timestamp"]
            new_entry.save()
        except ValueError as ve:
            print(ve)

def delete_index(index, elastic_host="localhost"):
    es = Elasticsearch([elastic_host], scheme="http", port=9200, )
    es.indices.delete(index=index, ignore=[400, 404])


def retrieve_elastic(d_end, d_start, ap_mac="", ue_mac="", elastic_host="localhost:9200"):
    client = Elasticsearch([elastic_host], scheme="http", port=9200,)
    s = Search(using=client, index="probe_clients")
    # querry_time = 1600
    # d_end = datetime.datetime.now()
    # d_start = d_end - datetime.timedelta(minutes=querry_time)
    if ap_mac != "":
        s = s.query("match", ap_mac=ap_mac)
    if ue_mac != "":
        s = s.query("match", mac=ue_mac)
    s = s.filter('range', timestamp={'gte': d_start, 'lt': d_end}).sort('-timestamp')
    total = s.count()
    s = s[0:total]
    response = s.execute()
    # print(len(response))
    # for hit in response:
    #     print("ap_mac: {}, mac: {}, rssi: {}, time: {}".format(hit.ap_mac, hit.mac, hit.rssi, hit.timestamp))
    return response
