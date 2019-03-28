from django.urls import reverse, NoReverseMatch
import pytest

@pytest.mark.incremental
class TestHome:
    def test_name_exists(self):
        assert urlExists('home') 
    def test_url_path(self):
        assert reverse('home') == '/home'

@pytest.mark.incremental
class TestRooms:
    def test_name_exists(self):
        assert urlExists('rooms') 
    def test_url_path(self):
        assert reverse('rooms') == '/rooms'

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

def urlExists(name):
    __tracebackhide__ = True
    try:
        reverse(name)
        return True
    except NoReverseMatch:
        pytest.fail("Named url not found: %s" % name)
        return False
    