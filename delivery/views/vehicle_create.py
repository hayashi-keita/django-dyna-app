from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Vehicle
from ..forms import VehicleForm

class VehicleCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = VehicleForm()
        return render(request, 'delivery/vehicle_form.html', {'form': form})
    
    def post(self, request):
        form =VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('delivery:vehicle_list')
        return render(request, 'delivery/vehicle_form.html', {'form': form})

class VehicleListView(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = Vehicle.objects.all().order_by('vehicle_number')
        return render(request, 'delivery/vehicle_list.html', {'vehicles': vehicles})

class VehicleUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(instance=vehicle)
        return render(request, 'delivery/vehicle_form.html', {'form': form})
    
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('delivery:vehicle_list')
        return render(request, 'delivery/vehicle_form.html', {'form': form})

class VehicleDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        return render(request, 'delivery/vehicle_delete.html', {'vehicle': vehicle})
    
    def post(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.delete()
        return redirect('delivery:vehicle_list')