from dnacentersdk.api import DNACenterAPI
from create_site import Area, create_area
from unittest.mock import Mock, patch, MagicMock
import pytest
import pytest_mock

from dnacentersdk import DNACenterAPI
dnac = DNACenterAPI()
dnac.sites.create_site = MagicMock(return_value={"executionId"})

# dnac = Mock()
area = Area

# @pytest.fixture(autouse=True)
# @patch("create_site.dnacentersdk")
def test_create_area(mocker):
    create_area(dnac, area)
    assert 4 == 3
# def test_create_area(mocker):
#     mocker.patch("main.dnacentersdk", return_value = 5)
#     create_area(dnac, area)
#     assert 4 == 3

# def test_create_area():
#     # mocker.patch("create_site.main.DNACenterAPI", return_value = 5)
#     create_area(dnac, area)
#     assert 4 == 3