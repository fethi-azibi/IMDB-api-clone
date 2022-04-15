from rest_framework.throttling import UserRateThrottle


class ReviewCreateThrottling(UserRateThrottle):
    # scope is a predefined var we use it in the settings
    scope = 'review-create'
