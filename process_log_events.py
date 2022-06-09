def create_processing_pipeline(start_generator, filters):
    generator = start_generator
    for filter in filters:
        generator = filter(generator)
    return generator


filters = [
    # file_filter,
    # dict_filter,
    # serie_a_filter,
    # log_filter,
    # sum_filter
]

pipeline = create_processing_pipeline(
    ['./crunchbase_funding.csv'], filters)
