# estimate_price.py
def read_thetas(filename="thetas_denorm.txt"):
    theta0, theta1 = 0.0, 0.0
    try:
        with open(filename, "r") as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split("=")
                    if key == "theta0":
                        theta0 = float(value)
                    elif key == "theta1":
                        theta1 = float(value)
    except (FileNotFoundError, ValueError):
        pass
    return theta0, theta1

def estimatePrice(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def main():
    theta0, theta1 = read_thetas()
    try:
        mileage = float(input("Enter mileage: ").strip())
    except ValueError:
        print("Invalid mileage input. Using 0.")
        mileage = 0.0

    price = estimatePrice(mileage, theta0, theta1)
    print(f"Estimated price: {price}")

if __name__ == "__main__":
    main()
