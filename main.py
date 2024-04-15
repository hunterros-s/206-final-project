from weather import get_icao_code

def main():
    success, data = get_icao_code("San Francisco")
    print(data)

if __name__ == "__main__":
    main()