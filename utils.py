import json
import datetime
from settings import GROUP_TYPE


def convert_to_data(inp_str: str):
    try:
        data = json.loads(inp_str)
        if isinstance(data, str):  # Для ситуации "'кавычки'"
            return "== Неверный формат JSON =="
    except json.decoder.JSONDecodeError:
        return "== Неверный формат JSON =="
    try:
        dt_from = datetime.datetime.fromisoformat(data['dt_from'])
        dt_upto = datetime.datetime.fromisoformat(data['dt_upto'])
        if dt_from > dt_upto:
            return "== Начальная дата больше конечной =="
        data.update({'dt_from': dt_from, 'dt_upto': dt_upto})
        if not data['group_type'] in GROUP_TYPE:
            return "== Неверный тип группировки =="
    except ValueError:
        return "== Неверный формат Даты =="
    except KeyError:
        return "== Неверные ключи =="
    return data


if __name__ == '__main__':
    pass

# # ========== For Test without telegram =====================
#     input_str_month = '{"dt_from": "2022-09-01T00:00:00",' \
#                       ' "dt_upto": "2022-12-31T23:59:00",' \
#                       ' "group_type": "month"}'
#
#     input_str_day = '{"dt_from": "2022-10-01T00:00:00",' \
#                     ' "dt_upto": "2022-11-30T23:59:00",' \
#                     ' "group_type": "day"}'
#
#     input_str_hour = '{"dt_from": "2022-02-01T00:00:00",' \
#                      ' "dt_upto": "2022-02-02T00:00:00",' \
#                      ' "group_type": "hour"}'
#
#     # input_str = input_str_month
#     # input_str = input_str_day
#     input_str = input_str_hour
#
#     input_data = convert_to_data(input_str)
#
#     if isinstance(input_data, str):
#         print(f"** Result: {input_data}\n** Неверные данные, Выходим!")
#         sys.exit()
#
#     res = get_aggregate_data(input_data)
#     print(f"** Result: {res}")
#     print(f"** Result Len: {len(res['labels'])}, {len(res['dataset'])}")
#
# # ========== End For Test without telegram =====================

