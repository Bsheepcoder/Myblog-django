# myblog-django-bootstrap4


##  version ：0.0.4 2023.3.3
- based on django and bootstrap4  0.0.4
##  version ：0.0.5 2023.3.15
- resovle issue about render the js by editor.md 
- 遭遇了一些安全性问题，对项目的安全性做优化
## version ：0.0.6 2023.4.15
- 修复了文章页并发访问的bug，对文章页的渲染加锁，基于目前不成熟方案的一点改进,但是导致死锁,放弃这个方案
- 通过js获取body值,渲染markdown，页面渲染还是不太好，存在字符识别不了
- 增加了文章页的滑动导航栏
