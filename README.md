# scrapy-github
利用scrapy爬取github上用户信息，并将数据存储于mongoDB

## 运行环境
 * Ubuntu 16.04 LTS
 * Python 3.5.2
 * scrapy 1.4.0
 * mongodb 3.6.1
 * pymongo

## 安装
scrapy安装见https://doc.scrapy.org/en/latest/intro/install.html

## 运行
在`scrapyspider`目录下，运行:
```
scrapy crawl github_user
```
如果需要中断程序，可以键入`Ctrl-C`。程序会在一小段时间后停止运行。
之后即可在mongoDB shell中查看结果：
```
> use test_database
> db.GithubUser.find()
```

## 表结构
mongoDB安装于本机，端口默认。
数据存放于`test_database`数据库，collection为`GithubUser`，其字段分别为：
 * username: 用户名
 * name: 姓名
 * url: 个人主页
 * organization: 所属单位
 * repos: 维护的仓库（内嵌表，表中字段仅有`name`）
 * followers: 粉丝（内嵌表，表中字段仅有`username`）
 * following: 关注的人（内嵌表，表中字段仅有`username`）

