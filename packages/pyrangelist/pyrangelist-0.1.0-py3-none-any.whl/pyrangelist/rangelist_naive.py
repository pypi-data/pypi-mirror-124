from typing import List

from pyrangelist.range import Range


class RangeListNaive:
    def __init__(self):
        self.ranges = []

    def add(self, range_list:List[int])->None:
        target_range = Range(range_list[0], range_list[1])

        if not target_range.is_empty():
            new_ranges = []
            for rang in self.ranges:
                if rang.is_touching(target_range):
                    target_range.low = min(
                        target_range.low,
                        rang.low
                    )
                    target_range.high = max(
                        target_range.high,
                        rang.high
                    )
                else:
                    new_ranges.append(rang)

            new_ranges.append(target_range)
            self.ranges = new_ranges

    def remove(self, range_list:List[int])->None:
        target_range = Range(range_list[0], range_list[1])

        if not target_range.is_empty():
            new_ranges = []

            for rang in self.ranges:
                if rang.intersection(target_range).is_empty():
                    new_ranges.append(rang)
                else:
                    low_leftover = Range(
                        low=rang.low,
                        high=target_range.low,
                        check_format=False
                    )
                    high_leftover = Range(
                        low=target_range.high,
                        high=rang.high,
                        check_format=False
                    )
                    if not low_leftover.is_empty():
                        new_ranges.append(low_leftover)
                    if not high_leftover.is_empty():
                        new_ranges.append(high_leftover)

            self.ranges = new_ranges


    def print(self)->None:
        intervals_sorted = sorted(self.ranges, key=lambda x: x.low)
        range_strings = []
        for rang in intervals_sorted:
            range_strings.append(str(rang))
        print(" ".join(range_strings))
