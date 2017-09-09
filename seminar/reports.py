from seminar import settings
from seminar.scenarios import seed_case
import os
from endurance.core.modeling.bus import Bus


def create(results):
    # for scenario, data in results.items():
    for scenario, subsystem_data_series in results.items():
        # report = scenario, _merge_into_time_series(data)
        # _write(report)
        subsystem_data_series.merge(['per_unit_voltage_magnitudes'])
        file_name = '{0}.csv'.format(scenario.file_name.split('\\')[-1].split('.')[0])
        subsystem_data_series.write(os.path.join(settings.DATA_DIR, file_name))

# def _merge_into_time_series(collection):
#     seed_case.read()
#     time_series = {}  # {record_parameter: [(iteration, value)]}
#     for iteration, bus_data in collection.items():
#         bus_numbers = bus_data.numbers
#         per_unit_voltage_magnitudes = bus_data.per_unit_voltage_magnitudes
#         for number, per_unit_voltage_magnitude in zip(bus_numbers, per_unit_voltage_magnitudes):
#             key = Bus(number).name
#             point = iteration, per_unit_voltage_magnitude
#             if key not in time_series.keys():
#                 time_series[key] = []
#             time_series[key].append(point)
#     return time_series
#
#
# def _convert(time_series_collection):
#     new_time_series = {}
#     for record_parameter, time_series in time_series_collection.items():
#         for iteration, value in time_series:
#             if iteration not in new_time_series.keys():
#                 new_time_series[iteration] = {}
#             if record_parameter not in new_time_series[iteration].keys():
#                 new_time_series[iteration][record_parameter] = value
#     return new_time_series
#
#
# def _write(report):
#     scenario, time_series = report
#     new_time_series = _convert(time_series)
#     file_name = '{0}.csv'.format(scenario.file_name.split('\\')[-1].split('.')[0])
#     columns = ["Iteration"] + time_series.keys()
#     column_headers = ""
#     data = ""
#     for column in columns:
#         column_headers += '{0},'.format(column)
#     column_headers = "{0}\n".format(column_headers[:-1])
#     for iteration in new_time_series.keys():
#         line = '{0},'.format(iteration)
#         for parameter in time_series.keys():
#             value = new_time_series[iteration][parameter]
#             line += '{0},'.format(value)
#         line += '{0}\n'.format(line[-1])
#         data += line
#     with (open(os.path.join(settings.DATA_DIR, file_name), mode='w')) as csv_file:
#         csv_file.write(column_headers + data)


