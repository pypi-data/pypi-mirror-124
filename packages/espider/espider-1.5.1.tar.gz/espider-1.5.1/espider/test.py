from espider import Spider, SpiderManager

f = open('./test.txt', 'a+')


def write(S):
    s, data = S
    f.write('{}\n'.format(s.__class__.__name__))
    print(data)


class Wall(Spider):

    def prepare(self):
        # self.RESPONSE_MIDDLEWARES =
        # self.REQUEST_MIDDLEWARES = []
        # self.ITEM_PIPELINES.extend([pi, pi2])
        # self.RESPONSE_MIDDLEWARES = [lambda x: time.sleep(1)]
        # self.REQUEST_BATCH_SIZE = 0
        # raise Exception('Prepare')
        self.ITEM_PIPELINES = write
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'
        for i in range(1, 10):
            yield self.request(url.format(i))

    def parse(self, response, *args, **kwargs):
        urls = response.xpath('//a[@class="pic"]/img/@src').getall()
        for i in urls:
            yield self.request(i, callback=self.level_1)

    def level_1(self, response, *args, **kwargs):
        yield self, response

    def close(self):
        pass


class Wall2(Spider):

    def prepare(self):
        # self.RESPONSE_MIDDLEWARES =
        # self.REQUEST_MIDDLEWARES = []
        # self.ITEM_PIPELINES.extend([pi, pi2])
        # self.RESPONSE_MIDDLEWARES = [lambda x: time.sleep(1)]
        # self.REQUEST_BATCH_SIZE = 0
        # raise Exception('Prepare')
        self.ITEM_PIPELINES = write
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'
        for i in range(10, 20):
            yield self.request(url.format(i))

    def parse(self, response, *args, **kwargs):
        urls = response.xpath('//a[@class="pic"]/img/@src').getall()
        for i in urls:
            yield self.request(i, callback=self.level_1)

    def level_1(self, response, *args, **kwargs):
        yield self, response

    def close(self):
        pass


sm = SpiderManager()
sm.add(Wall)
sm.add(Wall2)
sm.start()

f.close()

# w = Wall()
# w.start()