import csv
from pathlib import Path
import random


review = []

def print_score(num_correct: int, num_total: int):
    pct_correct = 100 * (float(num_correct) / num_total)
    print(f"\n\nYour score: {pct_correct:.1f}%")


def print_review():
    if review:
        print("\n\nReview these:")
        for row in review:
            print(f"\t{row}")


if __name__ == "__main__":
    data_file = Path(__file__).parent / "data.csv"
    assert data_file.is_file()

    data = []
    with open(data_file, mode="rt") as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    random.shuffle(data)

    num = 1
    num_correct = 0

    try:
        for en, es in data:
            es_response = input(f"{num:>4}. {en} →  ").strip()
            if es_response != es:
                print(f"Incorrect: {es}")
                review.append(f"{en} →  {es}")
            else:
                num_correct += 1
                
            num += 1
    except KeyboardInterrupt:
        print_score(num_correct, num)
        print_review()
        exit()
    print_score(num_correct, num)
    print_review()
