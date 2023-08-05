import logging


LOG = logging.getLogger(__name__)


def check_load_on_cluster(cases: list[str]) -> list[str]:
    """
    Adjust the number of cases to start based
    on computational resources available
    """
    cases_to_start = cases[0]
    return [cases_to_start]


def start_jobs(cases: list[str]) -> None:
    """
    Start an analysis for the given cases
    """
    cases_to_start = check_load_on_cluster(cases=cases)
    for case in cases_to_start:
        LOG.info("Starting analysis for %s" % case)


def get_cases_that_need_new_analysis(monitored_cases: list[str]) -> list[str]:
    """
    Find cases that qualify for a new
    analysis among the monitored cases
    """
    return ["justhusky"]


def get_monitored_cases() -> list[str]:
    """
    Return a list of cases that are monitored
    """
    return ["justhusky", "coollamb"]


def run_workflow() -> None:
    """
    Run all the steps needed for perpetual
    genomic monitoring:
    - Find all monitored cases
    - Identify monitored cases that need new analysis
    - Start the analyses
    """
    LOG.info("Requesting cases marked for monitoring in scout")
    monitored_cases: list[str] = get_monitored_cases()

    LOG.info("Identifying cases which need a new analysis")
    cases_that_need_new_analysis: list[str] = get_cases_that_need_new_analysis(
        monitored_cases=monitored_cases
    )

    LOG.info("Starting analyses")
    start_jobs(cases=cases_that_need_new_analysis)
