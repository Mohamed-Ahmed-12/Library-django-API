
from django.urls import path
from .views import BookView , AuthorView , SignupView , FavouriteBookView
from rest_framework_simplejwt.views import TokenObtainPairView , TokenVerifyView , TokenRefreshView

authurlspatterns = [
    path('token/obtain/', TokenObtainPairView.as_view()),# login
    path('token/verify/', TokenVerifyView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('signup/', SignupView.as_view()), 
]


urlpatterns = [
    path('books/', BookView.as_view(), name='book-list'), #fetch all books
    path('books/<int:pk>/', BookView.as_view(), name='book-detail'), # fetch a single book
    path('books/add/', BookView.as_view(), name='book-add'), # create a book
    path('books/update/<int:pk>/', BookView.as_view(), name='book-update'), # For update a book
    path('books/delete/<int:pk>/', BookView.as_view(), name='book-delete'), # For delete a book
    
    path('books/fav/', FavouriteBookView.as_view(), name='fav-books'), # fetch all favourite books and recommendation
    path('books/fav/add/<int:pk>/', FavouriteBookView.as_view(), name='fav-add'), # add fav books
    path('books/fav/delete/<int:pk>/', FavouriteBookView.as_view(), name='fav-delete'), # delete fav books

    path('authors/',AuthorView.as_view(),name='author-list'),
    path('authors/<int:pk>/',AuthorView.as_view(),name='author-detail'),
    path('authors/add/',AuthorView.as_view(),name='author-add'),
    path('authors/update/<int:pk>/',AuthorView.as_view(),name='author-update'),
    path('authors/delete/<int:pk>/',AuthorView.as_view(),name='author-delete'),
]+authurlspatterns
