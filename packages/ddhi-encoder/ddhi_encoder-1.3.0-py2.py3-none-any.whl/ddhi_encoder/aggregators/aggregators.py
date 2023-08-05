# -*- coding: utf-8 -*-
# aggregators.py
from ddhi_encoder.entities.entities import Place


class Aggregator:
    def __init__(self):
        self.interviews = []
        self.places = []

    def include(self, interview):
        self.interviews.append(interview)
        places = interview.places()
        [self.places.append(Place(place)) for place in places]
