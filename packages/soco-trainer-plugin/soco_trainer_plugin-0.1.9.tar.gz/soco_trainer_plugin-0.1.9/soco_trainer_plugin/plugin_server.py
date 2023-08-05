from .core.server import Connector


class PluginServer(object):
    def __init__(self, trainer, host, port, max_batch_size, debug, param, redis_url, mongo_url):
        self.host = host
        self.port = port
        self.max_batch_size = max_batch_size
        self.debug = debug
        self.trainer = trainer
        self.param = param
        self.redis_url = redis_url
        self.mongo_url = mongo_url

    def run_server(self):
        connector = Connector(debug=self.debug,
                              trainer=self.trainer,
                              param=self.param,
                              mongo_url=self.mongo_url,
                              redis_url=self.redis_url)
        application = connector.app
        application.run(host=self.host, port=self.port)

