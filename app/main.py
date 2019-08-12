import os, sys, random
from influxdb import InfluxDBClient
import urllib3
import certifi
from bs4 import BeautifulSoup

# 関数定義

# influxdbへ書き込み処理を行う
def insert(measurement, values):
    client = InfluxDBClient(
        host=os.environ['INFLUXDB_HOST'],
        port=os.environ['INFLUXDB_PORT'],
        database=os.environ['INFLUXDB_DATABASE']
    )

    json_payload = [
    {
        "measurement": measurement,
        "fields": values
    }
    ]
    client.write_points(json_payload)

# アマオクをスクレイピングして値を取得する
def scrape(url):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    res = http.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    table_body = soup.select_one('#tbody1')

    amounts = []
    rates = []
    for tr in table_body.find_all('tr'):
        temp_list = []
        for td in tr.find_all('td'):
            temp_list.append(td.string)
        amounts.append(int(temp_list[0].replace('枚', ''))) # "チケット枚数"リストに追加
        rates.append(float(temp_list[3].replace('%', ''))) # "レート"リストに追加

    # 最良レート、ワーストレート
    best_rate = min(rates) ; worst_rate = max(rates)

    # レート平均(重みつき)
    avg = 0
    for i in range(len(rates)):
        avg += amounts[i] * rates[i]
    avg = round(avg / sum(amounts), 2)

    return {'best_rate': best_rate, 'worst_rate': worst_rate, 'avg': avg, 'amount_sum': sum(amounts)} # チケット枚数の総量: sum(amounts)

# main
def main():
    # 変数定義
    url = 'https://url.of.webpage/' # スクレイピング先URL
    measurement = 'amaoku' # テーブル名

    # アマオクのWebサイトをスクレピングして値を取得
    values = scrape(url)
    # influxdbへ書き込み
    insert(measurement, values)

if __name__ == '__main__':
    main()
