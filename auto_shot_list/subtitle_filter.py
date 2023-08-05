import ass
from itertools import chain
from datetime import timedelta
from pydantic import BaseModel
from typing import List
from pathlib import Path
from enum import Enum

import json_tricks


class HowEnum(str, Enum):
    first = "first"
    last = "last"


class Event(BaseModel):
    text: str
    how: HowEnum
    event_time: timedelta = None

    def evaluate(self, event):
        if self.text not in event.text:
            return
        if self.how == "first" and not self.event_time:
            self.event_time = event.start
        elif self.how == "last":
            self.event_time = event.end


class SkipSection(BaseModel):
    name: str
    events: List[Event or None]

    def is_within(self, shot_time: timedelta):
        if len(self.events) > 2:
            raise ValueError("Too much events")

        if self.events[0]:
            time_start = self.events[0]
        else:
            time_start = shot_time - timedelta(seconds=0)

        if self.events[1]:
            time_stop = self.events[1]
        else:
            time_stop = shot_time + timedelta(seconds=0)

        return time_start <= shot_time <= time_stop


class SubtitleFilter:

    def __init__(self, filter_rules_path: Path, subtitles_path: Path):
        self.filter_rules_path = filter_rules_path
        self.subtitles_path = subtitles_path

        if not self.subtitles_path.exists():
            raise ValueError(f"Invalid subtitle path {self.subtitles_path}")
        if not self.filter_rules_path.exists():
            raise ValueError(f"Invalid filter rules path {self.filter_rules_path}")

        with open(self.filter_rules_path, "r") as f:
            data = json_tricks.load(f)
        self.filter_rules = [SkipSection(**item) for item in data]

        with open(self.subtitles_path, encoding='utf_8_sig') as f:
            self.subtitles = ass.parse(f)

        search_events = list(chain(*[x.events for x in self.filter_rules]))
        self._evaluate_search_events(search_events)

    def _evaluate_search_events(self, search_events):
        """
        Evaluates all events on subtitles path
        :param search_events:
        :return:
        """
        for event in self.subtitles.sections["Events"]:
            for se in search_events:
                se.evaluate(event)

    def is_within_any(self, shot_time: timedelta) -> bool:
        """
        Validated that given time is within any given sections
        :param shot_time:
        :return:
        """
        out = [filter_rule.is_within(shot_time) for filter_rule in self.filter_rules]
        return any(out)
