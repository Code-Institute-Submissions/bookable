"""PyTest Companies"""
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.test import Client


class TestCreateCompany:
    """Test Get Company Pages"""
    def test_if_user_is_anonymous_returns_302(self):
        """Test if anonymous"""

        client = Client()
        response = client.get('/company/add/')

        assert response.status_code == 302


    def test_if_user_is_redirected_to_error_page(self, request, user_client):
        """Test if render to company does not exist"""

        client = Client()
        client.force_login(user_client)
        response = client.post('/company/add/', {
            "company_name": "company_test",
            "address": "103 Greenwich Avenue, New York, NY, USA",
            "phone": "cascascas",
            "website": "46546",
            "spots": "6",
            })

        assert response.status_code == 302
        assert render(request, 'company/form_company_not_valid.html')


    def test_if_user_is_redirected_to_pending_page(self, request, user_client):
        """Test if render to company pending"""

        client = Client()
        client.force_login(user_client)
        response = client.post('/company/add/', {
            "company_name": "company_test",
            "address": "103 Greenwich Avenue, New York, NY, USA",
            "phone": "+1 222-333-4444",
            "website": "https://testsite.com",
            "spots": "6",
            })

        assert response.status_code == 302
        assert render(request, 'company/pending_company.html')
