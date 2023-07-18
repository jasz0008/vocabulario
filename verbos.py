from argparse import ArgumentParser
from pathlib import Path
import random
from typing import Tuple

import pandas as pd


review = []

PARTICIPLE_CHOICES = ["present"]
INDICATIVE_CHOICES = ["present", "preterite"]
FORMS = [
    ("first_singular", "yo"),
    ("second_singular", "tú"),
    ("third_singular", "él/ella/usted"),
    ("first_plural", "nosotros"),
    ("third_plural", "ellos/ellas/ustedes"),
]


def get_infinitive(row: pd.Series, args) -> Tuple[str, str]:
    text = "infinitive"
    es = row.infinitive[0]
    return text, es


def get_participle(row: pd.Series, args) -> Tuple[str, str]:
    if args.participle is not None:
        participle = args.participle
    else:
        participle = random.choice(PARTICIPLE_CHOICES)
    text = f"{participle} participle"
    es = row["participle"][participle]
    return text, es


def get_indicative(row: pd.Series, args) -> Tuple[str, str]:
    form, text = random.choice(FORMS)
    if args.indicative is not None:
        indicative = args.indicative
    else:
        indicative = random.choice(INDICATIVE_CHOICES)
    text = f"{text} {indicative}"
    es = row[indicative][form]
    return text, es


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
        required=False,
        type=int,
        help="number of practice examples"
    )
    parser.add_argument(
        "--infinitive",
        required=False,
        action="store_true",
        help="review infinitives only"
    )
    parser.add_argument(
        "--participle",
        required=False,
        choices=PARTICIPLE_CHOICES,
        help="review participles only"
    )
    parser.add_argument(
        "--indicative",
        required=False,
        choices=INDICATIVE_CHOICES,
        help="review indicatives only"
    )
    args = parser.parse_args()

    data_file = Path(__file__).parent / "verbos.csv"
    assert data_file.is_file()

    df = pd.read_csv(data_file)
    df.columns = pd.MultiIndex.from_tuples([
        ("english", ""),
        ("infinitive", ""),
        ("participle", "present"),
        ("present", "first_singular"),
        ("present", "second_singular"),
        ("present", "third_singular"),
        ("present", "first_plural"),
        ("present", "third_plural"),
        ("preterite", "first_singular"),
        ("preterite", "second_singular"),
        ("preterite", "third_singular"),
        ("preterite", "first_plural"),
        ("preterite", "third_plural"),
    ])
    assert df.shape[0] > 0
    assert df.shape[1] == 13

    if args.n:
        assert args.n > 0
        args.n = min(args.n, df.shape[0])

    # For specific practice
    if args.infinitive:
        df = df[["english", "infinitive"]].copy()
    elif args.participle:
        df = df[["english", "participle"]].copy() # TODO hardcoded
    elif args.indicative:
        df = df[["english", args.indicative]]

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
            en = row.english[0]
            if args.infinitive:
                text, es = get_infinitive(row, args)
            elif args.participle:
                text, es = get_participle(row, args)
            elif args.indicative:
                text, es = get_indicative(row, args)
            else:
                fn = random.choices([
                    get_infinitive, get_participle, get_indicative
                ], weights=[1, 1, 10])[0]  # TODO hardcoded
                text, es = fn(row, args)
            rnum = total - num
            es_response = input(f"{rnum:>4}. {en} ({text}) →  ").strip()
            if es_response != es:
                print(f"Incorrect: {es}")
                review.append(f"{en} ({text}) →  {es}")
            else:
                num_correct += 1
    except KeyboardInterrupt:
        print_score(num_correct, num + 1)
        print_review()
        exit()
    print_score(num_correct, num + 1)
    print_review()
