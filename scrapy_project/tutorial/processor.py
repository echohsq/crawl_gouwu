from scrapy.loader.processors import Join, MapCompose, SelectJmes, TakeFirst, Compose
# TakeFirst 返回列表的第一个非空值，类似 extract_first () 的功能，常用作 Output Processor
processor = TakeFirst()
print(processor(['', 1, 2, 3, 4]))
processor = Join()
print(processor(['one', 'two', 'three']))
processor = Join(',')
print(processor(['one', 'two', 'three']))
processor = Compose(str.upper, lambda s: s.strip())
print(processor(' hello world'))
processor = MapCompose(str.upper, lambda s: s.strip())
print(processor(['hello', 'python']))
# 通过json中的key来获得value
processor = SelectJmes('foo')
print(processor({'foo': 'bar'}))