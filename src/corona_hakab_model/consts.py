from typing import NamedTuple


class Consts(NamedTuple):
    # corona stats
    # todo replace with distribution
    # average state mechine transmitions times:
    average_latent_to_silent_days = 2
    average_silent_to_asymptomatic_days = 3
    average_silent_to_symptomatic_days = 3
    average_asymptomatic_to_recovered_days = 5
    average_symptomatic_to_asymptomatic_days = 10
    average_symptomatic_to_hospitalized_days = 2  # todo should be 1.5, but untill we roll this number, using a rounded up number
    average_hospitalized_to_asymptomatic_days = 18
    average_hospitalized_to_icu_days = 5
    average_icu_to_dead_days = 7
    average_icu_to_hospitalized_days = 7  # todo state mechine didnt state this time

    def average_infecting_days(self):
        """
        returns the expected time of infectivness of an infected people (for normalization)
        assuming you are not contagious when in a hospital nor in icu.
        also ignoring moving back from icu to asymptomatic
        """
        silent_time = self.silent_to_asymptomatic_probability * self.average_silent_to_asymptomatic_days + self.silent_to_symptomatic_probability * self.average_silent_to_symptomatic_days
        asymptomatic_time = self.average_asymptomatic_to_recovered_days * self.silent_to_asymptomatic_probability
        symptomatic_time = self.silent_to_symptomatic_probability * \
                           ((
                                        self.average_symptomatic_to_asymptomatic_days + asymptomatic_time) * self.symptomatic_to_asymptomatic_probability + \
                            self.average_symptomatic_to_hospitalized_days * self.symptomatic_to_hospitalized_probability)
        hosplital_time = self.silent_to_symptomatic_probability * self.symptomatic_to_hospitalized_probability * self.hospitalized_to_asymptomatic_probability * asymptomatic_time
        return silent_time + asymptomatic_time + symptomatic_time + hosplital_time

    # average probability for transmitions:
    silent_to_asymptomatic_probability = 0.2
    silent_to_symptomatic_probability = 0.8
    symptomatic_to_asymptomatic_probability = 0.85
    symptomatic_to_hospitalized_probability = 0.15
    hospitalized_to_asymptomatic_probability = 0.8
    hospitalized_to_icu_probability = 0.2
    icu_to_hospitalized_probability = 0.65
    icu_to_dead_probability = 0.35

    # probability of an infected symptomatic agent infecting others
    Symptomatic_infection_ratio: float = 0.75
    # probability of an infected asymptomatic agent infecting others
    ASymptomatic_infection_ratio: float = 0.25
    # probability of an infected silent agent infecting others
    Silent_infection_ratio: float = 0.3  # todo i made this up, need to get the real number
    # base r0 of the disease
    r0: float = 2.4

    def expected_infection_ratio(self):
        """
        The expected infection ratio of a random infected agent
        """
        asymptomatic_time = self.average_asymptomatic_to_recovered_days * self.silent_to_asymptomatic_probability
        symptomatic_time = self.silent_to_symptomatic_probability * \
                           (
                                       self.average_symptomatic_to_asymptomatic_days * self.symptomatic_to_asymptomatic_probability + \
                                       self.average_symptomatic_to_hospitalized_days * self.symptomatic_to_hospitalized_probability)
        silent_time = self.silent_to_symptomatic_probability * self.average_silent_to_symptomatic_days + self.silent_to_asymptomatic_probability * self.average_silent_to_asymptomatic_days
        total_time = asymptomatic_time + symptomatic_time + silent_time
        return (self.ASymptomatic_infection_ratio * asymptomatic_time \
                + self.Symptomatic_infection_ratio * symptomatic_time + self.Silent_infection_ratio * silent_time) / total_time

    # simulation parameters
    population_size = 10_000
    total_steps = 400
    initial_infected_count = 20

    # quarantine policy
    # todo why does this exist? doesn't the policy set this? at least make this an enum
    # note not to set both home quarantine and full quarantine true
    # whether to quarantine detected agents to their homes (allow familial contact)
    home_quarantine_sicks = False
    # whether to quarantine detected agents fully (no contact)
    full_quarantine_sicks = False
    # how many of the infected agents are actually caught and quarantined
    caught_sicks_ratio = 0.3

    # policy stats
    # todo this reeeeally shouldn't be hard-coded
    # defines whether or not to apply a quarantine (work shut-down)
    active_quarantine = False
    # the date to stop work at
    stop_work_days = 30
    # the date to resume work at
    resume_work_days = 60

    # social stats
    # the average family size
    average_family_size = 5  # todo replace with distribution
    # the average workplace size
    average_work_size = 50  # todo replace with distribution
    # the average amount of stranger contacts per person
    average_amount_of_strangers = 200  # todo replace with distribution

    # relative strangths of each connection (in terms of infection chance)
    # todo so if all these strength are relative only to each other (and nothing else), whe are none of them 1?
    family_strength_not_workers = 0.75
    family_strength = 0.4
    work_strength = 0.04
    stranger_strength = 0.004
