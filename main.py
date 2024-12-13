import sys
from src.location_optimization import optimize_coffee_shops

def main():
    try:
        optimize_coffee_shops()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()