从OSM 爬取 中国各行政区域边界 工具

运行：
python ChinaRegionBoundaryCrawler.py
python RelationCrawler.py


结果：
父区域ID ，区域ID，英文名，中文名，行政等级，边界坐标

ID 为0 标示顶级行政区域


注意：
爬取后检测发现有些城市某些地区关系不全，需要更具自己需要检测，目前发现 重庆 直辖市 有部分区relation丢失问题
一个城市 可能由多个 closed region 组成
