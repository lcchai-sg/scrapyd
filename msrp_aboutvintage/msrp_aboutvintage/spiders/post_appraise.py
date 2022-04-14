from requests import post

query = """mutation ($input: PriceReferenceInput){
    capturePriceReference(input: $input) {id}
}"""


def post_appraise(self):
    count = 0
    for res in self.result:
        price = round(res.get('amount') /
                      (1 + self.tax_rate / 100), self.precision)
        tax = round(res.get('amount') - price, self.precision)
        reference = res.get('reference')
        amount = res.get('amount')
        data = {
            "sourceId": self.sourceId,
            "type": self.type,
            "market": self.market,
            "brandId": self.brand_id,
            "reference": res.get('reference'),
            "currencyId": self.currency_id,
            "price": price,
            "tax": tax,
            "amount": res.get('amount')
        }
        count += 1
        variables = {'input': data}
        resp = post(self.api, json={"query": query, "variables": variables, "operation": "Capture MSRP", },
                    headers={"Content-Type": "application/json"})
        if resp is not None:
            res = resp.json()
            id = res["data"]["capturePriceReference"]["id"]
            print(f'POSTED #{count} R: {reference} A: {amount} with ID: {id}')
