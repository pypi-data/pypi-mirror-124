from pnd import specific


def main():
    crime = specific.Nations()
    print(crime.data_sample("2020-12-30"))


if __name__ == "__main__":
    main()
