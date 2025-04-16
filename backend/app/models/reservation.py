class Reservation:
    def __init__(self, id, property_id, renter_id, start_date, end_date, approved=None):
        self.id = id
        self.property_id = property_id
        self.renter_id = renter_id
        self.start_date = start_date  # string "YYYY-MM-DD"
        self.end_date = end_date      # string "YYYY-MM-DD"
        self.approved = approved      # True, False ou None

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "renter_id": self.renter_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "approved": self.approved
        }

    @staticmethod
    def from_dict(data):
        return Reservation(
            id=data["id"],
            property_id=data["property_id"],
            renter_id=data["renter_id"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            approved=data.get("approved")
        )
