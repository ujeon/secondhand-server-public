from .models import Raw_data


def input_crawl_data(data):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    # REVIEW: 번개장터 데이터 크롤링
    # bungae_crawler = Bungae_crawler("유모차")
    # bungae_data = bungae_crawler.data_maker(300)

    # REVIEW: 헬로마켓 데이터 크롤링
    # hello_data = hello_crawler(10)

    # REVIEW: 당근마켓 데이터 크롤링
    # daangn_data = daangn_crawler(100)

    # REVIEW: 모든 데이터를 리스트에 저장합니다.
    # all_data = [*hello_data]
    # *bungae_data, *daangn_data
    new_data = Raw_data(
        title=data["title"],
        content=data["content"],
        price=data["price"],
        url=data["url"],
        img_url=data["img_url"],
        market=data["market"],
        posted_at=data["posted_at"],
        is_sold=data["is_sold"],
        category_id=data["category_id"],
        location=data["location"],
    )
    new_data.save()
    return
