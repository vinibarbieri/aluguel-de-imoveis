class Review:
    def __init__(self, id, reservation_id, rating, comment):
        self.id = id
        self.reservation_id = reservation_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        return {
            "id": self.id,
            "reservation_id": self.reservation_id,
            "rating": self.rating,
            "comment": self.comment
        }

    @staticmethod
    def from_dict(data):
        return Review(
            id=data["id"],
            reservation_id=data["reservation_id"],
            rating=data["rating"],
            comment=data["comment"]
        )
