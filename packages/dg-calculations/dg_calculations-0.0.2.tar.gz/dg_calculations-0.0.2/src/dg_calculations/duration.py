class Duration:

    def __init__(self, hours: int = 0, minutes: int = 0, seconds: int = 0):
        # setup the class instance and convert any provided times to seconds
        self.total_duration: int = (hours * 60 * 60) + (minutes * 60) + seconds

    def __add__(self, other):
        new_total: int = self.total_duration + other.total_duration
        return Duration(seconds=new_total)

    def get_hours(self) -> int:
        # return only the hours
        return self.total_duration // (60 * 60)

    def get_minutes(self) -> int:
        # return only the minutes
        return (self.total_duration % (60 * 60)) // 60

    def get_seconds(self) -> int:
        # return only the seconds
        return (self.total_duration % (60 * 60)) % 60

    def get_all(self) -> tuple[int, int, int]:
        # return the total duration as hours, minutes & seconds individually
        return self.get_hours(), self.get_minutes(), self.get_minutes()

    def __str__(self) -> str:
        # quick and simple representation of the duration
        return f'{self.get_hours()}hrs {self.get_minutes()}mins {self.get_seconds()}secs'
