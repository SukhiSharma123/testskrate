from turtle import title
from rest_framework.response import Response
from rest_framework import (
    generics, 
    permissions, 
    status, 
    )
from rest_framework.views import APIView
from .models import *
from .serializer import (
    TicketSerializer,
)
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()

class TicketAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permissions_classes = (IsAuthenticated,)

    def post(self, request):
        if self.request.user.role == 'admin':
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Message":"You are not allowed"}, status=status.HTTP_401_UNAUTHORIZED)

class TicketAPILISTView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permissions_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = Tickets.objects.all()

        status = self.request.GET.get('status')
        title = self.request.GET.get('title')
        priority = self.request.GET.get('priority')
        if status is not None:
            qs = qs.filter(
                Q(status__icontains=f'{status}')
            )
        if title is not None:
            qs = qs.filter(
                Q(title__icontains=f'{title}')
            )
        if priority is not None:
            qs = qs.filter(
                Q(priority__icontains=f'{priority}')
            )
        return qs

class markAsClosedView(generics.UpdateAPIView):
    serializer_class = TicketSerializer
    permissions_classes = (IsAuthenticated,)

    def get_serializer_context(self, *args, **kwargs):
        ticketID = self.request.data.get('ticketID')
        if Tickets.objects.filter(id=ticketID).exists():
            ticket = Tickets.objects.get(id=ticketID)
        else:
            return Response({"Message":"Tickets not found"}, status=status.HTTP_404_NOT_FOUND)
        if self.request.user.role == 'admin' or ticket.assignedTo == self.request.user:
            ticketofuser = Tickets.objects.filter(assignedTo=ticket.assignedTo)
            priority = ticket.priority
            for ticketsof in ticketofuser:
                if priority =="low":
                    if ticketsof.priority !='medium' or ticketsof.priority !='high':
                        ticket.status = 'close'
                        ticket.save()
                elif priority == 'medium':
                    if ticketsof.priority !='high':
                        ticket.status = 'close'
                        ticket.save()
                elif priority == 'high':
                    ticket.status = 'close'
                    ticket.save()
                else:
                    return Response({"Message":"A higher priority task remains to be closed"}, status=status.HTTP_403_FORBIDDEN)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({"Message":"You are not allowed"}, status=status.HTTP_401_UNAUTHORIZED)

class DeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permissions_classes = (IsAuthenticated,)

    def get_serializer_context(self, *args, **kwargs):
        if self.request.user.role == 'admin':
            ticketID = self.request.data.get('ticketID')
            if Tickets.objects.filter(id=ticketID).exists():
                ticket = Tickets.objects.get(id=ticketID)
                ticket.delete()
                return Response({"Message":"Tickets Deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"Message":"Tickets not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Message":"You are not allowed"}, status=status.HTTP_401_UNAUTHORIZED)