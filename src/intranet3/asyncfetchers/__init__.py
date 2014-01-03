from .bugzilla import BugzillaFetcher
from .rockzilla import RockzillaFetcher
from .pivotaltracker import PivotalTrackerFetcher
from .unfuddle import UnfuddleFetcher

from .base import FetchException, FetcherTimeout, FetcherBaseException

FETCHERS = {
   'bugzilla': BugzillaFetcher,
   'rockzilla': RockzillaFetcher,
   'pivotaltracker': PivotalTrackerFetcher,
   'unfuddle': UnfuddleFetcher,
}

def get_fetcher(tracker, credentials, user, login_mapping):
    type = tracker.type
    fetcher_class = FETCHERS[type]
    return fetcher_class(tracker, credentials, user, login_mapping)
