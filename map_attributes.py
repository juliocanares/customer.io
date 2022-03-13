def map_attributes(pair, customer):
    if pair['from'] in customer:
        customer[pair['to']] = customer[pair['from']]
        customer.pop(pair['from'], None)
