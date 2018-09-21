import redis

r = redis.Redis(host='localhost')

r.set('foo', 'bar')
value = r.get('foo')
print(value)