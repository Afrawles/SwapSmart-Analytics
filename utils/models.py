from dataclasses import dataclass
from enum import Enum

class Discount(Enum):
    NO = "0%"
    FIFTY = "50%"
    SEVENTYFIVE = "75%"
    HUNDRED = "100%"

@dataclass
class Client:
    client_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    status: str # active | inactive 
    registration_date: str
    update_datetime: str

@dataclass
class Battery:
    battery_id: int
    capacity: int
    status: str # active | inactive | maintenance 
    manufacture_date: str
    update_datetime: str

@dataclass
class Bike:
    bike_id: int
    client_id: int
    status: str # active  | inactive | maintenance
    purchase_datetime: str
    update_datetime: str

@dataclass
class Attendants:
    attendant_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    status: str # active  | inactive
    created_datetime: str
    update_datetime: str

@dataclass
class Station:
    """
    Charging Station
    """
    station_id: int
    station_name: str
    phone_number: str
    address: str
    status: str # active  | inactive
    created_datetime: str
    update_datetime: str

@dataclass
class Transaction:
    # transaction_id: int  
    created_datetime: str
    client_id: int
    battery_given_id: int
    battery_received_id: int
    bike_id: int
    station_id: int
    attendant_id: int
    battery_given_percentage: int
    battery_recevived_percentage: int
    battery_usage_diff: int
    discount: str
    transaction_amount: float