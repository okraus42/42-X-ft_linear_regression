# precision.py
import sys
import csv
import os
import math

THETA_FILE = "thetas_denorm.txt"

def read_thetas(filename=THETA_FILE):
    theta0, theta1 = None, None
    try:
        with open(filename, "r") as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split("=")
                    if key == "theta0":
                        theta0 = float(value)
                    elif key == "theta1":
                        theta1 = float(value)
    except FileNotFoundError:
        print(f"{filename} not found!")
        return None, None

    if theta0 is None or theta1 is None:
        print("Theta values missing or malformed!")
        return None, None

    return theta0, theta1

def read_csv(filename):
    mileages = []
    prices = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mileages.append(float(row['km']))
            prices.append(float(row['price']))
    return mileages, prices

def estimate_price(mileage, theta0, theta1):
    return theta0 + theta1 * mileage

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 precision.py data.csv")
        sys.exit(1)

    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"File {data_file} does not exist.")
        sys.exit(1)

    theta0, theta1 = read_thetas()
    if theta0 is None or theta1 is None:
        print("Cannot evaluate precision without valid thetas.")
        sys.exit(1)

    mileages, prices = read_csv(data_file)
    m = len(mileages)

    errors = []
    squared_errors = []

    for i in range(m):
        predicted = estimate_price(mileages[i], theta0, theta1)
        error = predicted - prices[i]
        errors.append(abs(error))
        squared_errors.append(error ** 2)

    mae = sum(errors) / m
    mse = sum(squared_errors) / m
    rmse = math.sqrt(mse)

    print("Precision Metrics:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")

if __name__ == "__main__":
    main()
