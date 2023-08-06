import os
import sys
import importlib
import likeshell
from likeshell.shell import run_cls


def load_spider_name():
    pwd = os.getcwd()
    sys.path.append(pwd)
    spider_paths = [i for i in os.walk(pwd).__next__()[1] if not i.startswith('.')]
    spider_path = f'{spider_paths[0]}.spiders'
    spider_files = [
        i for i in os.walk(spider_path.replace('.', '/')).__next__()[2] if i != '__init__.py' and i.endswith('.py')
    ]
    spider_file = spider_files[0][:-3]
    module = importlib.import_module(f'{spider_path}.{spider_file}')
    for k, v in module.__dict__.items():
        base = None
        if hasattr(v, '__base__'):
            base = v.__base__.__name__
        if isinstance(v, type) and base == 'HttpSpider':
            return v.name


class CjztCrawler(likeshell.Main):
    def crawl(self, iid, sid, env):
        spider_name = load_spider_name()
        cmd = f'scrapy crawl {spider_name} -a instance_id={iid} -a spider_id={sid} -a env={env} --logfile ./log_{iid}.log'
        os.system(cmd)


def main():
    run_cls(CjztCrawler, CjztCrawler.__dict__)
