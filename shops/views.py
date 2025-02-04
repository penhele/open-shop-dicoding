from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from shops.serializers import ProductSerializer
from django.http import Http404 
from .models import Product

class ProductList(APIView):
    def post(self, request):
        product = ProductSerializer(data=request.data, context={'request': request})  # Pass request context
        if product.is_valid(raise_exception=True):
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        name_query = request.GET.get('name', None)  # Mendapatkan query parameter 'name'
        # products = Product.objects.filter(is_deleted=False)
        products = Product.objects.all()

        if name_query:
            products = products.filter(name__icontains=name_query)

        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)

class ProductDetail(APIView):
    # kriteria 1
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    # kriteria 2
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    # kriteria 3
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # kriteria 4
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.is_deleted = True
        product.delete()
        return Response({"message": "Product marked as deleted."}, status=status.HTTP_204_NO_CONTENT)
