from espider import Spider, SpiderManager


def droprsp(resp):
    if resp.url == 'https://desk-fd.zol-img.com.cn/t_s208x130c5/g5/M00/0A/04/ChMkJ1X3f2GIIXAPAASIZB7XQoEAACotAHfqiQABIh8696.jpg':
        return
    return resp


class Wall(Spider):

    def prepare(self):
        self.RESPONSE_MIDDLEWARES.append(droprsp)
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'
        for i in range(1, 10):
            yield self.request(url.format(i))
        #
        # url = 'https://www.google.com/'
        # yield self.request(url)

    def parse(self, response, *args, **kwargs):
        urls = response.xpath('//a[@class="pic"]/img/@src').getall()
        for i in urls:
            yield self.request(i, callback=self.level_1)

    def level_1(self, response, *args, **kwargs):
        yield response


class Wall2(Spider):

    def prepare(self):
        self.RESPONSE_MIDDLEWARES.append(droprsp)
        pass

    def start_requests(self):
        url = 'https://desk.zol.com.cn/fengjing/weimeiyijing/{}.html'
        for i in range(1, 10):
            yield self.request(url.format(i))
        #
        # url = 'https://www.google.com/'
        # yield self.request(url)

    def parse(self, response, *args, **kwargs):
        urls = response.xpath('//a[@class="pic"]/img/@src').getall()
        for i in urls:
            yield self.request(i, callback=self.level_1)

    def level_1(self, response, *args, **kwargs):
        yield response


spm = SpiderManager()
spm.add(Wall)
spm.start()
