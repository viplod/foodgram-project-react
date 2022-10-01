def get_text_on_print(dict_elements):
    text = []
    for elem in dict_elements:
        text.append(f'{elem["ingredient__name"].capitalize()} '
                    f'({elem["ingredient__measurement_unit"]}) '
                    f'- {elem["sum_amount"]} \n')
    return text
