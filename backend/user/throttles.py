from rest_framework.throttling import UserRateThrottle


class PhotoUploadThrottle(UserRateThrottle):
    rate = "5/hour"
