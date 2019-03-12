from libtera.redis.RedisProtocolFactory import RedisProtocolFactory, redisProtocol

# Twisted
from twisted.application import internet, service
from twisted.internet import reactor, ssl, defer


# Event based, twisted redis
import txredisapi as txredis

# Blocking redis
import redis

from modules.RedisModule import get_redis


class RedisClient:

    def __init__(self):
        print('Init RedisClient', self)
        self.protocol = None
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        reactor.connectTCP("localhost", 6379, RedisProtocolFactory(parent=self, protocol=redisProtocol))

    # @defer.inlineCallbacks
    # def getConnection(self):
    #    connection = yield txredis.Connection()
    #    defer.returnValue(connection)

    def redisConnectionMade(self):
        print('RedisClient connectionMade')
        pass

    def redisMessageReceived(self, pattern, channel, message):
        print('RedisClient message received', pattern, channel, message)
        pass

    def redisConnectionLost(self, reason):
        print("RedisClient lost connection", reason)
        pass

    def setProtocol(self, protocol: redisProtocol):
        print('RedisClient set protocol', protocol)
        self.protocol = protocol

    def subscribe(self, topic):
        if self.protocol:
            print('RedisClient (', self, ') subscribing to: ',  topic)
            self.protocol.psubscribe(topic)
        else:
            print('Error, no protocol')

    def publish(self, topic, message):
        self.redis.publish(topic, message)

    def redisGet(self, key):
        return self.redis.get(key)

    def redisSet(self, key, value, ex=None):
        self.redis.set(key, value, ex=ex)


# Debug
if __name__ == '__main__':
    print('Starting')

    class MyClient(RedisClient):
        def redisConnectionMade(self):
            self.subscribe('*')

    client = MyClient()

    print('setting variable')

    client.redisSet('papa', 'rien', ex=60)

    print('redis get', client.redisGet('papa'))

    print('Starting reactor')
    reactor.run()



