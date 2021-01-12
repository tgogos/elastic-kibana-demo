import time
import random
import datetime
from elasticsearch_dsl.connections import connections
from utils import ProbeRequestClientEntry, retrieve_elastic, elastic_rssi_post

ELASTIC_IP = "localhost"


def init_elastic(elastic_ip):
    connections.create_connection(hosts=[elastic_ip])
    ProbeRequestClientEntry.init()


def feed_data():
    probes = []
    for ii in range(10):    # how many minutes
        for i in range(60): # generate 60 random rssi values
            time.sleep(1)   # per second
            probes.append({"ap_model": "mikrotik", "ap_mac": "11:22:33:44:55:66",
                           "mac": "77:88:99:AA:BB:CC", "rssi": random.randint(-20, -10),
                           "timestamp": datetime.datetime.utcnow()})
        print("Data to be fed:")
        print(probes)
        elastic_rssi_post(probes)


def retrieve_data():
    query_time = 20
    d_end = datetime.datetime.now()
    d_start = d_end - datetime.timedelta(seconds=query_time)
    results = retrieve_elastic(d_end, d_start, ap_mac="11:22:33:44:55:66", ue_mac="77:88:99:AA:BB:CC",
                               elastic_host="{}:9200".format(ELASTIC_IP))
    print("Data read:")
    print(results)
    for res in results:
        print(res.rssi)


def main():
    init_elastic(ELASTIC_IP)
    feed_data()
    time.sleep(1)
    retrieve_data()


if __name__ == "__main__":
    main()
