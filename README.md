<div align="center">

# chat-E-AI

<p align="center">
  <a href="./README.md">简体中文</a>
</p>

chat-E-AI 是一款聊天机器人，具有嵌入人工智能（AI）的特点。它能将AI嵌入你的聊天频道，使你和你朋友更能够像和其他人聊天一样，来获取AI的问答响应。

</div>

<p align="center">
  <a href="#-面向开发者">
    <img height="21" src="https://img.shields.io/badge/面向开发者-7d09f1?style=flat-square&logo=xcode&logoColor=ffffff" alt="development">
  </a>
  <a href="#-类似项目">
    <img height="21" src="https://img.shields.io/badge/类似项目-%23d4eaf7?style=flat-square" alt="project">
  </a>
  <a href="https://github.com/garinops/chat-E-AI/blob/main/LICENSE">
    <img height="21" src="https://img.shields.io/badge/license-MIT-ffffff?style=flat-square&labelColor=7d09f1&color=%23d4eaf7" alt="license">
  </a>
</p>

<div align="center">

|                                    |                                    |
| ---------------------------------- | ---------------------------------- |
| ![Demo](./.github/imgs/intro1.png) | ![Demo](./.github/imgs/intro2.png) |


</div>

## 🛸 项目部署
### 第一步：克隆项目源代码
  ```shell
  git clone https://github.com/garinasset/chat-E-AI.git
  ```
  ```shell
  cd chat-E-AI
  ```
### 第二步：安装Python
- **Python3.10或更高。**
- **配置Python venv虚拟环境（可选，强烈建议！）[阅读venv虚拟环境](https://docs.python.org/zh-cn/3/library/venv.html)。**
  - 创建venv虚拟环境，以Python3.10为例。
    ```
    python3.10 -m venv venv-chat-E-AI
    ```
  - 激活venv虚拟环境（Linux\Unix\MacOS）注意，Windows有所不同。
    ```
    source venv-chat-E-AI/bin/activate
    ```
- **安装chat-E-AI项目依赖**
  ```shell
  pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```
### 第三步：编辑配置文件，以嵌入"OpenAI"为例：
- **找到配置文件/config/settings-example.py，复制并命名为settings.py，保存在/config文件夹下**
- **编辑/config/settings.py，设置OpenAI API Key（最小配置）**
  ```python
  OPENAI_API_KEYS = ["你的Key"]
  ```
- **其他根据需要配置，参阅settings.py的注释说明（可选）**

### 第四步：运行项目，开始和AI进行第一次对话，以接入"个人微信"为例：
- **运行程序**
  ```
  python main.py
  ```
- **在终端，使用微信扫描终端上的二维码，登录微信。**
- **给文件传输助手发送信息，或让你的朋友给你发送以"AI"开头的任何问题，等待回复。**
  > 注：默认回复"AI"开头的消息以及群聊@你的消息，你可以在/config/settings.py中设置为其他字符串，或者设置为空字符串“”以回复所有信息。
### 第五步：配置后台运行、开机启动。（可选）
- **以使用systemctl系统管理程序的Linux系统ubuntu为例：**
  - 创建系统管理服务配置
  ```shell
  sudo nano /lib/systemd/system/chat-E-AI.service
  ```
  - ***配置示例***
  ```config
  [Unit]
  Description=Daemon for chat-E-AI Demo Application
  After=network.target

  [Service]
  User=ubuntu
  Group=ubuntu
  
  WorkingDirectory=/home/ubuntu/chat-E-AI/
  ExecStart=/home/ubuntu/chat-E-AI/venv-chat-E-AI/bin/python main.py

  [Install]
  WantedBy=multi-user.target
  ```
  - 生效配置
  ```shell
  sudo systemctl daemon-reload
  ```
  - 运行chat-E-AI服务
  ```shell
  sudo systemctl start chat-E-AI.service
  ```
  - 登录
  ```shell
  journalctl -u chat-E-AI.service -n 50
  ```
  - 检查chat-E-AI服务运行状态
  ```shell
  sudo systemctl status chat-E-AI.service
  ```
  - ***配置开机启动（如果需要）***
  ```shell
  sudo systemctl enable chat-E-AI.service
  ```

<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>

## 💡 功能

`1` 即时通讯支持
   - [x] 个人微信 - 基于itchat
   - [ ] 企业微信
   - [ ] 微信公众号
   - [ ] 钉钉
   - [ ] 飞书

`2` AI支持
   - [x] OpenAI
   - [ ] 文心一言
   - [ ] 讯飞星火

`3` 超级命令
  - [x] #系统提示
  - [x] #账单查询
  - [x] #恢复出厂
  
`4` OpenAI
   - [x] 文本完成
   - [x] tools-天气联网 - 基于wttr.in
   - [x] tools-宏微观经济数据库 - 基于嘉林数据 
   - [x] tools-时间 - 基于本地
   - [x] tools-股票 - 基于xueqiu.com｜pysnowball
   - [ ] 图片生成
   - [ ] 语音翻译
   - [ ] 语音生成
   - [x] features - Keys池，随机策略，简单负载均衡
   - [x] features - Rate limits，自动回退

<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>

## 👨‍💻 面向开发者

- **嵌入其他AI**
- **嵌入其他即时通讯**
- **OpenAI tools开发**
  > 通过OpenAI的工具函数功能（tools），开发者能进一步拓展GPT的能力，比如联网获取实时信息，与第三方应用互动等。
  - 参照"chat-E-AI/ai/openai/tools/TOOL_TIME.py"这个时间工具，你可以轻松开发其他插件。
  - tools工具已经在openai Chat接口实现集成，你不必处理请求细节，只需要专注定义自己的插件工具，以及你的API调用即可。
  - 注意开发规范。
- **OpenAI 模型添加**
  > 项目已OpenAI几个常用封装模型为字典，可贡献补充其他模型。
  - 编辑chat-E-AI/ai/openai/assets/models.py
  - 按文档规范，贡献补充其他模型。
  

<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>

## 🏘️ 社区交流群

添加 wx 小助手加入：

![](https://garinasset.com/images/WX.png)

<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>


<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>

[//]: # (## 👀 其他)

[//]: # (## 🌿 第三方生态)

## 🤝 参与贡献

我们非常欢迎各种形式的贡献。如果你对贡献代码感兴趣，可以大展身手，向项目贡献你的伟大能力。

<a href="https://github.com/garinops/chat-E-AI/graphs/contributors" target="_blank">
<table>
  <tr>
    <th colspan="2">
      <br><img src="https://contrib.rocks/image?repo=garinops/chat-E-AI"><br><br>
    </th>
  </tr>

  <tr>
    <td rowspan="2">
        <picture>
          <source media="(prefers-color-scheme: dark)"
          srcset="https://next.ossinsight.io/widgets/official/analyze-repo-pushes-and-commits-per-month/thumbnail.png?repo_id=732435359&image_size=auto&color_scheme=dark">
          <img alt="Pushes and Commits of garinops/chat-E-AI"
          src="https://next.ossinsight.io/widgets/official/analyze-repo-pushes-and-commits-per-month/thumbnail.png?repo_id=732435359&image_size=auto&color_scheme=light">
        </picture>
    </td>
  </tr>

</table>
</a>

<a href="#readme">
    <img src="https://img.shields.io/badge/-返回顶部-7d09f1.svg" alt="#" align="right">
</a>

## 🌟 Star History

<!-- Copy-paste in your Readme.md file -->

<a href="https://next.ossinsight.io/widgets/official/analyze-repo-stars-history?repo_id=732435359" target="_blank" style="display: block" align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://next.ossinsight.io/widgets/official/analyze-repo-stars-history/thumbnail.png?repo_id=732435359&image_size=auto&color_scheme=dark">
    <img alt="Star History of garinops/chat-E-AI" src="https://next.ossinsight.io/widgets/official/analyze-repo-stars-history/thumbnail.png?repo_id=732435359&image_size=auto&color_scheme=light">
  </picture>
</a>

<!-- Made with [OSS Insight](https://ossinsight.io/) -->

## 使用协议

本仓库遵循 [MIT License](./LICENSE)  开源协议。