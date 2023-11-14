# from fastapi import Depends, Query, Response
# from openpyxl import Workbook
# from openpyxl.utils.dataframe import dataframe_to_rows
# import pandas as pd
#
# # Отримайте дані з бази даних і сформуйте monitoring_data_out, як робили раніше
#
# # Створіть Excel-файл та додайте дані
# workbook = Workbook()
# worksheet = workbook.active
# data = [list(monitoring_data.values()) for monitoring_data in monitoring_data_out]
# for row in data:
#     worksheet.append(row)
#
# # Збережіть Excel-файл у буфері пам'яті
# buffer = io.BytesIO()
# workbook.save(buffer)
# buffer.seek(0)
#
# # Відправте Excel-файл як відповідь
# response = Response(content=buffer.read(),
#                     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
# response.headers["Content-Disposition"] = "attachment; filename=monitoring_report.xlsx"
#
# return response