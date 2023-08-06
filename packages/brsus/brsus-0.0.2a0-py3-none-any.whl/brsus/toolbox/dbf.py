import csv
import subprocess

from dbfread import DBF


def blast_decompresser(input_file: str, output_file: str):
    subprocess.call(["./thirdy_part/blast-dbf", input_file, output_file])


def _dbf_data(input_file: str):
    yield from DBF(input_file)


def dbf2csv(input_file: str, output_file: str):
    data = _dbf_data(input_file)

    with open(output_file, "w") as f:
        header = next(data)
        writer = csv.DictWriter(f, fieldnames=header.keys())
        writer.writeheader()
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    blast_decompresser("data/DOSP2019.DBC", "data/DECOMPRESSED_DOSP2019.DBF")
    dbf2csv("data/DECOMPRESSED_DOSP2019.DBF", "data/DOSP2019.csv")
