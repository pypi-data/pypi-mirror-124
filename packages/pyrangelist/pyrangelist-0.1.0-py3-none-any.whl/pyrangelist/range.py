class Range:
    def __init__(self, low:int, high:int, check_format:bool=True):
        if check_format:
            if not isinstance(low, int):
                raise TypeError(
                    f"Range constructor argument 'low' must be int, "
                    f"received '{low}' of type '{type(low)}'"
                )

            if not isinstance(high, int):
                raise TypeError(
                    f"Range constructor argument 'high' must be int, "
                    f"received '{high}' of type '{type(high)}'"
                )

            if low > high:
                raise ValueError(
                    f"Range constructor argument 'low' must be >= "
                    f"range constructor argument 'high'. Received: "
                    f"low '{low}' > high '{high}'"
                )

        self.low = low
        self.high = high

    def is_empty(self):
        return self.low >= self.high

    def contains(self, other):
        return self.low <= other.low and self.high >= other.high

    def is_touching(self, other):
        return (
            (self.low <= other.high and self.low >= other.low) or
            (self.high <= other.high and self.high >= other.low) or
            (other.low <= self.high and other.low >= self.low) or
            (other.high <= self.high and other.high >= self.low)
        )

    def intersection(self, other):
        low=max(self.low, other.low)
        high=min(self.high, other.high)

        if low > high:
            low = 0
            high = 0
        return Range(low, high)

    def union(self, other):
        if not self.is_touching(other):
            raise ValueError(f"Unable to merge non-touching ranges {self} and {other}")

        result = Range(
            low=min(self.low, other.low),
            high=max(self.high, other.high)
        )
        return result

    def __gt__(self, other):
        return self.low >= other.high

    def __lt__(self, other):
        return self.high <= other.low

    def __eq__(self, other):
        return self.low == other.low and self.high == other.high

    def __repr__(self):
        return f"[{self.low}, {self.high})"
