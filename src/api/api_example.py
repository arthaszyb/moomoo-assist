from moomoo import OpenQuoteContext, OpenSecTradeContext, TrdSide, TrdEnv, TrdMarket, SecurityFirm, RET_OK, Currency

HOST = '127.0.0.1'
PORT = 11111

def main():
    with OpenQuoteContext(host=HOST, port=PORT) as quote_ctx:
        snapshot = quote_ctx.get_market_snapshot('HK.00700')
        print(snapshot)

    with OpenSecTradeContext(host=HOST, port=PORT) as trd_ctx:
        order = trd_ctx.place_order(
            price=100.0,
            qty=100,
            code="HK.00700",
            trd_side=TrdSide.BUY,
            trd_env=TrdEnv.SIMULATE
        )
        print(order)

    with OpenSecTradeContext(
        filter_trdmarket=TrdMarket.US,
        host=HOST,
        port=PORT,
        security_firm=SecurityFirm.FUTUSG
    ) as trd_ctx:
        ret, data = trd_ctx.accinfo_query(currency=Currency.USD)
        if ret == RET_OK:
            print(data)
            print(data['power'][0])  # 取第一行的购买力
            print(data['power'].values.tolist())  # 转为 list
        else:
            print('accinfo_query error:', data)

if __name__ == "__main__":
    main()
