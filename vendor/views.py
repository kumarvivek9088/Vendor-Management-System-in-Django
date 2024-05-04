from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .serializers import vendorSerializer,purchaseorderSerializer
from .models import Vendors,PurchaseOrder
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from datetime import datetime
# Create your views here.
class SigninAPI(APIView):
    def post(self,request):
        """Generate the access token for api endpoints

        Parameters:
            -username (str)
            -password (str)

        Returns:
            Json contains access_token
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username,password=password)
        if user is not None:
            refersh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'access_token':str(refersh.access_token),
                "referesh_token": str(refersh)
            },status=status.HTTP_200_OK)
        else:
            return Response({"success":False,"error":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)

class TokenRefershAPI(TokenRefreshView):
    pass
class vendorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        """
        Retrieve a list of all vendors.

        Returns:
            Response: List of vendor objects.
        """
        vendor_id = kwargs.get("vendor_id")
        if vendor_id:
            instance= get_object_or_404(Vendors,id=vendor_id)
            if request.path.split('/')[-2] == "performance":
                performance_matrix = {
                    "On-time delivery": instance.on_time_delivery_rate,
                    "quality rating": instance.quality_rating_avg,
                    "response time": instance.average_response_time,
                    "fulfilment rate": instance.fulfillment_rate
                }
                return Response(performance_matrix,status=status.HTTP_200_OK)
            # print(vendor_id)
            serializer = vendorSerializer(instance)
            return Response(serializer.data,status=status.HTTP_200_OK)
        data = Vendors.objects.all()
        serializer = vendorSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def post(self,request):
        """
        Create a new vendor.

        Parameters:
            - name (str): The name of the vendor.
            - contact_details (str): Contact details of the vendor.
            - address (str): Physical address of the vendor.
            - vendor_code (str): A unique identifier for the vendor.

        Returns:
            Response: Created vendor object.
        """
        serializer = vendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"sucess":True,"data":serializer.data},status=status.HTTP_201_CREATED)
    
    
    def put(self,request,vendor_id):
        """
            Update details of a specific vendor.

            Parameters:
                - vendor_id (int): The ID of the vendor to update in url.
                - attributes to update in json.

            Returns:
                Response: JSON response indicating success or failure of the update operation.

            Raises:
                Http404: If the vendor with the specified ID does not exist.
                ValidationError: If the request data is invalid.
        """
        instance = get_object_or_404(Vendors,id=vendor_id)
        serializer = vendorSerializer(instance,data=request.data,partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
    
    def delete(self,request,vendor_id):
        """
            Delete a specific vendor.

            Parameters:
                - vendor_id (int): The ID of the vendor to delete.

            Returns:
                Response: JSON response indicating success or failure of the delete operation.

            Raises:
                Http404: If the vendor with the specified ID does not exist.
        """
        instance = get_object_or_404(Vendors,id=vendor_id)
        instance.delete()
        return Response({"sucess":True,"message":"vendor deleted successfully"},status=status.HTTP_200_OK)
        


class PurchaseOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args,**kwargs):
        """
        Retrieve details of a specific purchase order or list all purchase orders.

        Parameters:
            - args (tuple): Additional positional arguments.
            - kwargs (dict): Additional keyword arguments.

        Returns:
            Response: JSON response containing details of the specified purchase order(s).

        Raises:
            Http404: If the purchase order with the specified ID does not exist.
        """
        po_id = kwargs.get('po_id')
        if po_id:
            data = get_object_or_404(PurchaseOrder,id=po_id)
            serializer = purchaseorderSerializer(data)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        
        data = PurchaseOrder.objects.all()
        serializer = purchaseorderSerializer(data,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        """
            Create a new purchase order.

            Parameters:
                - information of purchase order in json.

            Returns:
                Response: JSON response indicating success or failure of the creation operation.

            Raises:
                ValidationError: If the request data is invalid.
        """
        if request.path.split('/')[-2] == "acknowledge":
            po_id = kwargs.get('po_id')
            instance = get_object_or_404(PurchaseOrder,id=po_id)
            instance.acknowledgment_date = datetime.now()
            instance.save()
            return Response({"success":True,"message":"Acknowledgment date updated"},status=status.HTTP_200_OK)
        serializer = purchaseorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":True,"data":serializer.data},status=status.HTTP_201_CREATED)
    
    def put(self,request,po_id):
        """
            Update details of a specific Purchase Order.

            Parameters:
                - po_id (int): The ID of the Purchase Order to update in url.
                - attributes to update in json.

            Returns:
                Response: JSON response indicating success or failure of the update operation.

            Raises:
                Http404: If the PO with the specified ID does not exist.
                ValidationError: If the request data is invalid.
        """
        instance = get_object_or_404(PurchaseOrder,id=po_id)
        serializer = purchaseorderSerializer(instance=instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success":True,"data":serializer.data},status=status.HTTP_200_OK)
    
    def delete(self,request,po_id):
        """
            Delete a specific Purchase Order.

            Parameters:
                - po_id (int): The ID of the Purchase Order to delete.

            Returns:
                Response: JSON response indicating success or failure of the delete operation.

            Raises:
                Http404: If the PO with the specified ID does not exist.
        """
        instance =get_object_or_404(PurchaseOrder,id=po_id)
        instance.delete()
        return Response({"success":True,"message":"purchase order deleted successfully"},status=status.HTTP_200_OK)
    
        
