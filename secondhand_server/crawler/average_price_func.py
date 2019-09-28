def average_price_func(listed_query_set):
    try:
        first = listed_query_set.values().first()
        average_price_dict = {
            "brand": first["brand"],
            "model": first["model"],
            "date": first["posted_at"]
        }
        price_sum = 0
        post_count = 0
        highest_price = first["price"]
        lowest_price = first["price"]

        for each_query_set in listed_query_set.values():
            price_sum += each_query_set["price"]
            post_count += 1
            if highest_price < each_query_set["price"]:
                highest_price = each_query_set["price"]
            if lowest_price > each_query_set["price"]:
                lowest_price = each_query_set["price"]

        average_price_dict["average_price"] = int(price_sum / post_count)
        average_price_dict["lowest_price"] = lowest_price
        average_price_dict["highest_price"] = highest_price
        average_price_dict["quantity"] = post_count

        return average_price_dict

    except Exception as err:
        print(err)
        return
