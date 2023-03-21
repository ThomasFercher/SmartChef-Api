from dataclasses import dataclass
from bson import ObjectId


@dataclass
class User:
    id: str
    email: str
    password: str
    isAdmin: bool
    isVerified: bool

    def from_dict(source):
        user = User(
            str(source["_id"]),
            source["email"],
            source["password"],
            source["isAdmin"],
            source["isVerified"],
        )
        return user

    def to_json(self, include_id=True):
        if include_id:
            return {
                "_id": ObjectId(self.id),
                "email": self.email,
                "password": self.password,
                "isAdmin": self.isAdmin,
                "isVerified": self.isVerified,
            }
        else:
            return {
                "email": self.email,
                "password": self.password,
                "isAdmin": self.isAdmin,
                "isVerified": self.isVerified,
            }
