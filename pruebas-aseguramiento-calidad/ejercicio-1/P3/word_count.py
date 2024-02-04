"""Program to count words in a file
"""

import sys
import time


def count_words(filename: str) -> str:
    """Counts unique lines in file
    """
    word_counts = ""
    counter = {}
    with open(filename, encoding="utf-8") as file:
        for line in file:
            phrase = line.strip()
            if phrase not in counter:
                counter[phrase] = 0
            counter[phrase] += 1
        grand_total = 0
        for word, count in counter.items():
            grand_total += count
            word_counts += f"{word}    {count}\n"
        word_counts += f"Grand Total {grand_total}\n"
    return word_counts


if __name__ == "__main__":
    start = time.time()
    PROGRAM_OUTPUT = count_words(sys.argv[1])
    elapsed_time = time.time() - start
    time_report = f"EXECUTION TIME: {elapsed_time:10.3f}s"
    PROGRAM_OUTPUT += time_report
    print(PROGRAM_OUTPUT)
    with open("WordCountResults.txt", "w", encoding="utf-8") as results_file:
        results_file.write(PROGRAM_OUTPUT)
