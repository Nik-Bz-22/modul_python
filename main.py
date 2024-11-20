import csv
import os
from datetime import datetime
import random
from typing import List, Dict, Optional

import matplotlib.pyplot as plt
from faker import Faker

fake = Faker()


class OrderManager:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        self.orders: List[Dict[str, str]] = []
        self.load_orders()

    def load_orders(self) -> None:
        if not os.path.exists(self.filename):
            print("Файл не знайдено, буде створено новий.")
            return
        try:
            with open(self.filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.orders = [row for row in reader]
        except Exception as e:
            print(f"Помилка завантаження файлу: {e}")

    def save_orders(self) -> None:
        try:
            with open(self.filename, mode="w", encoding="utf-8", newline="") as file:
                fieldnames = [
                    "Ім'я клієнта",
                    "Номер замовлення",
                    "Дата замовлення",
                    "Сума замовлення",
                    "Статус",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.orders)
        except Exception as e:
            print(f"Помилка збереження файлу: {e}")

    def add_order(
        self,
        client_name: str,
        order_number: int,
        order_date: str,
        order_amount: float,
        status: str,
    ) -> None:
        self.orders.append(
            {
                "Ім'я клієнта": client_name,
                "Номер замовлення": str(order_number),
                "Дата замовлення": order_date,
                "Сума замовлення": f"{float(order_amount):.2f}",
                "Статус": status,
            }
        )
        self.save_orders()

    def edit_order(self, order_number: int, **kwargs: Dict[str, str]) -> None:
        for order in self.orders:
            if order["Номер замовлення"] == str(order_number):
                for key, value in kwargs.items():
                    if key in order:
                        order[key] = value
                self.save_orders()
                return
        print("Замовлення не знайдено.")

    def delete_order(self, order_number: int) -> None:
        self.orders = [
            order
            for order in self.orders
            if order["Номер замовлення"] != str(order_number)
        ]
        self.save_orders()

    def list_orders(self) -> None:
        print(f"{'Ім\'я клієнта':<20} {'Номер замовлення':<15} \
            {'Дата замовлення':<15} \
            {'Сума замовлення':<15} \
            {'Статус':<10}")
        print("-" * 80)
        for order in self.orders:
            print(f"{order['Ім\'я клієнта']:<20} \
                {order['Номер замовлення']:<15} \
                {order['Дата замовлення']:<15} \
                {order['Сума замовлення']:<15} \
                {order['Статус']:<10}")

    def analyze_orders(self) -> None:
        total_orders: int = len(self.orders)
        total_amount: float = sum(
            float(order["Сума замовлення"]) for order in self.orders
        )
        completed_orders: int = len(
            [order for order in self.orders if order["Статус"] == "Виконано"]
        )
        in_progress_orders: int = total_orders - completed_orders
        print(f"Загальна кількість замовлень: {total_orders}")
        print(f"Сумарна вартість: {total_amount:.2f}")
        print(f"Виконано: {completed_orders}, В процесі: {in_progress_orders}")

    def find_largest_order(self) -> Optional[Dict[str, str]]:
        if not self.orders:
            print("Список замовлень порожній.")
            return None
        largest_order = max(self.orders, key=lambda x: x["Сума замовлення"])
        print("Замовлення з найбільшою сумою:")
        print(largest_order)
        return largest_order

    def visualize_status_pie_chart(self) -> None:
        completed_orders: int = len(
            [order for order in self.orders if order["Статус"] == "Виконано"]
        )
        in_progress_orders: int = len(self.orders) - completed_orders
        labels = ["Виконано", "В процесі"]
        sizes = [completed_orders, in_progress_orders]
        plt.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=["green", "orange"],
        )
        plt.title("Статус замовлень")
        plt.show()

    def visualize_orders_histogram(self) -> None:
        date = [
            datetime.strptime(order["Дата замовлення"], "%Y-%m-%d")
            for order in self.orders
        ]
        dates = [date.strftime("%Y-%m-%d") for date in sorted(dates)]
        plt.hist(dates, bins=len(set(dates)), color="blue", rwidth=0.8)
        plt.title("Кількість замовлень за датами")
        plt.xlabel("Дата")
        plt.ylabel("Кількість замовлень")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def generate_random_order(self) -> tuple[str, int, str, float, str]:
        order = (
            fake.name(),
            random.randint(0, 5000),
            str(fake.date_this_year()),
            round(random.uniform(100.00, 5000.00), 2),
            random.choice(["Виконано", "В процесі"]),
        )
        return order


if __name__ == "__main__":
    manager = OrderManager("data.csv")
    manager.add_order(*manager.generate_random_order())
    manager.list_orders()
    manager.analyze_orders()
    manager.find_largest_order()
    manager.visualize_status_pie_chart()
    manager.visualize_orders_histogram()
