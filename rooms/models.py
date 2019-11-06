from django.db import models

from django_countries.fields import CountryField

from core import models as core_models  # 위에거랑 이름이 같으니까 이름을 지정해준다.
from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition"""

    class Meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Object Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition """

    class Meta:
        verbose_name_plural = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(
        max_length=140
    )  # 따로 blank, null을 안해준다 왜냐하면 필수적인 요소로 만들거라서 그래
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()  # date를 신경 쓸 필요 없다.
    check_out = models.TimeField()  # date를 신경 쓸 필요 없다.
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        user_models.User, related_name="rooms", on_delete=models.CASCADE
    )  # 이건 유저니까 포린키로 연결해줘야해
    room_type = models.ManyToManyField(
        "RoomType", related_name="rooms", blank=True
    )  # roomtype을 이야기할 떄 (hotel일 때) rooms를 쓰면 hotel을 쓰고있는 보든 룸을 알려준다. 이제 room_type.room_set말고 room_type.rooms를 쓸 수 있게 되는 거지
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True
    )  # 추가적으로 MtoM으로 설정되면 쿼리셋이 반대쪽에 없어도 자동으로 생김, 그래서 amenity.rooms로 하면 그 어메니티 가진 방이 보임
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        return all_ratings / len(all_reviews)

