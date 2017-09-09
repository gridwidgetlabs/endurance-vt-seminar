from seminar import settings
import os


def create(results):
    """
    Creates the reports for each of the scenario results
    :param results: A dictionary of the scenario results
    :type results: dict{scenario: [SubsystemDataSeries]}
    """
    for scenario, subsystem_data_series in results.items():
        subsystem_data_series.merge(['per_unit_voltage_magnitudes'])
        file_name = '{0}.csv'.format(scenario.file_name.split('\\')[-1].split('.')[0])
        subsystem_data_series.write(os.path.join(settings.DATA_DIR, file_name))
