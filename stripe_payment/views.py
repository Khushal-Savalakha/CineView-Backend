from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
import stripe
from django.conf import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.views.decorators.csrf import csrf_exempt
from BookingDetails.models import BookingData
from SeatDetails.models import MovieAvailability

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@csrf_exempt
def create_checkout_session(request):
    try:
        data = request.data
        email = data.get('email')
        movie_name = data.get('movie_name')
        date = data.get('date')
        time_slot = data.get('time_slot')
        seat_number = data.get('seat_number')
        amount = int(data.get('amount'))
        seat_status = data.get('seat_status')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f'Movie Ticket: {movie_name}',
                        'description': f'Seats: {seat_number}, Date: {date}, Time Slot: {time_slot}',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/stripe/success/') + 
                f'?email={email}&movie_name={movie_name}&date={date}&time_slot={time_slot}&seat_number={seat_number}&amount={amount}',
            cancel_url=request.build_absolute_uri('/stripe/cancel/')
        )
        return Response({'id': session.id, 'url': session.url})
    except Exception as e:
        return Response({
            'error': str(e),
            'detail': 'Failed to create checkout session'
        }, status=400)

@api_view(['GET'])
def success_page(request):
    try:
        email = request.GET.get('email')
        movie_name = request.GET.get('movie_name')
        date = request.GET.get('date')
        time_slot = request.GET.get('time_slot')
        seat_number = request.GET.get('seat_number')
        amount = int(request.GET.get('amount', 0)) // 100

        # Update seat status
        movie_availability = MovieAvailability.objects.get(
            movie_name=movie_name,
            date=date,
            time_slot=time_slot
        )
        
        seat_status_list = movie_availability.seat_status.split(',')
        selected_seats = seat_number.split(',')
        
        # Mark selected seats as booked
        for seat in selected_seats:
            seat_index = int(seat) - 1
            seat_status_list[seat_index] = '0'
        
        movie_availability.seat_status = ','.join(seat_status_list)
        movie_availability.save()

        # Create booking record
        BookingData.objects.create(
            email=email,
            movie_name=movie_name,
            date=date,
            time_slot=time_slot,
            seat_number=seat_number,
            amount=amount
        )

        context = {
            'email': email,
            'movie_name': movie_name,
            'date': date,
            'time_slot': time_slot,
            'seat_number': seat_number,
            'amount': amount,
            'frontend_url': settings.FRONTEND_URL
        }
        return render(request, 'stripe_payment/success.html', context)

    except Exception as e:
        return render(request, 'stripe_payment/error.html', {
            'error_message': str(e),
            'frontend_url': settings.FRONTEND_URL
        })

@api_view(['GET'])
def payment_cancel(request):
    return redirect(settings.FRONTEND_URL)

@api_view(['GET'])
def download_ticket(request):
    try:
        email = request.GET.get('email')
        movie_name = request.GET.get('movie_name')
        date = request.GET.get('date')
        time_slot = request.GET.get('time_slot')
        seat_number = request.GET.get('seat_number')
        amount = request.GET.get('amount')

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, 750, "Movie Ticket")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, 700, f"Movie: {movie_name}")
        p.drawString(50, 680, f"Date: {date}")
        p.drawString(50, 660, f"Time: {time_slot}")
        p.drawString(50, 640, f"Seats: {seat_number}")
        p.drawString(50, 620, f"Amount: ₹{amount}")
        p.drawString(50, 600, f"Email: {email}")
        
        p.save()
        buffer.seek(0)
        
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f'ticket_{movie_name}_{date}.pdf'
        )

    except Exception as e:
        return Response({'error': 'Failed to generate ticket'}, status=500)