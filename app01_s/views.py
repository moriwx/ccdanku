from django.shortcuts import render
from app01_s import models
from django.http import HttpResponse
from django.views.decorators import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import Form, fields, widgets
from django.db.models import Q

def index(request):
    return render(request, "index.html", {'num': models.words.objects.count()})

def multisearch(request):
    if request.method == 'GET':
        return render(request, "multisearch.html", {'keys': [], 'total_n': 0, 'rpage': range(0), 'total_p': 1, 'iperp': 0})
    if request.method == 'POST':
        words = request.POST.get('words')
        meaning = request.POST.get('meaning')  # 义项
        pronunciation = request.POST.get('pronunciation')
        sample_sentence = request.POST.get('sample_sentence')
        remarks = request.POST.get('remarks')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        dialect_area = request.POST.get('dialect_area')
        sub_dialect_area = request.POST.get('sub_dialect_area')
        dialect_field = request.POST.get('dialect_field')
        sub_dialect_field = request.POST.get('sub_dialect_field')
        ref_source = request.POST.get('ref_source')
        iperp = request.POST.get('iperp')  # 每页条目数
        
    # 地区查询
    location_dict = {}
    if province: location_dict['province'] = province
    if city: location_dict['city'] = city
    if county: location_dict['county'] = county
    # 多条件查询 关键点在这个位置传入的字典前面一定要加上两个星号.
    locations = models.location.objects.filter(**location_dict)
    location_id = [location_.id_label for location_ in locations]

    # 参考文献查询
    refs = models.reference.objects.filter(ref__contains=ref_source)
    ref_id = [ref_.id_label for ref_ in refs]   

    user_order_info = models.words.objects.filter(words__contains=words) \
                .filter(meaning__contains=meaning).filter(pronunciation__contains=pronunciation) \
                .filter(county_number__in=location_id).filter(ref_source__in=ref_id) \
                .filter(dialect_area__contains=dialect_area).filter(sub_dialect_area__contains=sub_dialect_area) \
                .filter(dialect_field__contains=dialect_field).filter(sub_dialect_field__contains=sub_dialect_field) \
                .filter(sample_sentence__contains=sample_sentence).filter(remarks__contains=remarks).order_by('lenwords')

    # user.county_number.number.longitude 表示经度, user.county_number.number.latitude 表示纬度. 
        
    # 统计结果
    total_number = user_order_info.count()
    ppp = Paginator(user_order_info, iperp)
    user_order = []
    for i in range(ppp.num_pages):
        user_order.append(ppp.page(i+1))
    return render(request, "multisearch.html", {'keys': user_order, 'total_n': total_number, 'rpage': range(ppp.num_pages), 'total_p': ppp.num_pages, 'iperp': iperp})

def daohang(request):
    bv = ['大','小','粗','细','长','短','高','低','矮','远','近','深','浅','肥','瘦','胖',
          '黑','白','红','黄','蓝','绿','紫','灰','多','少','重','轻','直','陡','弯','歪',
          '厚','薄','稠','稀','密','亮','热','暖和','凉','冷','干','湿','干净','脏','快','钝',
          '慢','早','晚','老','年轻','软','硬','热闹','香','好','老实','大方','小气','宽','窄','圆']
    if request.GET.get('q') is not None and request.GET.get('q') in bv:
        q = request.GET.get('q')
        iperp = 20
        user_order_info = models.words.objects.filter(Q(meaning__exact=q) | (Q(meaning__exact='')&Q(words__contains=q) & (Q(lenwords__in=[3*len(q), 3*len(q)+2, 3*len(q)+4]) | (Q(words__contains='⁼')&Q(lenwords__in=[3*len(q)+3, 3*len(q)+5, 3*len(q)+7])) )))
        # 统计结果
        total_number = user_order_info.count()
        ppp = Paginator(user_order_info, iperp)
        user_order = []
        for i in range(ppp.num_pages):
            user_order.append(ppp.page(i+1))
        return render(request, "daohang.html", {'keys': user_order, 'total_n': total_number, 'rpage': range(ppp.num_pages), 'total_p': ppp.num_pages, 'iperp': iperp})
    else:
        return render(request, "daohang.html", {'keys': [], 'total_n': 0, 'rpage': range(0), 'total_p': 1, 'iperp': 0})

def info(request):
    return render(request, "info.html")

def bmap(request):
    return render(request, "map.html")

def p_map(request):
    provinces = ['河北省','山西省','辽宁省','吉林省','黑龙江省','江苏省','浙江省','安徽省','福建省','江西省','山东省','河南省','湖北省','湖南省','广东省','海南省','四川省','贵州省','云南省','陕西省','甘肃省','青海省','台湾省','内蒙古自治区','广西壮族自治区','西藏自治区','宁夏回族自治区','新疆维吾尔自治区','北京市','天津市','上海市','重庆市','香港特别行政区','澳门特别行政区']
    data = []
    for province in provinces:
        location_dict = {}
        location_dict['province'] = province
        locations = models.location.objects.filter(**location_dict)
        location_id = [location_.id_label for location_ in locations]
        p_num = models.words.objects.filter(county_number__in=location_id).count()
        place = models.long_and_lati.objects.filter(county=province)
        p_data = [place[0].longitude, place[0].latitude, province, p_num]
        data.append(p_data)
    return render(request, "p_map.html", {'data': data, 'range': range(len(provinces))})

# def word_search(request):
#     ctx = {}
#     if request.POST:
#         word = models.words.objects.filter(words=request.POST['q'])[0]
#         ctx['word'] = word.words
#         ctx['meaning'] = word.meaning
#         ctx['province'] = word.county_number.province
#         ctx['county'] = word.county_number.county
#     return render(request, "search-post.html", ctx)
class TestForm(Form):
    inp1 = fields.CharField(min_length=1, max_length=82)

def word_search(request):
    ctx = {}
    if request.method == 'GET':
        obj = TestForm()
        return render(request, 'search-post.html', {'obj': obj, 'ctx': ctx})
    else :
        obj = TestForm(request.POST)
        ctx['word'] = '南'
        ctx['meaning'] = '开'
        ctx['province'] = '大'
        ctx['county'] = '学'
#         word = models.words.objects.filter(words=request.POST['q'])[0]
#         ctx['word'] = word.words
#         ctx['meaning'] = word.meaning
#         ctx['province'] = word.county_number.province
#         ctx['county'] = word.county_number.county
    return render(request, "search-post.html", {'obj': obj, 'ctx': ctx})