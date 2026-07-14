import logging

from .models import Item, Order
from .forms import ItemForm
from .serializers import ItemSerializer, OrderSerializer
from .permissions import IsOwnerOrReadOnly

from django.core.paginator import Paginator
from django.urls import reverse_lazy #classic reverse but with success_url
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# ------ VIEWSETS ------

# Creates URLs automatically
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # filterset_fields = ['item_name', 'item_price']
    # ordering_fields = ['item_name', 'item_price']
    search_fields = ['item_name', 'item_desc']

    # def perform_create(self, serializer):
    #     serializer.save(user_name=self.request.user)


# ------ GENERICS ------
#
# class ItemListCreateAPI(generics.ListCreateAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#
# class ItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer


# ------ CLASS BASED VIEW ------
#
# class ItemListAPIView(APIView):
#     @staticmethod
#     def get(request):
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @staticmethod
#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ItemDetailAPIView(APIView):
#     @staticmethod
#     def get_object(pk):
#         try:
#             return Item.objects.get(pk=pk)
#         except Item.DoesNotExist:
#             return None
#
#     def get(self, request, pk):
#         item = self.get_object(pk)
#         if not item:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ItemSerializer(item)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         item = self.get_object(pk)
#         if not item:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ItemSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         item = self.get_object(pk)
#         if not item:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         item.delete()
#         return Response(status=status.HTTP_200_OK)


# ------ FUNCTION BASED VIEW ------
#
# @api_view(['GET', 'POST'])
# def item_list_api(request):
#     if request.method == 'GET':
#         items = Item.objects.all()
#         serializer = ItemSerializer(items, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ItemSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#     return None
#
# @api_view(['GET','PUT','DELETE'])
# def item_detail_api(request, pk): #for a single item
#     item = get_object_or_404(Item, pk=pk)
#
#     if request.method == 'GET':
#         serializer = ItemSerializer(item, many=False)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ItemSerializer(item, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == 'DELETE':
#         item.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     return None


#@login_required
def index(request):
    #Getting items from the database
    logger.info("Fetching all items from the database")
    logger.info(f"At [{timezone.now().isoformat()}] user {request.user} requested item list from {request.META.get('REMOTE_ADDR')}")
    item_list = Item.objects.all() #returns Queryset
    logger.debug(f"Found {item_list.count()} items")
    paginator = Paginator(item_list, 5) #now we have only 5 items per webpage
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #Passing the template to the render method
    return render(request, 'foodapp/index.html', {'page_obj': page_obj})

#Generic List Class from Django
class IndexClassView(ListView):
    model = Item
    template_name = 'foodapp/index.html'
    context_object_name = 'item_list'

def detail(request,id):
    logger.info(f"Fetching item with id {id}")
    try:
        item = get_object_or_404(Item, pk=id) #pk = primary key
        logger.debug(f"Item found {item.item_name} ($ {item.item_price})")
    except Exception as e:
        logger.error("Error fetching the item %s: %s", id, e)
        raise e
    return render(request, 'foodapp/detail.html', {'item': item})

# class DetailClassView(DetailView):
#     model = Item
#     template_name = 'foodapp/detail.html'
#     context_object_name = 'item'

#----CRUD_OPERATIONS----

def create_item(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('foodapp:index')
    contex = {'form': form}
    return render(request,'foodapp/item-form.html', contex)

# class ItemCreateView(CreateView):
#     #it tries to find *model*_form.html -> model = Item -> item_form.html; model = Food -> food_form.html
#     model = Item
#     fields = ['item_name', 'item_desc', 'item_price', 'item_image']
#     def form_valid(self, form):
#         form.instance.user_name = self.request.user
#         return super().form_valid(form)


# def update_item(request,id):
#     item = Item.objects.get(pk=id)
#     form = ItemForm(request.POST or None, instance=item)
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('foodapp:index')
#     return render(request,'foodapp/item-form.html', {'form': form})

class ItemUpdateView(UpdateView):
    model = Item
    fields = ['item_name', 'item_desc', 'item_price', 'item_image']
    template_name_suffix = '_update_form' # -> item_update_form.html due to model = Item
    def get_queryset(self):
        return Item.objects.filter(user_name=self.request.user)

# def delete_item(request,id):
#     item = Item.objects.get(pk=id)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('foodapp:index')
#     return render(request, 'foodapp/item-delete.html')

class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('foodapp:index')


def get_objects(request):
    items = Item.objects.only('item_name')
    for item in items:
        print(item.user_name)

