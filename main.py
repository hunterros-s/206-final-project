from weather import get_icao_code


def main():
    success, data = get_icao_code("70112")
    print(data)

if __name__ == "__main__":
    main()