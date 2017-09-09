import os
from seminar import settings
from endurance.core.io.files import SavedCaseFile
from endurance.core.modeling.all import FixedShunt
from endurance.core.modeling.case import Case
from endurance.core.simulation.power_flow import NewtonRaphson

seed_case = SavedCaseFile(settings.QUICKSTART_CASE)


def create():
    """
    Creates each of the fixed shunt outage scenarios and saves them to the disk, returning
    an array of scenario files for convenience.
    :return: An array of scenario files.
    :rtype: List[SavedCaseFile]
    """
    keys = _get_fixed_shunt_keys()
    scenarios = []
    for bus_number, identifier in keys:
        scenario = _create_fixed_shunt_outage_scenario(bus_number, identifier)
        scenarios.append(scenario)
    return scenarios


def get():
    """
    Gets an array of SavedCaseFile objects that represent each of the scenario files. Does not
    create the files or overwrite the files.
    :return: An array of scenario files.
    :rtype: List[SavedCaseFile]
    """
    keys = _get_fixed_shunt_keys()
    scenarios = []
    for bus_number, identifier in keys:
        scenario_file_name = 'scenario_{0}_{1}.sav'.format(bus_number, identifier.strip(' '))  # create a unique file name
        scenario = SavedCaseFile(os.path.join(settings.CASE_DIR, scenario_file_name))
        scenarios.append(scenario)
    return scenarios


def _create_fixed_shunt_outage_scenario(bus_number, identifier):
    """
    Creates a single saved case scenario where the specified fixed shunt is out of service.
    Saves to the disk and returns a saved case file object.
    :param bus_number: The bus number of the fixed shunt
    :type bus_number: int
    :param identifier: The 2 character id of the fixed shunt
    :type identifier: str
    :return: The scenario as a SavedCaseFile
    :rtype: :class:`SavedCaseFile'
    """
    seed_case.read()  # import the seed case

    fixed_shunt = FixedShunt(bus_number, identifier)  # sync the specified fixed shunt
    fixed_shunt.status = 0  # remove the fixed shunt from service

    powerflow = NewtonRaphson()  # get a power flow solver
    powerflow.run()  # run the power flow to create the scenario solution

    scenario_file_name = 'scenario_{0}_{1}.sav'.format(bus_number, identifier.strip(' '))  # create a unique file name
    scenario = SavedCaseFile(os.path.join(settings.CASE_DIR, scenario_file_name))  # create a saved case
    scenario.write()  # write it to disk
    return scenario


def _get_fixed_shunt_keys():
    seed_case.read()
    case = Case(autoinit=True)
    keys = []
    for fixed_shunt in case.fixed_shunts:
        keys.append(fixed_shunt.key)
    return keys

