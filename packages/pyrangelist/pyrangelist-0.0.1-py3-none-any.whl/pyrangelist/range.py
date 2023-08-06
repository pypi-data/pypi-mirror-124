class Range:
    def __init__(self, low, high):
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
        return self.low == self.high

    def __gt__(self, other):
        return self.low >= other.high

    def __lt__(self, other):
        return self.high <= other.low

    def __eq__(self, other):
        return self.low == other.low and self.high == other.high

    def __repr__(self):
        return f"[{self.low}, {self.high})"
