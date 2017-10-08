from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from resumeApp.pinpin.models import Country, State, City, Video,\
    UserProfile, Follower
import json

validate_url = URLValidator()


def index(request):
    return render(request, 'pinpin/index.html')


@csrf_exempt
def register_new_user(request):
    print(request.POST)
    usernames = User.objects.values_list('username', flat=True)
    emails = User.objects.values_list('email', flat=True)
    cities = City.objects.values_list('name', flat=True)

    if request.method == "POST" and request.POST['type'] == 'new_user_signup':
        username = request.POST['username'].lower()
        email = request.POST['email'].lower()
        password = request.POST['password']
        city = request.POST['city']
        state = request.POST['state'].upper()
        country = request.POST['country']
        res = {
            'type': 'new_user_signup',
            'username': username,
            'email': email,
        }
        # validate the email
        try:
            validate_email(email)
        except ValidationError:
            res['success'] = False
            res['error'] = "Invalid Email"
        else:
            if username not in usernames and email not in emails:
                new_user = User.objects.create_user(
                    username=username, email=email, password=password)
                new_user.save()

                new_user_country = Country.objects.get(name=country)
                new_user_state = State.objects.get(code=state)
                if city not in cities:
                    new_city = City(name=city, state=new_user_state,
                                    country=new_user_country)
                    new_city.save()
                    new_user_city = new_city
                else:
                    new_user_city = City.objects.get(name=city)
                new_user.userprofile.city = new_user_city
                new_user.save()
                res['success'] = True
            else:
                res['success'] = False
                res['error'] = 'username_password_existed'
        return HttpResponse(json.dumps(res), content_type='application/json')


def _get_user(email):
    ''' get user using email '''
    try:
        user = User.objects.get(email=email)
        return user.username
    except User.DoesNotExist:
        print("User doesn't exist")
        return None


@csrf_exempt
def user_login(request):
    if request.method == "POST" and request.POST['type'] == "user_login":
        print(request.POST)
        email = request.POST['email'].lower()
        password = request.POST['password']
        username = _get_user(email)
        user = authenticate(username=username, password=password)
        res = {
            'type': 'user_login',
            'email': email
        }
        if user is not None:
            if user.is_active:
                login(request, user)
                res['success'] = True
                res['username'] = username
        else:
            res['success'] = False
            res['error'] = "invalid_email_password"
        return HttpResponse(json.dumps(res), content_type='application/json')


@csrf_exempt
def save_new_video(request, username):
    if request.user.is_authenticated:
        if request.method == 'POST' and \
                request.POST['type'] == 'save_new_video':
            print("Request: ", request.POST)
            title = request.POST['title']
            link = request.POST['link']
            date = request.POST['date']
            description = request.POST['description']
            username = request.POST['username'].lower()
            user = User.objects.get(username=username)
            if user.is_active:
                res = {
                    'type': 'save_new_video',
                    'username': username,
                    'video_title': title,
                    'video_link': link,
                }
                # check if link is valid
                try:
                    validate_url(link)
                except ValidationError:
                    res['success'] = False
                    res['error'] = 'invalid_link'
                else:
                    # check if link already saved
                    user_videos = Video.objects.filter(
                        user=user).values_list('link', flat=True)
                    if link in user_videos:
                        res['success'] = False
                        res['error'] = 'duplicated_link'
                    else:
                        # save the new video
                        # Video.objects.create(user=user, title=title,
                        #                      link=link, date=date,
                        #                      description=description)
                        new_video = Video(user=user, title=title,
                                          link=link, date=date,
                                          description=description)
                        new_video.save()
                        res['success'] = True
                        res['video_db_id'] = new_video.id
                return HttpResponse(json.dumps(res),
                                    content_type='application/json')


@csrf_exempt
def get_user_videos(request, username):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == 'POST' and \
                request.POST['type'] == 'user_videos':
            user_videos = list(Video.objects.filter(
                user=request.user).values())
            res = {
                'type': 'user_videos',
                'username': request.POST['username'],
            }
            if user_videos:
                res['videos'] = user_videos,
                res['success'] = True
            else:
                res['videos'] = '{} has no videos'.format(
                    request.POST['username'])
                res['success'] = False
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                content_type='application/json')


@csrf_exempt
def delete_video(request, username):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == 'POST' and request.POST['type'] == 'delete_video':
            video_id = request.POST['video_db_id']
            video = Video.objects.get(id=video_id)
            if video.user == request.user:
                video.delete()
                res = {
                    'type': 'delete_video',
                    'success': True
                }
            else:
                res = {
                    'type': 'delete_video',
                    'success': False,
                    'error': 'invalid_user',
                }
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                content_type='application/json')


@csrf_exempt
def find_users_in_location(request, city_name):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == 'POST' and \
                request.POST['type'] == 'find_users_in_location':
            res = {
                'type': 'find_users_in_location',
                'city': city_name,
                'users': []
            }
            if City.objects.filter(name=city_name).exists():
                city = City.objects.get(name=city_name)
                user_ids = UserProfile.objects.filter(
                    city=city).values_list('user_id', flat=True)
                for i in user_ids:
                    user = User.objects.filter(
                        id=i).values('username', 'email')[0]
                    if request.user.userprofile.is_following(i):
                        print("FOLLOWING? ",
                              request.user.userprofile.is_following(i))
                        user['following'] = True
                    else:
                        user['following'] = False
                    res['users'].append(user)
            else:
                res['success'] = False
                res['error'] = 'city_not_existing'
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                content_type='application/json')


@csrf_exempt
def new_following(request, username):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == 'POST' and \
                request.POST['type'] == 'new_following':
            following_username = request.POST['following_username']
            res = {
                'type': 'new_following',
                'following_index': request.POST['following_index']
            }
            # check if the username exist
            if User.objects.filter(username=following_username).exists():
                following_user = User.objects.get(username=following_username)
                # check if already following that user
                if request.user.userprofile.is_following(following_user.id):
                    res['success'] = False
                    res['error'] = 'already_followed'
                else:
                    Follower.objects.create(
                        user=following_user, follower=request.user)
                    res['success'] = True
                return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                    content_type='application/json')


@csrf_exempt
def unfollowing(request, username):
    if request.user.is_authenticated:
        print(request.POST)
        if request.method == 'POST' and \
                request.POST['type'] == 'unfollowing':
            unfollowing_username = request.POST['unfollowing_username']
            res = {
                'type': 'unfollowing',
                'unfollowing_index': request.POST['unfollowing_index']
            }
            # check if the username exist
            if User.objects.filter(username=unfollowing_username).exists():
                unfollowing_user = User.objects.get(
                    username=unfollowing_username)
                # check if really following that user
                if request.user.userprofile.is_following(unfollowing_user.id):
                    Follower.objects.filter(user=unfollowing_user).delete()
                    res['success'] = True
                else:
                    res['success'] = False
                    res['error'] = "not_following_already"
                return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                    content_type='application/json')


@csrf_exempt
def following_feeds(request, username):
    print(request.POST)
    if request.user.is_authenticated:
        if request.method == 'POST' and \
                request.POST['type'] == 'following_feeds':
            profile = UserProfile.objects.get(user=request.user)
            following_ids = profile.get_followings()
            res = {
                'type': 'following_feeds',
                'success': True,
                'followings': [],
            }
            if following_ids:
                for i in following_ids:
                    # get user info
                    user = User.objects.filter(
                        id=i).values('username', 'email')[0]
                    # get user location
                    user_ins = User.objects.get(id=i)
                    city = user_ins.userprofile.city.name
                    user['city'] = city
                    # get user video
                    videos = list(Video.objects.filter(user=user_ins).values())
                    user['videos'] = videos
                    res['followings'].append(user)
            else:
                res['error'] = 'user_has_no_followings'
            return HttpResponse(json.dumps(res, cls=DjangoJSONEncoder),
                                content_type='application/json')
