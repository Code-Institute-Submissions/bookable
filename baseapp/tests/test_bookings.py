"""PyTest Bookings"""
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import pytest
from model_bakery import baker
from baseapp.models import Company, Booking, Customer


@pytest.mark.django_db
class TestRetrieveCompany:
    """Tests to booking model"""
    def test_if_company_does_not_exists_returns_200(self, request, test_client):
        """Test creation & retriving of company"""
        response = test_client.get('/booking/no-company/')

        assert response.status_code == 200
        assert render(request, 'booking/book_company_does_not_exist.html')


    def test_if_company_exists_returns_200(self, test_client):
        """Test creation & retriving of company"""
        (phone, address) = (
            '+12223334444',
            '103 Greenwich Avenue, New York, NY, USA'
        )

        company = baker.make(Company, phone=phone, address=address)
        company_dict = company.__dict__

        response = HttpResponse(test_client\
            .get(f'/booking/{company.slug}/'), headers=company_dict
        )

        assert response.status_code == 200
        assert response.headers['id'] == str(company.id)


@pytest.mark.django_db
class TestCreateBooking:
    """Tests to booking model"""
    def test_if_booking_exists_returns_200(self, test_client):
        """Test creation & retriving of company"""
        (phone, c_phone, address) = (
            '+12223334444',
            '+13334445555',
            '103 Greenwich Avenue, New York, NY, USA'
        )

        company = baker.make(Company, phone=phone, address=address)

        customer = baker.make(Customer, phone=c_phone)
        c = customer.__dict__

        spots = 1
        first_name = c['first_name']
        last_name = c['last_name']
        email = c['email']
        c_phone = c['first_name']
        first_name = c['first_name']

        response = test_client.post(f'/booking/{company.slug}/', {
              "spots": spots,
              "date_time": datetime.now(),
              "first_name": first_name,
              "last_name": last_name,
              "email": email,
              "phone": c_phone,
              }
            )

        booking = baker.make(
          Booking,
          company_id=company.id,
          customer_id=customer.id
          )

        redirection = 'thank-you/' + str(booking.id) + '/'

        assert response.status_code == 200
        assert redirect(redirection)
