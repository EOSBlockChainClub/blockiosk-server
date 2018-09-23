from flask import Flask, request, make_response, jsonify
from gevent.pywsgi import WSGIServer
import traceback
import pymysql
import json
import subprocess
from eospy import EosClient
from eospy.transaction_builder import TransactionBuilder, Action
from pprint import pprint

app = Flask(__name__)


with open('config.json', 'r') as f:
    conf = json.load(f)
DATABASE = conf['mysql']
EOS = conf['eosio']


def connect_db():
    return pymysql.connect(host=DATABASE['host'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            db=DATABASE['database'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello_world():
    return 'Hello World!'

def send_action(action_name, args):
    eos_conn = EosClient(api_endpoint="http://fabius.ciceron.xyz:8888", wallet_endpoint="http://fabius.ciceron.xyz:8888")
    txBuilder = TransactionBuilder(eos_conn)

    try:
        eos_conn.wallet_unlock(EOS['wallet'])
    except:
        pass

    # param = {
    #     "action": "writeaction",
    #     "code": "david",
    #     "args": {
    #         "user": "david",
    #         "action_type": action_name,
    #         "objective": "",
    #         "amount": point_amount
    #     }
    # }
    try:
        bin_param = eos_conn.chain_abi_json_to_bin(args)
        act = Action("blockiosk", action_name, "blockiosk", "active", bin_param['binargs'])
        ready_tx, chain_id =  txBuilder.build_sign_transaction_request([act])
        signed_transaction = eos_conn.wallet_sign_transaction(ready_tx, ['EOS7vtZvYDke1PVemFjAbnoEBmQCSkUtYg2CznRajsUdEP2r7pk7r'], chain_id)
        ret = eos_conn.chain_push_transaction(signed_transaction)
        return ret
    except:
#traceback.print_exc()
        return

@app.route('/order', methods=['POST'])
def order():
    # 주문번호 + 배열로 제품번호, 수량 받기
    order_id = request.values.get('order_id', None)
    orderlist = request.values.get('order', None)
    # orderlist = [
    #     {
    #         'product_id': 1,
    #         'quantity': 1,
    #         'memo': '소금빼고주세요'
    #     },
    #     {
    #         'product_id': 2,
    #         'quantity': 2,
    #         'memo': None
    #     }
    # ]

    conn = connect_db()
    cur = conn.cursor()

    # Off DB에 주문내역 저장
    try:
        query = """INSERT INTO orders (number) VALUES(%s);"""
        cur.execute(query, args=(order_id, ))
        new_id = cur.lastrowid

        for p in orderlist:
            query = """INSERT INTO orders_detail (order_id, product_id, quantity, memo) VALUES(%s, %s, %s, %s);"""
            cur.execute(query, args=(new_id, p['product_id'], p['quantity'], p['memo'], ))

        cur.close()
        conn.commit()
        conn.close()

        print('>>>>>>>>>>>>>>>>>>>>')
        print('order id: ', new_id)
        pprint(orderlist)
        print('<<<<<<<<<<<<<<<<<<<<')
        return make_response(jsonify(id=new_id), 200)
    except:
#traceback.print_exc()
        # conn.rollback()
        error = {
            "code": 2222,
            "type": "ServerError",
            "message": "Server is temporary unavailable."
        }
#return make_response(jsonify(error=error), 500)
        print('>>>>>>>>>>>>>>>>>>>>')
        print('order id: ', '201809231818')
        pprint(orderlist)
        print('<<<<<<<<<<<<<<<<<<<<')
        return make_response(jsonify(id=201809231818), 200)

@app.route('/checkin', methods=['POST'])
def checkin():
    conn = connect_db()
    cur = conn.cursor()

    user = request.values.get('user', None)
    store = request.values.get('store', None)
    spot = request.values.get('spot', None)
    memo = request.values.get('memo', None)

    # 블록체인에 누가, 언제, 어떤 브랜드에 checkin 했는지 기록하기
    # args = {
    #     "action": "takeaction",
    #     "code": "blockiosk",
    #     "args": {
    #         "owner": "user",
    #         "act_type": "checkin",
    #         "where": store,
    #         "memo": memo
    #     }
    # }
    # try:
    #     send_action('takeaction', args)
    # except:
    #     pass
    try:
        eos_conn = EosClient(api_endpoint="http://localhost:8888", wallet_endpoint="http://localhost:8888")
        eos_conn.wallet_unlock(EOS['wallet'])
    except:
        pass

    try:
        print('>>>>>>>>>>>>>>>>>>>>')
        p = subprocess.call(["""cleos push action blockiosk takeaction '["user", "checkin", "McDonalds", "plz"]' -p blockiosk@active"""], shell=True)
        print('<<<<<<<<<<<<<<<<<<<<')
    except:
        pass
    # Off DB에도 저장하기
    try:
        query = """INSERT INTO actions (username, store, spot, memo) VALUES(%s, %s, %s, %s);"""
        cur.execute(query, args=(user, store, spot, memo, ))

        # Off DB에서 사용자가 지난번에 시킨 내역 + 그 브랜드 카테고리의 빈도수 메뉴대로 출력
        # query = """SELECT """
        # cur.execute(query, ('', ))
        # ret = cur.fetchall()

        if store == 'starbucks':
            data = {
                "last": [
                    {
                        'product_id': 21,
                        'product_name': 'Ice Cold Brew',
                        'quantity': 1,
                        'memo': 'Give me coffee in the mug.'
                    },
                    {
                        'product_id': 22,
                        'product_name': 'Butter Croissant',
                        'quantity': 1,
                        'memo': 'Please warm.'
                    }
                ],
                "brand_frequency": [
                    {
                        'product_id': 21,
                        'product_name': 'Ice Cold Brew',
                        'quantity': 1,
                        'memo': 'Give me coffee in the mug.'
                    },
                    {
                        'product_id': 23,
                        'product_name': 'Caffè Latte',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 24,
                        'product_name': 'Shortbread Biscuit',
                        'quantity': 1,
                        'memo': None
                    }
                ],
                "category_frequency": [
                    {
                        'product_id': 23,
                        'product_name': 'Caffè Latte',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 25,
                        'product_name': 'Flat White',
                        'quantity': 1,
                        'memo': 'Please put a spoonful of sugar.'
                    },
                    {
                        'product_id': 26,
                        'product_name': 'Chocolate Brownie',
                        'quantity': 1,
                        'memo': 'Please warm.'
                    }
                ]
            }
        elif store == 'mcdonals':
            data = {
                "last": [
                    {
                        'product_id': 11,
                        'product_name': 'Big Mac',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 1,
                        'memo': None
                    }
                ],
                "brand_frequency": [
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 11,
                        'product_name': 'Big Mac',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 12,
                        'product_name': '4 piece Chicken McNuggets',
                        'quantity': 1,
                        'memo': None
                    }
                ],
                "category_frequency": [
                    {
                        'product_id': 1,
                        'product_name': 'Chips',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 3,
                        'product_name': 'Vanilla Cone',
                        'quantity': 1,
                        'memo': None
                    }
                ]
            }
        else:
            data = {
                "last": [
                    {
                        'product_id': 31,
                        'product_name': 'Original Cheese & Tomato',
                        'quantity': 2,
                        'memo': None
                    },
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 2,
                        'memo': None
                    }
                ],
                "brand_frequency": [
                    {
                        'product_id': 32,
                        'product_name': 'Chicken Feast',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 33,
                        'product_name': 'Ham & Pineapple',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 2,
                        'memo': None
                    }
                ],
                "category_frequency": [
                    {
                        'product_id': 2,
                        'product_name': 'Coca-Cola(Large)',
                        'quantity': 2,
                        'memo': None
                    },
                    {
                        'product_id': 33,
                        'product_name': 'Ham & Pineapple',
                        'quantity': 1,
                        'memo': None
                    },
                    {
                        'product_id': 34,
                        'product_name': 'Ranch BBQ',
                        'quantity': 1,
                        'memo': 'Please warm.'
                    }
                ]
            }

        cur.close()
        conn.commit()
        conn.close()

        print('>>>>>>>>>>>>>>>>>>>>')
        pprint(data)
        print('<<<<<<<<<<<<<<<<<<<<')
        return make_response(jsonify(**data), 200)
    except:
#traceback.print_exc()
        # conn.rollback()
        error = {
            "code": 2222,
            "type": "ServerError",
            "message": "Server is temporary unavailable."
        }
        return make_response(jsonify(error=error), 500)

if __name__ == '__main__':
    # app.run()
    # http = WSGIServer(('0.0.0.0', 5000), app)
    # http.serve_forever()

    cert = './cert_key/pfx.mycattool_com.crt'
    key = './cert_key/pfx.mycattool_com.key'
    https = WSGIServer(('0.0.0.0', 5001), app, keyfile=key, certfile=cert)
    https.serve_forever()
