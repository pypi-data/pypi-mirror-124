from typing import Any, List
from intervaltree import IntervalTree

from pyrangelist.range import Range
from pyrangelist.log import LOGGER as rangelist_logger


class RangeList:
    def __init__(self):
        # Using existing package for interval tree implementation
        # itervaltree package stores sets of *overlapping* ranges,
        # and the performance will be suboptimal.
        # But it's good to push out a working prototype.
        self.tree = IntervalTree()

    @staticmethod
    def check_listrange_argument(arg:Any, argname:str, func:str)->None:
        if not isinstance(arg, list):
            raise TypeError(
                f"'{func}' argument '{argname}' must be of type 'list'. "
                f"Received: '{arg}' of type '{type(arg)}'"
            )
        if len(arg) != 2:
            raise ValueError(
                f"'{func}' argument '{argname}' must be of length 2. "
                f"Received: '{arg}' of with length == {len(arg)}"
            )

    def add(self, range_list:List[int])->None:
        self.check_listrange_argument(range_list, "range_list", "add")

        # Our own Range datatype here.
        # It is not great that our 'Range' and 'intervaltree.Interval'
        # are mixed, however it is good to reuse the typechecks in
        # our range class
        target_range = Range(range_list[0], range_list[1])
        rangelist_logger.debug(f"Call to add {target_range} to the RangeList.")

        # Ignoring empty regions for simplicity
        if not target_range.is_empty():
            # Check overlap with minimally extended range
            # result in combining with the immediate neighlow value to bor ranges
            overlap = self.tree.overlap(target_range.low - 1, target_range.high + 1)
            rangelist_logger.debug(
                f"Removing overlap {overlap} of {target_range} with the current tree."
            )
            self.tree.remove_overlap(target_range.low - 1, target_range.high + 1)

            new_l = target_range.low
            new_h = target_range.high

            # Extend the ranges of the new interval in case it
            # needs to be joined with existing intervals
            if len(overlap) > 0:
                for inter in overlap:
                    new_l = min(new_l, inter.begin)
                    new_h = max(new_h, inter.end)

            rangelist_logger.debug(f"Adding [{new_l}, {new_h}) to the tree.")
            self.tree.addi(new_l, new_h)
        else:
            rangelist_logger.debug(f"{target_range} is empty.")

    def remove(self, range_list:List[int])->None:
        self.check_listrange_argument(range_list, "range_list", "remove")

        # Our own Range datatype here.
        # It is not great that our 'Range' and 'intervaltree.Interval'
        # are mixed, however it is good to reuse the typechecks in
        # our range class
        target_range = Range(range_list[0], range_list[1])
        rangelist_logger.debug(f"Call to remove {target_range} from the RangeList.")

        overlap = self.tree.overlap(target_range.low, target_range.high)
        rangelist_logger.debug(
            f"Removing overlap {overlap} of {target_range} with the current tree."
        )
        self.tree.remove_overlap(target_range.low, target_range.high)

        # Check for the leftovers of existing intervals need to
        # be added back
        if len(overlap) > 0:
            # initialize leftovers as empty.
            # adding empty ranges does nothing.
            low_leftover = Range(target_range.low, target_range.low)
            high_leftover = Range(target_range.high, target_range.high)

            for inter in overlap:
                low_leftover.low = min(low_leftover.low, inter.begin)
                high_leftover.high = max(high_leftover.high, inter.end)

            if not low_leftover.is_empty():
                rangelist_logger.debug(
                    f"Adding low leftover {low_leftover} to the tree."
                )
                self.tree.addi(low_leftover.low, low_leftover.high)
            else:
                rangelist_logger.debug("Low leftover is empty.")

            if not high_leftover.is_empty():
                rangelist_logger.debug(
                    f"Adding high leftover {high_leftover} to the tree."
                )
                self.tree.addi(high_leftover.low, high_leftover.high)
            else:
                rangelist_logger.debug("High leftover is empty.")

    def print(self)->None:
        intervals = list(inter for inter in self.tree)
        intervals_sorted = sorted(intervals, key=lambda x: x.begin)
        range_strings = []
        for inter in intervals_sorted:
            range_strings.append(f"[{inter.begin}, {inter.end})")
        print(" ".join(range_strings))
