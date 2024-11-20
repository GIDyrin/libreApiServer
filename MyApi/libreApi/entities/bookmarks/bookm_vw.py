from .bookm_sz import BookmarkSerializer, Bookmarks
from rest_framework import views, generics, status
from rest_framework.response import Response


class BookmarkRUDView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Bookmarks.objects.all()
  serializer_class = BookmarkSerializer


class CreateBookmarkView(generics.CreateAPIView):
  serializer_class = BookmarkSerializer
  queryset = Bookmarks.objects.all()
  
  def create(self, request, *args, **kwargs):
    id = request.user.id
    bookmark_json = request.data
    bookmark_json["user"] = id
    serializer = self.get_serializer(data=bookmark_json)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
class UsersBookmarksView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Bookmarks.objects.filter(user=user)