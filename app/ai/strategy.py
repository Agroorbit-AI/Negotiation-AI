class NegotiationStrategy:

    def decide_price(self, product, customer, history, offer_price):
        base = product.base_price
        floor = product.floor_price

        last_price = history.get("last_price", base)
        target = max(last_price + 10, floor)

        if offer_price is None:
            return "ask", target

        if offer_price >= target:
            return "accept", offer_price

        if offer_price >= floor:
            counter = (offer_price + target) / 2
            return "counter", round(counter, 2)

        return "reject", None
