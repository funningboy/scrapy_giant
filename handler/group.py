# -*- coding: utf-8 -*-

# group by main stream
tradergroup = [
    # ref: http://tim1891.pixnet.net/blog/post/273284627-%E6%B4%9E%E6%82%89%E4%B8%BB%E5%8A%9B~~~~%E8%B2%B7%E8%B3%A3%E6%97%A5%E5%A0%B1%E8%A1%A8%E6%9F%A5%E8%A9%A2%E7%B3%BB%E7%B5%B1
    {
        'groupnm': u'林滄海,海哥的主力券商',
        'groupids': ['9658', '9216', '9255', '1260', '585b'],
        'description': u'(9658)富邦-建國, (9216)凱基-信義, (9255)凱基-和平, (1260)宏遠, (585b)統一-內湖'
    },
    {
        'groupnm': u'KTV金主轉型主力券商',
        'groupids': ['700S', '9A00', '922H', '8450' '6911', '5852'],
        'description': u'(700S)兆豐-大同, (9A00)永豐金, (922H)凱基-復興, (8450)康和, (6911)德信-台北 (5852)統一-敦南'
    },
    {
        'groupnm': u'塑化大家族主力券商',
        'groupids': ['9216', '779u', '526B', '9676'],
        'description': u'(9216)凱基-台北, (779u)國票-長程, (525B)大慶-復興. (9676)富邦-仁愛'
    },
    {
        'groupnm': u'虎尾幫',
        'groupids': ['9697', '6386', '700F', '592N', '9A9b'],
        'description': u'(9697)富邦-虎尾,（6386)光合-虎尾, (700F)兆豐-虎尾, (592N)元富-虎尾, (9A9b)永豐-虎尾'
    }
    # update tradergroup after runing some alg
    # ex: 'groupnm': 'bestbuy-5' means which trader has the best portfolio in the past 5 days  
]

stockgroup = [
    #http://www.twse.com.tw/ch/trading/indices/twco/tai50i.php
    {
        'groupnm': u'臺灣50指數成分股票',
        'groupids': ['3474', '4938'],
        'description': u'台灣50指數成分股票'
    }
    # update tradergroup after runing some alg
    # ex: 'groupnm': 'bestbuy-5' means which stock has the best portfolio in the past 5 days
]
