import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from elections.models import Region, Territory, Precinct, Candidate, VoteResult  # noqa


CSV_PATH = r"C:\Users\Abuna\elections2018\data\voting_data_eng.csv"


CANDIDATE_COLUMNS = [
    "Baburin Sergei Nikolaevich",
    "Grudinin Pavel Nikolaevich",
    "Zhirinovskiy Vladimir Volfovich",
    "Putin Vladimir Vladimirovich",
    "Sobchak Ksenia Anatolyevna",
    "Suraikin Maksim Aleksandrovich",
    "Titov Boris Yurievich",
    "Yavlinskiy Gregory Alekseivich",
]


def main():
    # создаём записи кандидатов (если ещё нет)
    candidates = {}
    for col in CANDIDATE_COLUMNS:
        candidate, _ = Candidate.objects.get_or_create(name=col)
        candidates[col] = candidate

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            region_name = row["region_name"].strip()
            subregion_name = row["subregion_name"].strip()

            region, _ = Region.objects.get_or_create(name=region_name)
            territory, _ = Territory.objects.get_or_create(
                region=region,
                name=subregion_name,
            )

            precinct = Precinct.objects.create(
                territory=territory,
                precinct_number=row["ps_id"],
                registered_voters=int(row["Number of voters enlisted"] or 0),
                ballots_issued=int(row["Number of ballot papers in ballot boxes"] or 0),
                ballots_valid=int(row["Number of valid ballot papers"] or 0),
                ballots_invalid=int(row["Number of invalid ballot papers"] or 0),
            )

            for col in CANDIDATE_COLUMNS:
                votes_str = row[col].strip()
                votes = int(votes_str) if votes_str else 0
                VoteResult.objects.create(
                    precinct=precinct,
                    candidate=candidates[col],
                    votes=votes,
                )

            if i % 500 == 0:
                print(f"Imported {i} rows...")


if __name__ == "__main__":
    main()
