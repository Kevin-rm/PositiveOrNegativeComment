from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from base.models import Comment


# Create your views here.
def index(request):
    if request.method == "POST":
        try:
            comment = Comment(text=request.POST.get("comment"))
            comment.clean()
            comment.generate_reply()
            comment.save()
        except ValidationError as e:
            messages.error(request, e.message)
        finally:
            return redirect("index")

    comments = Comment.objects.all()
    return render(request, "index.html", {"comments": comments})
