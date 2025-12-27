from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import Video, Comment, Like, Subscription
from .forms import VideoUploadForm, CommentForm, RegisterForm
from .youtube_api import search_youtube_videos, format_view_count, get_video_details


def get_user_subscriptions(user):
    """Get subscriptions for sidebar display."""
    if user.is_authenticated:
        return Subscription.objects.filter(subscriber=user).select_related('channel')[:10]
    return []


def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    # Fetch YouTube videos (now with category support)
    youtube_videos = search_youtube_videos(query=query, max_results=50, category=category)
    
    # Format view counts for display
    for video in youtube_videos:
        video['formatted_views'] = format_view_count(video['view_count'])
    
    # Also get local videos
    if query:
        local_videos = Video.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        local_videos = Video.objects.all()
    
    local_videos = local_videos.annotate(like_count=Count('likes', filter=Q(likes__is_like=True)))
    
    context = {
        'youtube_videos': youtube_videos,
        'videos': local_videos,
        'query': query,
        'category': category,
        'user_subscriptions': get_user_subscriptions(request.user),
    }
    return render(request, 'core/home.html', context)


def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.views += 1
    video.save()
    
    comments = video.comments.all()
    related_videos = Video.objects.exclude(pk=pk)[:10]
    
    # Check if user liked/disliked
    user_like = None
    is_subscribed = False
    if request.user.is_authenticated:
        like_obj = Like.objects.filter(user=request.user, video=video).first()
        if like_obj:
            user_like = 'like' if like_obj.is_like else 'dislike'
        is_subscribed = Subscription.objects.filter(subscriber=request.user, channel=video.user).exists()
    
    like_count = video.likes.filter(is_like=True).count()
    dislike_count = video.likes.filter(is_like=False).count()
    subscriber_count = video.user.subscribers.count()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return redirect('video_detail', pk=pk)
    else:
        form = CommentForm()
    
    context = {
        'video': video,
        'comments': comments,
        'related_videos': related_videos,
        'form': form,
        'user_like': user_like,
        'is_subscribed': is_subscribed,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'subscriber_count': subscriber_count,
        'user_subscriptions': get_user_subscriptions(request.user),
    }
    return render(request, 'core/video_detail.html', context)


def youtube_video_detail(request, video_id):
    """View for embedded YouTube videos."""
    video = get_video_details(video_id)
    
    if not video:
        messages.error(request, 'Video not found')
        return redirect('home')
    
    # Format view count
    video['formatted_views'] = format_view_count(video.get('view_count', 0))
    
    # Get related videos (other YouTube videos)
    related_videos = search_youtube_videos(max_results=10)
    for related in related_videos:
        related['formatted_views'] = format_view_count(related.get('view_count', 0))
    
    # Filter out current video from related
    related_videos = [v for v in related_videos if v['id'] != video_id][:8]
    
    context = {
        'video': video,
        'related_videos': related_videos,
        'user_subscriptions': get_user_subscriptions(request.user),
    }
    return render(request, 'core/youtube_video_detail.html', context)



@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('home')
    else:
        form = VideoUploadForm()
    
    context = {
        'form': form,
        'user_subscriptions': get_user_subscriptions(request.user),
    }
    return render(request, 'core/upload.html', context)


@login_required
def toggle_like(request, pk):
    if request.method == 'POST':
        video = get_object_or_404(Video, pk=pk)
        action = request.POST.get('action', 'like')
        is_like = action == 'like'
        
        like_obj, created = Like.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'is_like': is_like}
        )
        
        if not created:
            if like_obj.is_like == is_like:
                like_obj.delete()
                status = 'removed'
            else:
                like_obj.is_like = is_like
                like_obj.save()
                status = 'changed'
        else:
            status = 'added'
        
        like_count = video.likes.filter(is_like=True).count()
        dislike_count = video.likes.filter(is_like=False).count()
        
        return JsonResponse({
            'status': status,
            'like_count': like_count,
            'dislike_count': dislike_count,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_subscribe(request, user_id):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        channel = get_object_or_404(User, pk=user_id)
        
        if channel == request.user:
            return JsonResponse({'error': 'Cannot subscribe to yourself'}, status=400)
        
        sub, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            channel=channel
        )
        
        if not created:
            sub.delete()
            subscribed = False
        else:
            subscribed = True
        
        subscriber_count = channel.subscribers.count()
        
        return JsonResponse({
            'subscribed': subscribed,
            'subscriber_count': subscriber_count,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def channel_view(request, user_id):
    from django.contrib.auth.models import User
    channel_user = get_object_or_404(User, pk=user_id)
    videos = Video.objects.filter(user=channel_user)
    subscriber_count = channel_user.subscribers.count()
    
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(subscriber=request.user, channel=channel_user).exists()
    
    context = {
        'channel_user': channel_user,
        'videos': videos,
        'subscriber_count': subscriber_count,
        'is_subscribed': is_subscribed,
        'user_subscriptions': get_user_subscriptions(request.user),
    }
    return render(request, 'core/channel.html', context)
