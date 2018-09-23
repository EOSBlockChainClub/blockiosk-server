# bizEOS-server
EOS Hackathon London, EOSwag


## EOSIO

Q. 블록체인에 무엇을 담을 것인가?

누가, 언제, 어느 브랜드에서 체크인을 하였다.



- struct: actions
- function: takeaction(액션 기록하기), getaction(액션 불러오기)






## API

### /order

주문 결과를 저장하는 API

#### request

POST

- order_id: 매장에서 제공하는 주문 번호. (옵션, 없어도 됨)
- orderlist: 배열. 아래 예시 참고. 필수!
```
orderlist = [
    {
        'product_id': 1,
        'quantity': 1,
        'memo': '소금빼고주세요'
    },
    {
        'product_id': 2,
        'quantity': 2,
        'memo': None
    }
]
```

#### response

```
{
    "id": 4
}
```




### /checkin

사용자가 매장에서 체크인했을 때 데이터를 출력해주는 API

#### request

POST

- user: 사용자 이름, 이메일.. 응 안써~ (옵션)
- store: 브랜드 이름 ([starbucks](https://www.starbucks.co.uk/menu), [mcdonalds](https://www.mcdonalds.com/us/en-us/full-menu.html), [domino](https://www.dominos.co.uk/menu?start=true) -클릭시 메뉴 사이트로 이동)
- spot: 지점명 (옵션)
- memo: (옵션)


#### response

- last: 최근 주문내역
- brand_frequency: 브랜드별 빈도순 상위 세가지 메뉴
- category_frequency: 브랜드가 해당하는 카테고리별 빈도순 상위 세가지 메뉴

```
{
    "brand_frequency": [
        {
            "memo": null,
            "product_id": 2,
            "product_name": "Coca-Cola(Large)",
            "quantity": 1
        },
        {
            "memo": null,
            "product_id": 11,
            "product_name": "Big Mac",
            "quantity": 1
        },
        {
            "memo": null,
            "product_id": 12,
            "product_name": "4 piece Chicken McNuggets",
            "quantity": 1
        }
    ],
    "category_frequency": [
        {
            "memo": null,
            "product_id": 1,
            "product_name": "Chips",
            "quantity": 1
        },
        {
            "memo": null,
            "product_id": 2,
            "product_name": "Coca-Cola(Large)",
            "quantity": 1
        },
        {
            "memo": null,
            "product_id": 3,
            "product_name": "Vanilla Cone",
            "quantity": 1
        }
    ],
    "last": [
        {
            "memo": null,
            "product_id": 11,
            "product_name": "Big Mac",
            "quantity": 1
        },
        {
            "memo": null,
            "product_id": 2,
            "product_name": "Coca-Cola(Large)",
            "quantity": 1
        }
    ]
}
```
