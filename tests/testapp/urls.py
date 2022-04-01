from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from newsletter_subscription.backend import ModelBackend
from newsletter_subscription.urls import newsletter_subscriptions_urlpatterns

from .models import Subscription


admin.autodiscover()


class TestModelBackend(ModelBackend):
    def subscription_details_form(self, email, request):
        form = super().subscription_details_form(email, request)

        if not form.instance or not form.instance.is_active:
            return None

        # We do not want more informations about people with '42' in their
        # email address. Why? To test the code path where this method does not
        # return a form.
        if "42" in form.instance.email:
            return None

        return form


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "newsletter/",
        include(
            newsletter_subscriptions_urlpatterns(
                backend=TestModelBackend(Subscription),
            )
        ),
    ),
] + staticfiles_urlpatterns()
