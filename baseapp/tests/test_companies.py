"""PyTest Companies"""
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
import pytest


@pytest.fixture
def create_company_info(test_client, user_client):
    """Fixture for test company info"""
    test_client.force_login(user_client)
    def do_create_company_info(info):
        return test_client.post('/company/add/', info)
    return do_create_company_info


class TestCreateCompany:
    """Test Get Company Pages"""
    def test_if_user_is_anonymous_returns_302(self, test_client):
        """Test if anonymous"""

        response = test_client.get('/company/add/')

        assert response.status_code == 302
        assert HttpResponseRedirect(reverse('home'))


    def test_if_user_is_redirected_to_error_page(self, request, create_company_info):
        """Test if render to company does not exist"""

        response = create_company_info({
            "company_name": "company_error",
            "address": "company_error_address",
            "phone": "cascascas",
            "website": "46546",
            "spots": "6",
            })

        assert response.status_code == 302
        assert render(request, 'company/form_company_not_valid.html')


    def test_if_user_is_redirected_to_pending_page(self, request, create_company_info):
        """Test if render to company pending"""

        response = create_company_info({
            "company_name": "company_test",
            "address": "103 Greenwich Avenue, New York, NY, USA",
            "phone": "+1 222-333-4444",
            "website": "https://testsite.com",
            "spots": "6",
            })

        assert response.status_code == 302
        assert render(request, 'company/pending_company.html')
