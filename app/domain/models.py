from enum import Enum
from pydantic import BaseModel

# Defining our Traffic Light System
class RiskLevel(Enum):
    GREEN = "safe"
    AMBER = "caution"
    RED = "danger"

# The fundamental unit of our app
class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    O_POS = "O+"
    O_NEG = "O-"
    AB_POS = "AB+"
    AB_NEG = "AB-"