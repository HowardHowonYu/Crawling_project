# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class JobkoreaCrawlerPipeline(object):
    def process_item(self, item, spider):
        
        
        def __init__(self):
            # 변수선언은 여기서
            self.webhook_url = "https://hooks.slack.com/services/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"

            
        def send_msg(self, msg):
            
            payload = {
                "channel" : "#myworkspace",
                "username" : "article_bot",
                "icon_emoji" : ":thumbsup:",
                "text" : msg,
            }

            requests.post(self.webhook_url,json.dumps(payload))
            time.sleep(1)
            
            return item
