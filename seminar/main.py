import seminar

# point endurance to the appropriate project settings
seminar.setup()

# imports
from endurance import quickstart, stop

# main entry point for the seminar project
def run():

    # use endurance's quickstart feature to initialize PSSE and load a base case
    quickstart()

    from seminar import scenarios
    from seminar import analysis
    from seminar import reports

    scenario_files = scenarios.create()

    results = {}
    percent_increment = 1.0
    iteration_limit = 50

    scenario_files = [scenarios.seed_case] + scenario_files
    for scenario in scenario_files:
        results[scenario] = analysis.run(scenario, percent_increment, iteration_limit)

    reports.create(results)

    # stop PSSE from running (helpful for hourly licenses)
    return results