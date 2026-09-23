import os
import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


# ==========================================
# 1. ABSTRACT BASE CLASS & DOMAIN MODELS
# ==========================================

class Trip(ABC):
    """Abstract Base Class representing a Transport Trip"""
    
    def __init__(self, trip_id: int, source: str, destination: str, 
                 travel_date: str, departure_time: str, total_seats: int, 
                 available_seats: int, base_fare: float):
        self._trip_id = trip_id
        self._source = source
        self._destination = destination
        self._travel_date = travel_date
        self._departure_time = departure_time
        self._total_seats = total_seats
        self._available_seats = available_seats
        self._base_fare = base_fare

    @property
    def trip_id(self) -> int:
        return self._trip_id

    @property
    def source(self) -> str:
        return self._source

    @property
    def destination(self) -> str:
        return self._destination

    @property
    def travel_date(self) -> str:
        return self._travel_date

    @property
    def departure_time(self) -> str:
        return self._departure_time

    @property
    def total_seats(self) -> int:
        return self._total_seats

    @property
    def available_seats(self) -> int:
        return self._available_seats

    @available_seats.setter
    def available_seats(self, count: int):
        if 0 <= count <= self._total_seats:
            self._available_seats = count

    @property
    def base_fare(self) -> float:
        return self._base_fare

    @abstractmethod
    def get_transport_type(self) -> str:
        pass

    @abstractmethod
    def calculate_total_fare(self) -> float:
        pass


class BusTrip(Trip):
    """Derived Class for Bus Services"""
    
    def __init__(self, trip_id: int, source: str, destination: str, 
                 travel_date: str, departure_time: str, total_seats: int, 
                 available_seats: int, base_fare: float, bus_operator: str, bus_type: str, rating: float):
        super().__init__(trip_id, source, destination, travel_date, departure_time, 
                         total_seats, available_seats, base_fare)
        self._bus_operator = bus_operator
        self._bus_type = bus_type
        self._rating = rating

    @property
    def bus_operator(self) -> str:
        return self._bus_operator

    @property
    def bus_type(self) -> str:
        return self._bus_type

    @property
    def rating(self) -> float:
        return self._rating

    def get_transport_type(self) -> str:
        return f"{self._bus_operator} ({self._bus_type})"

    def calculate_total_fare(self) -> float:
        return round(self._base_fare * 1.05, 2)


class TrainTrip(Trip):
    """Derived Class for Train Services"""
    
    def __init__(self, trip_id: int, source: str, destination: str, 
                 travel_date: str, departure_time: str, total_seats: int, 
                 available_seats: int, base_fare: float, train_name: str, train_number: str):
        super().__init__(trip_id, source, destination, travel_date, departure_time, 
                         total_seats, available_seats, base_fare)
        self._train_name = train_name
        self._train_number = train_number

    @property
    def train_name(self) -> str:
        return self._train_name

    @property
    def train_number(self) -> str:
        return self._train_number

    def get_transport_type(self) -> str:
        return f"{self._train_number} - {self._train_name}"

    def calculate_total_fare(self) -> float:
        return round(self._base_fare + 50.0, 2)


class Passenger:
    def __init__(self, passenger_id: int, name: str, mobile: str, email: str):
        self._passenger_id = passenger_id
        self._name = name
        self._mobile = mobile
        self._email = email

    @property
    def passenger_id(self) -> int:
        return self._passenger_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def mobile(self) -> str:
        return self._mobile

    @property
    def email(self) -> str:
        return self._email


class Booking:
    def __init__(self, booking_id: int, passenger_id: int, trip_id: int, 
                 seat_number: int, booking_date: str, fare: float, status: str = "CONFIRMED"):
        self._booking_id = booking_id
        self._passenger_id = passenger_id
        self._trip_id = trip_id
        self._seat_number = seat_number
        self._booking_date = booking_date
        self._fare = fare
        self._status = status

    @property
    def booking_id(self) -> int:
        return self._booking_id

    @property
    def passenger_id(self) -> int:
        return self._passenger_id

    @property
    def trip_id(self) -> int:
        return self._trip_id

    @property
    def seat_number(self) -> int:
        return self._seat_number

    @property
    def booking_date(self) -> str:
        return self._booking_date

    @property
    def fare(self) -> float:
        return self._fare

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str):
        if new_status in ["CONFIRMED", "CANCELLED"]:
            self._status = new_status


# ==========================================
# 2. TRANSPORT SYSTEM MANAGER
# ==========================================

class TransportSystem:
    TRIP_FILE = "trips.txt"
    PASSENGER_FILE = "passengers.txt"
    BOOKING_FILE = "bookings.txt"

    def __init__(self, mode: str):
        self._mode = mode.upper()  # "BUS" or "TRAIN"
        self._trips: List[Trip] = []
        self._passengers: List[Passenger] = []
        self._bookings: List[Booking] = []
        
        self.load_data()
        if not self._trips:
            self.seed_preset_data()

    # --- Validations ---
    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    @staticmethod
    def is_valid_mobile(mobile: str) -> bool:
        return bool(re.match(r"^\d{10}$", mobile))

    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_time(time_str: str) -> bool:
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    @staticmethod
    def normalize_city_name(city: str) -> str:
        """Fixes common spelling mistakes for cities."""
        city_clean = city.strip().lower()
        mapping = {
            "hyderbad": "Hyderabad",
            "hyd": "Hyderabad",
            "hyderabad": "Hyderabad",
            "chenai": "Chennai",
            "chennai": "Chennai",
            "vijaywada": "Vijayawada",
            "vijayawada": "Vijayawada",
            "bangalore": "Bengaluru",
            "bengaluru": "Bengaluru",
            "mysore": "Mysuru",
            "mysuru": "Mysuru",
            "cuddapah": "Kadapa",
            "kadapa": "Kadapa"
        }
        return mapping.get(city_clean, city.strip().title())

    # --- Preset Route Data ---
    def seed_preset_data(self):
        if self._mode == "BUS":
            self._trips = [
                # Kadapa to Chennai
                BusTrip(101, "Kadapa", "Chennai", "2026-05-15", "14:30", 36, 18, 650.0, "APSRTC", "Super Luxury Non-AC", 4.3),
                BusTrip(102, "Kadapa", "Chennai", "2026-05-15", "21:00", 30, 10, 850.0, "APS Travels", "AC Sleeper (2+1)", 4.5),
                # Hyderabad to Chennai
                BusTrip(103, "Hyderabad", "Chennai", "2026-05-15", "13:30", 36, 15, 950.0, "Orange Tours & Travels", "Volvo Multi-Axle AC Sleeper", 4.8),
                BusTrip(104, "Hyderabad", "Chennai", "2026-05-15", "18:00", 40, 20, 850.0, "IntrCity SmartBus", "AC Sleeper (2+1)", 4.6),
                # Hyderabad to Vijayawada
                BusTrip(105, "Hyderabad", "Vijayawada", "2026-05-15", "14:00", 36, 12, 500.0, "TGSRTC", "Super Luxury Non-AC", 4.2),
                # Bengaluru to Mysuru
                BusTrip(106, "Bengaluru", "Mysuru", "2026-05-15", "14:30", 45, 18, 320.0, "KSRTC", "EV PowerPlus AC", 4.7),
            ]
        else:
            self._trips = [
                # Kadapa to Chennai
                TrainTrip(201, "Kadapa", "Chennai", "2026-05-15", "15:20", 100, 25, 310.0, "Kacheguda Chennai Express", "17652"),
                # Hyderabad to Chennai
                TrainTrip(202, "Hyderabad", "Chennai", "2026-05-15", "12:45", 120, 35, 450.0, "Charminar Express", "12760"),
                TrainTrip(203, "Hyderabad", "Chennai", "2026-05-15", "17:15", 150, 60, 520.0, "Chennai SF Express", "12604"),
            ]
        self.save_data()

    # --- Data Persistence ---
    def load_data(self):
        if os.path.exists(self.PASSENGER_FILE):
            with open(self.PASSENGER_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self._passengers.append(Passenger(int(parts[0]), parts[1], parts[2], parts[3]))

        if os.path.exists(self.TRIP_FILE):
            with open(self.TRIP_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 9:
                        mode_type = parts[0]
                        if mode_type == "BUS" and self._mode == "BUS":
                            operator = parts[9] if len(parts) > 9 else "Express Operator"
                            bus_type = parts[10] if len(parts) > 10 else "Standard AC"
                            rating = float(parts[11]) if len(parts) > 11 else 4.0
                            
                            self._trips.append(BusTrip(
                                int(parts[1]), parts[2], parts[3], parts[4], parts[5],
                                int(parts[6]), int(parts[7]), float(parts[8]),
                                operator, bus_type, rating
                            ))
                        elif mode_type == "TRAIN" and self._mode == "TRAIN":
                            train_name = parts[9] if len(parts) > 9 else "Express Train"
                            train_num = parts[10] if len(parts) > 10 else "10000"
                            
                            self._trips.append(TrainTrip(
                                int(parts[1]), parts[2], parts[3], parts[4], parts[5],
                                int(parts[6]), int(parts[7]), float(parts[8]),
                                train_name, train_num
                            ))

        if os.path.exists(self.BOOKING_FILE):
            with open(self.BOOKING_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 7:
                        self._bookings.append(Booking(
                            int(parts[0]), int(parts[1]), int(parts[2]),
                            int(parts[3]), parts[4], float(parts[5]), parts[6]
                        ))

    def save_data(self):
        with open(self.TRIP_FILE, "w") as f:
            for t in self._trips:
                if isinstance(t, BusTrip):
                    f.write(f"BUS|{t.trip_id}|{t.source}|{t.destination}|{t.travel_date}|"
                            f"{t.departure_time}|{t.total_seats}|{t.available_seats}|{t.base_fare}|"
                            f"{t.bus_operator}|{t.bus_type}|{t.rating}\n")
                elif isinstance(t, TrainTrip):
                    f.write(f"TRAIN|{t.trip_id}|{t.source}|{t.destination}|{t.travel_date}|"
                            f"{t.departure_time}|{t.total_seats}|{t.available_seats}|{t.base_fare}|"
                            f"{t.train_name}|{t.train_number}\n")

        with open(self.PASSENGER_FILE, "w") as f:
            for p in self._passengers:
                f.write(f"{p.passenger_id}|{p.name}|{p.mobile}|{p.email}\n")

        with open(self.BOOKING_FILE, "w") as f:
            for b in self._bookings:
                f.write(f"{b.booking_id}|{b.passenger_id}|{b.trip_id}|{b.seat_number}|"
                        f"{b.booking_date}|{b.fare}|{b.status}\n")

    # --- Add New Route / Trip ---
    def add_new_route(self):
        print(f"\n=================== ADD NEW {self._mode} ROUTE ===================")
        try:
            trip_id = int(input("Enter New Trip ID: "))
            if any(t.trip_id == trip_id for t in self._trips):
                print("[Error] Trip ID already exists.")
                return

            raw_source = input("Enter Source City: ").strip()
            raw_dest = input("Enter Destination City: ").strip()
            source = self.normalize_city_name(raw_source)
            destination = self.normalize_city_name(raw_dest)

            while True:
                travel_date = input("Enter Travel Date (YYYY-MM-DD): ").strip()
                if self.is_valid_date(travel_date):
                    break
                print("[Error] Invalid Date Format! Please use YYYY-MM-DD.")

            while True:
                dep_time = input("Enter Departure Time (HH:MM in 24hr): ").strip()
                if self.is_valid_time(dep_time):
                    break
                print("[Error] Invalid Time Format! Please use HH:MM.")

            total_seats = int(input("Enter Total Seats: "))
            available_seats = int(input("Enter Available Seats: "))
            if available_seats > total_seats:
                print("[Error] Available seats cannot exceed total seats.")
                return

            base_fare = float(input("Enter Base Fare (₹): "))

            if self._mode == "BUS":
                operator = input("Enter Bus Operator Name: ").strip()
                bus_type = input("Enter Bus Type (e.g., AC Sleeper, Volvo): ").strip()
                rating = float(input("Enter Bus Rating (e.g., 4.5): "))
                
                new_trip = BusTrip(trip_id, source, destination, travel_date, dep_time,
                                   total_seats, available_seats, base_fare, operator, bus_type, rating)
            else:
                train_name = input("Enter Train Name: ").strip()
                train_num = input("Enter Train Number: ").strip()
                
                new_trip = TrainTrip(trip_id, source, destination, travel_date, dep_time,
                                    total_seats, available_seats, base_fare, train_name, train_num)

            self._trips.append(new_trip)
            self.save_data()
            print(f"[Success] New {self._mode.lower()} route from {source} to {destination} added successfully!")

        except ValueError:
            print("[Error] Invalid numeric input entered.")

    # --- Search Functionality ---
    def search_available_services(self):
        print(f"\n=================== SEARCH {self._mode} ROUTES ===================")
        raw_source = input("Enter Source City (e.g., Hyderabad, Bengaluru, Kadapa): ").strip()
        raw_dest = input("Enter Destination City (e.g., Vijayawada, Chennai): ").strip()
        
        source = self.normalize_city_name(raw_source)
        destination = self.normalize_city_name(raw_dest)

        results = []
        source_fallback = []

        for trip in self._trips:
            if trip.source.lower() == source.lower():
                source_fallback.append(trip)
                if trip.destination.lower() == destination.lower():
                    results.append(trip)

        if results:
            print(f"\n[Success] Available {self._mode.lower()} service(s) for {source} -> {destination}:\n")
            self._display_results(results)
            return

        print(f"\n[Info] No direct {self._mode.lower()} route found for '{source}' -> '{destination}'.")
        if source_fallback:
            print(f"Here are other available {self._mode.lower()} services departing from '{source}':\n")
            self._display_results(source_fallback)
        else:
            print(f"Showing all scheduled {self._mode.lower()} services in system:\n")
            self._display_results(self._trips)

    def _display_results(self, trip_list: List[Trip]):
        if self._mode == "BUS":
            print(f"{'ID':<6}{'Route':<25}{'Operator & Bus Type':<35}{'Date':<12}{'Time':<8}{'Rating':<8}{'Seats':<10}{'Fare':<10}")
            print("-" * 115)
            for b in trip_list:
                route = f"{b.source} -> {b.destination}"
                seats = f"{b.available_seats} Left"
                fare = f"₹{b.calculate_total_fare():.2f}"
                details = f"{b.bus_operator} ({b.bus_type})"
                rating = f"★ {b.rating}"
                print(f"{b.trip_id:<6}{route:<25}{details:<35}{b.travel_date:<12}{b.departure_time:<8}{rating:<8}{seats:<10}{fare:<10}")
            print("-" * 115)
        else:
            print(f"{'ID':<6}{'Route':<25}{'Train Number & Name':<35}{'Date':<12}{'Time':<8}{'Seats':<10}{'Fare':<10}")
            print("-" * 105)
            for t in trip_list:
                route = f"{t.source} -> {t.destination}"
                seats = f"{t.available_seats} Left"
                fare = f"₹{t.calculate_total_fare():.2f}"
                details = f"{t.get_transport_type()}"
                print(f"{t.trip_id:<6}{route:<25}{details:<35}{t.travel_date:<12}{t.departure_time:<8}{seats:<10}{fare:<10}")
            print("-" * 105)

    def view_all_trips(self):
        self._display_results(self._trips)

    def register_passenger(self):
        print("\n--- Register Passenger ---")
        try:
            pid = int(input("Enter Passenger ID: "))
        except ValueError:
            print("[Error] Passenger ID must be an integer.")
            return

        if any(p.passenger_id == pid for p in self._passengers):
            print("[Error] Passenger ID already registered.")
            return

        name = input("Enter Name: ").strip()

        while True:
            mobile = input("Enter 10-digit Mobile: ").strip()
            if self.is_valid_mobile(mobile):
                break
            print("[Error] Invalid Mobile Number!")

        while True:
            email = input("Enter Email: ").strip()
            if self.is_valid_email(email):
                break
            print("[Error] Invalid Email Address!")

        self._passengers.append(Passenger(pid, name, mobile, email))
        self.save_data()
        print(f"[Success] Passenger '{name}' registered successfully!")

    def book_ticket(self):
        print(f"\n--- Book {self._mode} Ticket ---")
        try:
            bid = int(input("Enter New Booking ID: "))
            if any(b.booking_id == bid for b in self._bookings):
                print("[Error] Booking ID already exists.")
                return

            pid = int(input("Enter Passenger ID: "))
            if not any(p.passenger_id == pid for p in self._passengers):
                print("[Error] Passenger not registered. Please register first.")
                return

            tid = int(input(f"Enter {self._mode} Trip ID: "))
            trip = next((t for t in self._trips if t.trip_id == tid), None)
            if not trip:
                print(f"[Error] Trip ID not found.")
                return

            if trip.available_seats <= 0:
                print("[Error] No seats available on this service.")
                return

            seat_no = int(input(f"Enter Seat Number (1 to {trip.total_seats}): "))
            if seat_no < 1 or seat_no > trip.total_seats:
                print("[Error] Seat number out of range.")
                return

            if any(b.trip_id == tid and b.seat_number == seat_no and b.status == "CONFIRMED" for b in self._bookings):
                print(f"[Error] Seat {seat_no} is already booked.")
                return

            bdate = datetime.now().strftime("%Y-%m-%d")
            total_fare = trip.calculate_total_fare()
            new_booking = Booking(bid, pid, tid, seat_no, bdate, total_fare, "CONFIRMED")

            trip.available_seats -= 1
            self._bookings.append(new_booking)

            self.save_data()
            print(f"[Success] Reservation Successful! Ticket Fare: ₹{total_fare:.2f}")
            
            # Print ticket receipt automatically
            print("\nPrinting Digital Ticket Pass...")
            self.display_booking_details(bid)

        except ValueError:
            print("[Error] Invalid numerical input.")

    # --- View Booked Ticket Details ---
    def display_booking_details(self, booking_id: Optional[int] = None):
        if booking_id is None:
            print(f"\n=================== VIEW BOOKED TICKET ===================")
            try:
                booking_id = int(input("Enter Booking ID: "))
            except ValueError:
                print("[Error] Booking ID must be a number.")
                return

        booking = next((b for b in self._bookings if b.booking_id == booking_id), None)
        if not booking:
            print(f"[Error] No booking found with ID {booking_id}.")
            return

        passenger = next((p for p in self._passengers if p.passenger_id == booking.passenger_id), None)
        trip = next((t for t in self._trips if t.trip_id == booking.trip_id), None)

        print("\n" + "=" * 50)
        print(f"        OFFICIAL {self._mode} E-TICKET PASS        ")
        print("=" * 50)
        print(f" Booking ID    : {booking.booking_id}")
        print(f" Booking Date  : {booking.booking_date}")
        print(f" Status        : {booking.status}")
        print("-" * 50)
        
        if passenger:
            print(f" Passenger ID  : {passenger.passenger_id}")
            print(f" Name          : {passenger.name}")
            print(f" Mobile        : {passenger.mobile}")
            print(f" Email         : {passenger.email}")
        else:
            print(f" Passenger ID  : {booking.passenger_id} (Details Not Found)")
            
        print("-" * 50)
        if trip:
            print(f" Trip ID       : {trip.trip_id}")
            print(f" Service       : {trip.get_transport_type()}")
            print(f" Route         : {trip.source} -> {trip.destination}")
            print(f" Travel Date   : {trip.travel_date}")
            print(f" Departure Time: {trip.departure_time}")
            print(f" Seat Number   : {booking.seat_number}")
        else:
            print(f" Trip ID       : {booking.trip_id} (Trip Details Not Found)")

        print("-" * 50)
        print(f" Total Paid    : ₹{booking.fare:.2f}")
        print("=" * 50 + "\n")


# ==========================================
# 3. INTERACTIVE CLI INTERFACE
# ==========================================

def select_mode() -> str:
    print("======================================================")
    print("      TRANSPORTATION TICKET RESERVATION SYSTEM        ")
    print("======================================================")
    print("Select Platform:")
    print("1. Bus Search & Reservation")
    print("2. Train Search & Reservation")
    print("3. Exit System")
    
    choice = input("Enter choice (1/2/3): ").strip()
    if choice == "1":
        return "BUS"
    elif choice == "2":
        return "TRAIN"
    elif choice == "3":
        return "EXIT"
    else:
        print("[Error] Invalid option selected.\n")
        return select_mode()


def main():
    mode = select_mode()
    if mode == "EXIT":
        print("Thank you for using the Reservation System.")
        return

    sys = TransportSystem(mode)

    while True:
        print(f"\n=================== {mode} RESERVATION SYSTEM ===================")
        print("1. Search Available Services")
        print("2. Add New Route / Trip")
        print("3. View All Routes")
        print("4. Register Passenger")
        print("5. Book Ticket")
        print("6. View Booked Ticket")
        print("7. Switch Mode / Exit")

        choice = input("Select Menu Option: ").strip()

        if choice == "1":
            sys.search_available_services()
        elif choice == "2":
            sys.add_new_route()
        elif choice == "3":
            sys.view_all_trips()
        elif choice == "4":
            sys.register_passenger()
        elif choice == "5":
            sys.book_ticket()
        elif choice == "6":
            sys.display_booking_details()
        elif choice == "7":
            sys.save_data()
            print("Session saved. Returning to platform selector...\n")
            main()
            break
        else:
            print("[Error] Invalid Option.")


if __name__ == "__main__":
    main()
    