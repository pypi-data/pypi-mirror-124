# Easy Sipder

---

Easy Spider 主要有四大模块：

- Spider 负责推送请求到请求线程池
- Downloader 负责启动请求与数据，请求在启动前会经过请求处理程序，响应在下载后会经过响应处理程序
- Pipeline 负责清理数据，数据的持久化等工作

流程图如下

![epsider流程图](https://ftp.bmp.ovh/imgs/2021/04/76657cd1da61f203.png)


---

# TODO

- 2020-04-06
    - [x] 修复 start_requests 错误提示
    - [x] 自动设置请求优先级
    - [x] 请求和响应扩展合并为下载中间件
    - [ ] ~~settings 像 scrapy 看齐~~


- 2020-04-07
    - [x] 优化 setting
    - [ ] 下载器开始停止问题
  
