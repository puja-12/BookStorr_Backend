import json

from book.redis_cache import RedisFunction


class RedisCrudAPI:
    key = None

    def __get_key(self, user_id):
        if self.key is None:
            raise Exception("key can not be none")
        return '%s_%s' % (self.key, user_id)

    def __init__(self, user_id=None):
        self.redis_obj = RedisFunction()
        self.r_key = self.__get_key(user_id)

    def get(self):

        data = self.redis_obj.extract(self.r_key)

        if data is None:
            return {}
        return json.loads(data)

    def create(self, payload):

        data = self.get()
        data.update({payload.get('id'): payload})
        self.redis_obj.save(self.r_key, data)

    def delete(self, pk):

        dict_ = self.get()
        if dict_.get(str(pk)):
            dict_.pop(str(pk))
            self.redis_obj.save(self.r_key, dict_)


class RedisBook(RedisCrudAPI):
    key = 'book'

    def get(self):
        data = {}
        book_keys = list(filter(lambda x: x.startswith("book_"), self.redis_obj.get_keys()))
        for i in book_keys:
            variable = json.loads(self.redis_obj.extract(i))
            data.update(**variable)

        return data


class RedisCart(RedisCrudAPI):
    key = "cart"
