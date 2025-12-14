import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt

API_KEY = "807dabc1c9655942ba4436502f722e17"  

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather App")
        self.setFixedSize(350, 220)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        input_layout = QHBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name (e.g., Bengaluru)")
        self.city_input.returnPressed.connect(self.get_weather)

        get_button = QPushButton("Get Weather")
        get_button.clicked.connect(self.get_weather)

        input_layout.addWidget(self.city_input)
        input_layout.addWidget(get_button)

        self.location_label = QLabel("Location: -")
        self.temp_label = QLabel("Temperature: -")
        self.humidity_label = QLabel("Humidity: -")
        self.condition_label = QLabel("Condition: -")

        for lbl in [
            self.location_label,
            self.temp_label,
            self.humidity_label,
            self.condition_label,
        ]:
            lbl.setAlignment(Qt.AlignLeft)
            lbl.setStyleSheet("font-size: 14px;")

        main_layout.addLayout(input_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.location_label)
        main_layout.addWidget(self.temp_label)
        main_layout.addWidget(self.humidity_label)
        main_layout.addWidget(self.condition_label)

        self.setLayout(main_layout)

    def get_weather(self):
        city = self.city_input.text().strip()

        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return

        if API_KEY == "YOUR_API_KEY_HERE":
            QMessageBox.warning(
                self,
                "API Key Missing",
                "Please set your OpenWeatherMap API key in the code (API_KEY variable).",
            )
            return

        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"q={city}&appid={API_KEY}&units=metric"
            )
            response = requests.get(url, timeout=5)

            if response.status_code != 200:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Could not fetch weather.\n"
                    "Check the city name or your API key.",
                )
                return

            data = response.json()

            name = data.get("name", "Unknown")
            sys_info = data.get("sys", {})
            country = sys_info.get("country", "")
            main = data.get("main", {})
            weather_list = data.get("weather", [])

            temp = main.get("temp", "N/A")
            humidity = main.get("humidity", "N/A")
            if weather_list:
                condition = weather_list[0].get("description", "N/A").title()
            else:
                condition = "N/A"

            self.location_label.setText(f"Location: {name}, {country}")
            self.temp_label.setText(f"Temperature: {temp} °C")
            self.humidity_label.setText(f"Humidity: {humidity} %")
            self.condition_label.setText(f"Condition: {condition}")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Network Error",
                f"Something went wrong while connecting to the weather service.\n\n{e}",
            )


def main():
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()