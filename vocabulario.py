from argparse import ArgumentParser
from pathlib import Path
import random

import pandas as pd


# TODO
# places
# nationalities
# languages
# gran, mal, buen
# puede ser, a lo mejor


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
    parser = ArgumentParser()
    parser.add_argument(
        "-n",
        type=int,
        help="number of practice examples"
    )
    parser.add_argument(
        "-c",
        type=int,
        help="chapter to review"
    )
    args = parser.parse_args()

    data_file = Path(__file__).parent / "vocabulario.csv"
    assert data_file.is_file()

    df = pd.read_csv(data_file)
    df.columns = ("en", "es", "cap")
    assert df.shape[0] > 0
    assert df.shape[1] == 3

    if args.n:
        assert args.n > 0
        args.n = min(args.n, df.shape[0])

    if args.c:
        assert args.c in df.cap.unique()

    # Filter by desired chapter first
    if args.c:
        df = df[df.cap == args.c]

    # Randomly sample
    if args.n:
        frac = args.n / df.shape[0]
    else:
        frac = 1.0
    df = df.sample(frac=frac).reset_index(drop=True)

    total = df.shape[0]
    num_correct = 0

    try:
        for num, row in df.iterrows():
            rnum = total - num + 1  # End at 1, not 0
            en = row.en
            es = row.es
            rnum = total - num
            es_response = input(f"{rnum:>4}. {en} →  ").strip()
            if es_response != es:
                print(f"Incorrect: {es}")
                review.append(f"{en} →  {es}")
            else:
                num_correct += 1
    except KeyboardInterrupt:
        print_score(num_correct, num)
        print_review()
        exit()
    print_score(num_correct, num)
    print_review()
