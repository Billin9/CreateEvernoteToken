# CreateEvernoteToken

模拟登录印象笔记（Evernote），自动创建印象笔记开发者 Token ，写入 Evernote.sublime-settings 配置文件

# 依赖

- requests
- bs4
- lxml

# 配置

在项目目录下创建 config.py 文件，内容如下：

```python
name = '用户名'
pwd = '密码'
cfg = '~/Library/Application Support/Sublime Text 3/Packages/User/Evernote.sublime-settings' # 确认自己的配置路径
```

# 加入计划任务

每隔6天在中午12点执行一次

```crontab
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed

0 12 */6 * * 虚拟环境路径/python 本项目路径/createevernotetoken.py
```
