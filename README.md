## drf实现前后端分离
#### 在django2.2 python3.7下进行的开发，修改了一点源码
#### 其中支付功能 还有  sentry 监控bug 没有完善。
#### 依赖包无法安装时就下载轮子
#### python 组件地址https://www.lfd.uci.edu/~gohlke/pythonlibs/

### 需要注意的点有：
  ```
  1  parser 解析器    上传视频 图片  文件 会自动识别
  MultiPartParser 
  解析多部分HTML表单内容，支持文件上载multipart/form-data
  2 信号量的问题 这个东西没必要 不是很方便写自己的逻辑。
  3 可能会遇到xadmin 报错 
  编辑xadmin/views/dashboard.py #render() got an unexpected keyword argument 'renderer' 37 #修改bug, 添加renderer 38   
  def render(self, name, value, attrs=None, renderer=None):
  4 跨域问题  pip install django-cors-header
    INSTALLED_APPS = ( ... 'corsheaders', ... )
    中间件放在首位 
    MIDDLEWARE = [
        ... 
      'corsheaders.middleware.CorsMiddleware', 
      'django.middleware.common.CommonMiddleware',
      ..]
   5 验证方式  使用JWT
   6 第三方登录 oauth2
   7 缓存 pip install drf-extensions
   https://python-social-auth.readthedocs.io/en/latest/configuration/settings.html
  ``` 
