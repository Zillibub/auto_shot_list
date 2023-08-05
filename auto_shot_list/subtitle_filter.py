import ass
from itertools import chain
from datetime import timedelta
from pydantic import BaseModel
from typing import List, Union
from pathlib import Path
from enum import Enum

import json


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
    events: List[Union[Event,None]]
    offset: int = 0

    def is_within(self, shot_time: timedelta):
        if len(self.events) > 2:
            raise ValueError("Too much events")

        if self.events[0] and self.events[0].event_time:
            time_start = self.events[0].event_time
        else:
            time_start = shot_time + timedelta(seconds=1)

        if self.events[1] and self.events[1].event_time:
            time_stop = self.events[1].event_time
        else:
            time_stop = shot_time - timedelta(seconds=1)

        return time_start - timedelta(seconds=self.offset) <= shot_time <= time_stop + timedelta(seconds=self.offset)


class SubtitleFilter:

    def __init__(self, filter_rules_path: Path, subtitles_path: Path):
        self.filter_rules_path = filter_rules_path
        self.subtitles_path = subtitles_path

        if not self.subtitles_path.exists():
            raise ValueError(f"Invalid subtitle path {self.subtitles_path}")
        if not self.filter_rules_path.exists():
            raise ValueError(f"Invalid filter rules path {self.filter_rules_path}")

        with open(self.filter_rules_path, "r", encoding='utf-8') as f:
            data = json.load(f)
        self.filter_rules = [SkipSection(**item) for item in data]

        with open(self.subtitles_path, encoding='utf_8_sig') as f:
            self.subtitles = ass.parse(f)

        search_events = [event for event in chain(*[x.events for x in self.filter_rules]) if event]
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

    def is_within_any(self, scene_start: timedelta, scene_end: timedelta) -> bool:
        """
        Validated that given time is within any given sections
        :param scene_start:
        :param scene_end:
        :return:
        """
        out = [filter_rule.is_within(scene_start) for filter_rule in self.filter_rules] + [
            filter_rule.is_within(scene_end) for filter_rule in self.filter_rules
        ]
        return any(out)
