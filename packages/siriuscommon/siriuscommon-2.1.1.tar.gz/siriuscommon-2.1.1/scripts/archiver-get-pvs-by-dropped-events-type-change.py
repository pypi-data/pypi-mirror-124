#!/usr/bin/env python
import argparse

from siriuscommon.archiver import getPVsByDroppedEventsTypeChange

if __name__ == "__main__":
    parser = argparse.ArgumentParser("getPVsByDroppedEventsTypeChange Request")
    args = parser.parse_args()

    for pv in getPVsByDroppedEventsTypeChange():
        print(pv.pv_name, pv.events_dropped)
