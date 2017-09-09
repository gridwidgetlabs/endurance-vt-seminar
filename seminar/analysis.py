from endurance.core.modeling.case import Case
from endurance.core.subsystems.data.all import BusData, MachineData
from endurance.core.simulation.power_flow import NewtonRaphson
from endurance.core.modeling.macros.scaling import *
from endurance.core.simulation.solution_parameters import NewtonRaphsonSolutionParameters
from endurance.core.subsystems.base import SubsystemDataSeries


dispatch_mw_tolerance = 5.0
max_dispatch_iterations = 5


def run(scenario, percent_increment, iteration_limit):
    """
    Runs the demonstration analysis for a given scenario.
    :param scenario: The saved case file for the scenario of interest.
    :type scenario: SavedCaseFile
    :param percent_increment: The percentage of the original load to increment on each iteration.
    :type percent_increment: float
    :param iteration_limit: The total number of iterations for the analysis run. i.e. how many times to scale the load
    and run the power flow.
    :type iteration_limit: int
    :return: The results from the study
    :rtype: SubsystemDataSeries
    """
    scenario.read()
    case = Case(autoinit=True)
    original_loads = _cache_original_loads(case)

    # results = {}
    results = SubsystemDataSeries()
    _set_solution_parameters()
    powerflow = NewtonRaphson()

    for iteration in range(1, iteration_limit + 1):
        pre_scale_total_mw_load = _calculate_total_load(case)
        scaling_factor = (percent_increment / 100) * iteration
        _scale_loads(case, original_loads, scaling_factor)
        post_scale_total_mw_load = _calculate_total_load(case)
        mw_to_dispatch = post_scale_total_mw_load - pre_scale_total_mw_load
        _redispatch(case, mw_to_dispatch)
        powerflow.run()
        # results[iteration] = _cache_bus_data()
        results.sets.append(_cache_bus_data())
    return results


def _set_solution_parameters():
    solution_parameters = NewtonRaphsonSolutionParameters()
    solution_parameters.max_iterations = 50
    solution_parameters.mismatch_convergence_tolerance = 3.0
    solution_parameters.voltage_controlled_bus_reactive_power_mismatch_tolerance = 1.0


def _cache_bus_data():
    data = BusData()
    data.read_all()
    data.block_read = True
    return data


def _scale_loads(case, original_loads, scaling_factor):
    for load in case.loads:
        base_mw = original_loads[load.key]['MW']
        base_mvar = original_loads[load.key]['MVAR']
        load.nominal_constant_P_mw = base_mw * (1 + scaling_factor)
        load.nominal_constant_P_mvar = base_mvar * (1 + scaling_factor)


def _calculate_total_load(case):
    total_load_mw = 0
    for load in case.loads:
        if load.status:
            total_load_mw += load.nominal_constant_P_mw
    return total_load_mw


def _redispatch(case, mw_to_dispatch):
    remaining_mw_to_dispatch = mw_to_dispatch
    total_dispatchable_mw_max = _calculate_total_dispatchable_mw(case)
    already_dispatched_mw = 0
    iteration_number = 0
    swing = case.swing
    while (abs(remaining_mw_to_dispatch) > dispatch_mw_tolerance) and (iteration_number <= max_dispatch_iterations):
        for machine in case.machines:
            if machine.status and machine.has_capacity:
                if machine.bus_number != swing.number:
                    delta_p = (remaining_mw_to_dispatch * machine.max_mw_output) / total_dispatchable_mw_max
                    if machine.mw_loading + delta_p < machine.max_mw_output:
                        machine.mw_loading += delta_p
                    else:
                        delta_p = machine.max_mw_output - machine.mw_loading
                        machine.mw_loading = machine.max_mw_output
                    already_dispatched_mw += delta_p
        iteration_number += 1
        remaining_mw_to_dispatch -= already_dispatched_mw


def _calculate_total_dispatchable_mw(case):
    total_dispatchable_mw_max = 0
    swing = case.swing
    for machine in case.machines:
        if machine.status and machine.has_capacity:
            if machine.bus_number != swing.number:
                total_dispatchable_mw_max += machine.max_mw_output
    return total_dispatchable_mw_max


def _cache_original_loads(case):
    original_loads = {}
    for load in case.loads:
        original_loads[load.key] = {'MW': load.constant_P_mw,
                                    'MVAR': load.constant_P_mvar}
    return original_loads
