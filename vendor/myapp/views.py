from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import VendorSerializer,PurchaseorderSerializer,VendorPerformanceSerializer,UserSerializer
from .models import VendorModel,PuchaseorderModel
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def getVendor(request):
    vendor = VendorModel.objects.all()
    serializer = VendorSerializer(vendor, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getVendorDetail(request, pk):
    vendor = get_object_or_404(VendorModel,vendor_code=pk)
    serializer = VendorSerializer(vendor, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addVendor(request):
    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def updateVendor(request, pk):
    vendor = get_object_or_404(VendorModel, vendor_code=pk)
    serializer = VendorSerializer(instance=vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE']) 
def deleteVendor(request, pk):
    vendor = get_object_or_404(VendorModel, vendor_code=pk)
    vendor.delete()
    return Response('Item deleted successfully')

# logic for purchase_order api
@api_view(['GET'])
def getPurchaseorder(request):
    po =PuchaseorderModel.objects.all()
    serializer = PurchaseorderSerializer(po, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPurchaseorderDetail(request, pk):
    po = get_object_or_404(PuchaseorderModel,po_number=pk)
    serializer = PurchaseorderSerializer(po, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addPurchaseorder(request):
    serializer = PurchaseorderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def updatePurchaseorder(request, pk):
    po = get_object_or_404(PuchaseorderModel, po_number=pk)
    serializer =PurchaseorderSerializer(instance=po, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE']) 
def deletePurchaseorder(request, pk):
    po = get_object_or_404(PuchaseorderModel,po_number=pk)
    po.delete()
    return Response('Item deleted successfully')
 
# logic for 

@api_view(['GET'])
def vendor_performance(request,pk):
    try:
        vendor =VendorModel.objects.get(vendor_code=pk)
    except VendorModel.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=404)
    
    # Calculate performance metrics for the vendor
    on_time_delivery_rate = vendor.calculate_on_time_delivery_rate()
    quality_rating_avg = vendor.calculate_quality_rating_avg()
    average_response_time = vendor.calculate_average_response_time()
    fulfilment_rate = vendor.calculate_fulfilment_rate()
    
    # Serialize the performance metrics
    serializer = VendorPerformanceSerializer({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfilment_rate': fulfilment_rate
    })
    
    return Response(serializer.data)

@api_view(['POST'])
def acknowledge_purchase_order(request,pk):
    try:
        purchase_order = PuchaseorderModel.objects.get(po_number=pk)
    except PuchaseorderModel.DoesNotExist:
        return Response({'error': 'Purchase order not found'}, status=404)
    
    # Update acknowledgment date
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()
    
    # Recalculate average response time for the vendor
    vendor = purchase_order.vendor
    vendor.calculate_average_response_time()
    
    return Response({'message': 'Purchase order acknowledged successfully'})


#logic for token authntication
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User,username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"NOT FOUND"},status=status.HTTP_404_NOT_FOUND)
    token,created  = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token':token.key,'user':serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token':token.key,'user':serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))