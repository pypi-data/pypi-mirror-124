from specific import Nations


def main():
    crime = Nations()
    print(crime.data_sample("2020-12-30"))
    crime.run()


if __name__ == "__main__":
    main()
