import matplotlib.pyplot as plt
from datetime import date

def main():
    plt.figure(figsize=(12, 6.75))
    plt.plot([1, 2, 3, 4], [10, 12, 9, 14])
    plt.title(f"Bot Test — {date.today().isoformat()}", loc="left")
    plt.tight_layout()
    plt.savefig("test_chart.png", dpi=150)
    plt.close()
    print("Saved test_chart.png")

if __name__ == "__main__":
    main()
