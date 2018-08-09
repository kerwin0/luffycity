import json
import redis
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser

from api import models
from api.utils.my_response import BaseResponse

CONN = redis.Redis(host='192.168.11.61', port=6379)

USER_ID = 1


class ShoopingCarView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):

        ret = {'code': 10000, 'data': None, 'error': None}
        try:
            shopping_car_course_list = []
            pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)

            user_key_list = CONN.keys(pattern)
            for key in user_key_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                shopping_car_course_list.append(temp)

            ret['data'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 1001
            ret['error'] = '获取购物车数据失败'

        return Response(ret)

    def create(self, request, *args, **kwargs):
        course_id = request.data.get('courseid')
        policy_id = request.data.get('policyid')

        course = models.Course.objects.filter(id=course_id).first()
        if not course:
            return Response({'code': 10001, 'error': '课程不存在'})

        price_policy_queryset = course.price_policy.all()
        price_policy_dict = {}
        for item in price_policy_queryset:
            temp = {
                'id': item.id,
                'price': item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp
        if policy_id not in price_policy_dict:
            return Response({'code': 10002, 'error': '傻×，价格策略别瞎改'})

        pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
        keys = CONN.keys(pattern)
        if keys and len(keys) >= 1000:
            return Response({'code': 10009, 'error': '购物车东西太多，先去结算再进行购买..'})

        key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'default_price_id', policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))

        return Response({'code': 10000, 'data': '购买成功'})

    def destroy(self, request, *args, **kwargs):

        response = BaseResponse()
        try:
            courseid = request.GET.get('courseid')
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid,)

            CONN.delete(key)
            response.data = '删除成功'
        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
        return Response(response.dict)

    def update(self, request, *args, **kwargs):

        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None

            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)

            if not CONN.exists(key):
                response.code = 10007
                response.error = '课程不存在'
                return Response(response.dict)

            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
            if policy_id not in price_policy_dict:
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)

            CONN.hset(key, 'default_price_id', policy_id)
            CONN.expire(key, 20 * 60)
            response.data = '修改成功'
        except Exception as e:
            response.code = 10009
            response.error = '修改失败'

        return Response(response.dict)
