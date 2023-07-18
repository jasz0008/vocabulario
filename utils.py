class Scorer:
    review = []

    def print_score(self, num_correct: int, num_total: int):
        pct_correct = 100 * (float(num_correct) / num_total)
        print(f"\n\nYour score: {pct_correct:.1f}%")


    def print_review(self):
        if review:
            print("\n\nReview these:")
            for row in review:
                print(f"\t{row}")