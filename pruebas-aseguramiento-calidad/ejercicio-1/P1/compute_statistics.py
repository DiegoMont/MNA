"""Tool to get statistics of numbers in a file
"""
import sys
import time


def calculate_variance(sample: list, sample_mean: float) -> float:
    """Calculates the variance of a list of numbers.
    """
    e = 0
    for xi in sample:
        e += (xi - sample_mean) ** 2
    return e / (len(sample) - 1)

class Counter:
    """Class that counts how many ocurrences of elements have appeared.
    """
    def __init__(self):
        self.__elements: dict[float, int] = {}
        self.__mode: float | None = None

    def update(self, number: float):
        """Add number ocurrence to counter
        """
        if not number in self.__elements:
            self.__elements[number] = 0
        self.__elements[number] += 1
        if self.__mode is None:
            self.__mode = number
        if self.__elements[number] > self.__elements[self.__mode]:
            self.__mode = number

    def get_most_common(self) -> float | None:
        """Gets the number that appeared the most.
        """
        most_common_elements = sorted(
            self.__elements.items(),
            key=lambda item: item[1],
            reverse=True)
        if most_common_elements[0][1] == 1:
            return None
        return self.__mode


if __name__ == "__main__":
    start = time.time()
    filename = sys.argv[1]
    numbers = []
    MEAN = 0
    element_counter = Counter()
    with open(filename, encoding="utf-8") as file:
        for line in file:
            try:
                num = float(line)
                MEAN += num
                numbers.append(num)
                element_counter.update(num)
            except ValueError:
                print(f"Error: {line} is not a number")
    NUMBER_COUNT = len(numbers)
    MEAN /= NUMBER_COUNT
    numbers = sorted(numbers)
    ODD_AMOUNT_OF_NUMBERS = NUMBER_COUNT % 2 == 1
    MID_INDEX = NUMBER_COUNT // 2
    if ODD_AMOUNT_OF_NUMBERS:
        median = numbers[MID_INDEX]
    else:
        median = (numbers[MID_INDEX] + numbers[MID_INDEX - 1]) / 2
    mode = element_counter.get_most_common()
    variance = calculate_variance(numbers, MEAN)
    std_deviation = variance ** 0.5
    elapsed_time = time.time() - start
    count_report = f"COUNT: {NUMBER_COUNT}\n"
    mean_report = f"MEAN: {MEAN:10.3f}\n"
    median_report = f"MEDIAN: {median:10.3f}\n"
    MODE_REPORT = "MODE: " + ("N/A" if mode is None else str(mode)) + "\n"
    variance_report = f"VARIANCE: {variance:10.3f}\n"
    std_deviation_report = f"STD_DEV: {std_deviation:10.3f}\n"
    time_report = f"EXECUTION TIME: {elapsed_time:10.3f}s"
    statistics_report = count_report \
        + mean_report \
        + median_report \
        + MODE_REPORT \
        + std_deviation_report \
        + variance_report \
        + time_report
    print(statistics_report)
    with open("StatisticsResults.txt", "w", encoding="utf-8") as results_file:
        results_file.write(statistics_report)
