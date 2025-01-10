from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Book , Author , Favorite
from .serializers import BookSerializer , AuthorSerializer , UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly , AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def get_user_from_token(token):
    try:
        # decode the access token
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        return user
    except:
        return None
    
class SignupView(APIView):
    """Take user credientials (username,email,pass) and generate tokens for a new user """
    permission_classes = (AllowAny,)     
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user
            user = serializer.save()
            # Generate token for the new user
            token_serializer = TokenObtainPairSerializer(data={
                "username": user.username, 
                "password": request.data.get("password")  # Assuming password is in the request
            })
            if token_serializer.is_valid():
                tokens = token_serializer.validated_data # save tokens
                return Response(tokens, status=status.HTTP_201_CREATED)
            else:
                return Response(token_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class BookView(APIView):
    """
    Book View
    Access token 'Bearer Token' must be in header Authorization
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk=None):
        '''
        Get List or one book
        Search about book by title or author
        '''
        if pk:
            book = get_object_or_404(Book, id=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if request.GET.get('search'):
            try:
                query = request.GET.get('search')
                books = Book.objects.filter(title__icontains=query)
                if not books.exists():
                    try:
                        author = Author.objects.get(name__icontains=query)
                        books = Book.objects.filter(author=author)
                        serializer = BookSerializer(books, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except Author.DoesNotExist:
                        return Response({"detail": "No matching books or authors found."}, status=status.HTTP_404_NOT_FOUND)
                    except:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # get all books by default
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self , request):
        '''
        Create new book
        '''
        # token = request.headers['Authorization'][7:]
        # user = get_user_from_token(token)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        '''
        Updtae a book
        '''
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk):
        '''
        Delete a book
        '''
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            raise Http404


class AuthorView(APIView):
    """
    Author View
    Access token 'Bearer Token' must be in header Authorization
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk=None):
        '''
        Get List or one author
        '''
        if pk:
            author = get_object_or_404(Author, id=pk)
            serializer = AuthorSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self , request):
        '''
        Create new author
        '''
        # token = request.headers['Authorization'][7:]
        # user = get_user_from_token(token)
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        '''
        Update an author
        '''
        try:
            author = Author.objects.get(id=pk)
            serializer = AuthorSerializer(author , data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk):
        '''
        Delete an author
        '''
        try:
            author = Author.objects.get(id=pk)
            author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            raise Http404
        

# Similarity-based recommendations
class FavouriteBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_user_favorites(self, user):
        favorite, created = Favorite.objects.get_or_create(user=user)
        return favorite
    
    def get_recommendations(self, favorite_books):
        # Implement a similarity algorithm to recommend books
        all_books = Book.objects.exclude(id__in=[book.id for book in favorite_books])
        recommended = []

        for book in all_books:
            similarity_score = self.calculate_similarity(book, favorite_books)
            recommended.append((book, similarity_score))

        # Sort by similarity score and return the top 5
        recommended = sorted(recommended, key=lambda x: x[1], reverse=True)[:5]
        return [item[0] for item in recommended]

    def calculate_similarity(self, book, favorite_books):
        """
        Calculate the best similarity score between a book and a list of favorite books.
        The similarity is based on shared genres using Jaccard similarity.
        """
        book_genres = set(book.genre.lower().split(", "))
        best_similarity = 0.0

        for fav in favorite_books:
            favorite_genres = set(fav.genre.lower().split(", "))
            
            # Jaccard similarity
            intersection = book_genres & favorite_genres
            union = book_genres | favorite_genres
            
            similarity = len(intersection) / len(union) if union else 0.0
            best_similarity = max(best_similarity, similarity)
        
        return best_similarity
    
    def get(self,request):
        # Fetch the user's favorite books and recommendations
        favorite = self.get_user_favorites(request.user)
        favorite_books = favorite.books.all()
        recommended_books = self.get_recommendations(favorite_books)

        return Response({
            "favorites": BookSerializer(favorite_books, many=True).data,
            "recommendations": BookSerializer(recommended_books, many=True).data
        })
        
    def post(self, request ,pk):
        # Add a book to the user's favorites
        book = get_object_or_404(Book, id=pk)
        favorite = self.get_user_favorites(request.user)
        favorite.books.add(book)
        return Response({"message": "Book added to favorites successfully."}, status=status.HTTP_200_OK)

    def delete(self, request ,pk):
        # Remove a book from the user's favorites
        book = get_object_or_404(Book, id=pk)
        favorite = self.get_user_favorites(request.user)
        favorite.books.remove(book)
        return Response({"message": "Book removed from favorites successfully."}, status=status.HTTP_200_OK)
