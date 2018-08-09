import redis

conn = redis.Redis(host='192.168.11.137', port=6379)

conn.set('name', '張凱竣')

val = conn.get('name').decode('utf-8')

print(val)
