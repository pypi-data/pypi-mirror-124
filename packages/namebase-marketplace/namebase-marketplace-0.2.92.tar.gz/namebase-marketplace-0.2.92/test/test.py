from namebase_marketplace import marketplace

def should_accept_offer(offerAmount, threshold):
    return float(offerAmount) >= threshold

def get_best_offer(bestBidId, domain_history):
    negotiations = domain_history['negotiations']
    for negotiation in negotiations:
        history = negotiation['history']
        for hist in history['bids']:
            amount = hist['amount']
            id = hist['bidId']
            isAccepted = hist['isAccepted']
            if id == bestBidId and not isAccepted:
                return {"id" : id, "amount" : float(amount)}

    return {}

if __name__ == '__main__':
    cookie= 's%3AHDlsLuQDU8ndHj3MdLefqJyfn9DEQuKH.xgQGDcEUB0i9HG8a8q1%2BO55zAy7AW7zwM7WTNzMJmlg'
    m = marketplace.Marketplace(namebase_cookie=cookie)
    domain = 'naodanga'
    rem = m.cancel_listing(domain=domain)
    print(rem)
    #v = m.list_domain(domain=domain,amount=2000, description='test')
