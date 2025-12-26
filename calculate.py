# calculate.py
import sys
import csv
import os
import math
import matplotlib.pyplot as plt

from estimate import estimatePrice, read_thetas

DEFAULT_LEARNING_RATE = 0.05
DEFAULT_ITERATIONS = 1000
THETA_FILE = "thetas.txt"
SETUP_FILE = "setup.txt"
DEBUG = False  # Set to False to disable printing each iteration


def plot_result(mileages, prices, theta0, theta1):
    # Scatter plot of original data
    plt.scatter(mileages, prices, label="Data")

    # Regression line
    x_vals = mileages
    y_vals = [theta0 + theta1 * x for x in x_vals]
    plt.plot(x_vals, y_vals, label="Regression line")

    plt.xlabel("Mileage")
    plt.ylabel("Price")
    plt.title("Linear Regression Result")
    plt.legend()
    plt.show()

def write_thetas(theta0, theta1, filename="thetas.txt"):
    with open(filename, "w") as file:
        file.write(f"theta0={theta0}\n")
        file.write(f"theta1={theta1}\n")

def write_thetas_denorm(theta0, theta1, filename="thetas_denorm.txt"):
    with open(filename, "w") as file:
        file.write(f"theta0={theta0}\n")
        file.write(f"theta1={theta1}\n")

def read_setup(filename=SETUP_FILE):
    learning_rate = DEFAULT_LEARNING_RATE
    iterations = DEFAULT_ITERATIONS
    try:
        with open(filename, "r") as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split("=")
                    if key == "learning_rate":
                        learning_rate = float(value)
                    elif key == "iterations":
                        iterations = int(value)
    except (FileNotFoundError, ValueError):
        pass
    return learning_rate, iterations

def read_csv(filename):
    mileages = []
    prices = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mileages.append(float(row['km']))
            prices.append(float(row['price']))
    return mileages, prices

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 calculate.py data.csv")
        sys.exit(1)

    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"File {data_file} does not exist.")
        sys.exit(1)

    learning_rate, iterations = read_setup()
    # theta0, theta1 = read_thetas()
    theta0, theta1 = 0.0, 0.0  # Start with zero thetas for training
    mileages, prices = read_csv(data_file)
    #normalise mileages and prices
    max_mileage = max(mileages) if mileages else 1
    max_price = max(prices) if prices else 1
    normalised_mileages = [mileage / max_mileage for mileage in mileages]
    normalised_prices = [price / max_price for price in prices]
    m = len(mileages)

    # Gradient descent iterations
    for iteration in range(iterations):
        sum0 = 0.0
        sum1 = 0.0

        for i in range(m):
            mileage = normalised_mileages[i]
            price = normalised_prices[i]

            estimated = estimatePrice(mileage, theta0, theta1)
            error = estimated - price

            sum0 += error
            sum1 += error * mileage

            # Debug output per data point
            if DEBUG:
                print(
                    f"i={i} | mileage={mileage} | price={price} | "
                    f"estimated={estimated} | error={error}"
                )
        tmp_theta0 = learning_rate * (sum0 / m)
        tmp_theta1 = learning_rate * (sum1 / m)
        theta0 -= tmp_theta0
        theta1 -= tmp_theta1

        if DEBUG:
            print(f"Iteration {iteration+1}: theta0 = {theta0}, theta1 = {theta1}")


    if math.isnan(theta0) or math.isnan(theta1):
        print("Theta values became NaN. Resetting to 0 and stopping training.")
        theta0, theta1 = 0.0, 0.0
        write_thetas(theta0, theta1)
        sys.exit(1)  # Exit early
    write_thetas(theta0, theta1)
    print(f"Training complete.")
    print(f"Updated theta0: {theta0}")
    print(f"Updated theta1: {theta1}")
    # Denormalize thetas
    theta0_denorm = theta0 * max_price
    theta1_denorm = theta1 * max_price / max_mileage

    write_thetas_denorm(theta0_denorm, theta1_denorm)
    print(f"Training complete.")
    print(f"Updated theta0 (denormalized): {theta0_denorm}")
    print(f"Updated theta1 (denormalized): {theta1_denorm}")

    # Plot using denormalized thetas
    plot_result(mileages, prices, theta0_denorm, theta1_denorm)


if __name__ == "__main__":
    main()
