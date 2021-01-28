from django.shortcuts import render, get_object_or_404
from .forms import ImageForm
import os
from django.conf import settings
from .models import Image
from PIL import Image as PILImage
from .forms import SizeForm
from django.shortcuts import redirect


def image_upload_view(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.instance.image
            image = Image.objects.filter(image=name)
            img_id = image[0].id
            return redirect('image_resize', pk=img_id)
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form})


def FilesListView(request):
    path = settings.MEDIA_ROOT+'images'
    files_list = os.listdir(path)
    return render(request, 'list.html', {'images': files_list})


def image_resize(request, pk):
    template = 'image_resize.html'
    image = get_object_or_404(Image, pk=pk)
    form = SizeForm()

    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data.get("width")
            height = form.cleaned_data.get("height")
            img_to_r = PILImage.open(image.image)
            img_width, img_height = img_to_r.size
            if not width:
                wpercent = (float(height) / float(img_height))
                width = int((float(img_width) * float(wpercent)))
            if not height or (width and height):
                hpercent = (float(width) / float(img_width))
                height = int((float(img_height) * float(hpercent)))

            context = {
                'resize': True,
                'width': width,
                'image': image,
                'height': height,
            }

            return render(request, template, context)
    context = {
        'form': form,
        'image': image,
    }
    return render(request, template, context)


def image_list_view(request):
    template = 'list.html'
    images = Image.objects.all()

    context = {
        'image_list': images,
    }

    return render(request, template, context)
