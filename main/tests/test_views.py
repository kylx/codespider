# from django.test import RequestFactory
# from django.urls import reverse
# from main import views

# """
# Test for mapping from url -> views
# """
# def functionExists(view_name, view_function):
#     return callable(getattr(view_name, view_function, None))

# class TestViewExists:
#     def test_home_view_exists(self):
#         assert functionExists(views, 'home')

# class TestViews:
#     pass

#     # def test_home(self):
#     #     url = reverse('home')
#     #     assert resolve(url).view_name == 'home'

#     # def test_rooms(self):
#     #     url = reverse('rooms')
#     #     assert resolve(url).view_name == 'rooms'

#     # def test_patients(self):
#     #     url = reverse('patients')
#     #     assert resolve(url).view_name == 'patients'

#     # def test_summary(self):
#     #     url = reverse('summary')
#     #     assert resolve(url).view_name == 'summary'

#     # def test_inquiry(self):
#     #     url = reverse('inquiry')
#     #     assert resolve(url).view_name == 'inquiry'