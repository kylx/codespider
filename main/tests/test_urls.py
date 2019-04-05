from django.urls import reverse, NoReverseMatch
import pytest
from main import views

class TestViews:
    def test_home(self):
        assert functionExists(views, 'home')
    def test_rooms(self):
        assert functionExists(views, 'rooms')
    def test_patients(self):
        assert functionExists(views, 'patients')
    def test_summary(self):
        assert functionExists(views, 'summary')
    def test_inquiry(self):
        assert functionExists(views, 'inquiry')

@pytest.mark.incremental
class TestHome:
    def test_name_exists(self):
        assert urlExists('home')
    def test_url_path(self):
        assert reverse('home') == '/home'

@pytest.mark.incremental
class TestPatients:
    def test_name_exists(self):
        assert urlExists('patients') 
    def test_url_path(self):
        assert reverse('patients') == '/patients'

@pytest.mark.incremental
class TestSummary:
    def test_name_exists(self):
        assert urlExists('summary') 
    def test_url_path(self):
        assert reverse('summary') == '/summary'

@pytest.mark.incremental
class TestInquiry:
    def test_name_exists(self):
        assert urlExists('inquiry') 
    def test_url_path(self):
        assert reverse('inquiry') == '/inquiry'
    

def functionExists(view_name, view_function):
    return callable(getattr(view_name, view_function, None))

def urlExists(name):
    __tracebackhide__ = True
    try:
        reverse(name)
        return True
    except NoReverseMatch:
        pytest.fail("Named url not found: %s" % name)
        return False
    