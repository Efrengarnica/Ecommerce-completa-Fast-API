from enum import Enum
class UserRole(str, Enum):
    CUSTOMER="customer"
    ADMIN="admin"
    SUPER_ADMIN="super_admin"