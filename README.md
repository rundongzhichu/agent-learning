# 大模型Agent开发学习

## 基于RAG架构开发

### RAG原理图
![rag原理图](static/RAG原理图.png)

### agent RAG流程
![RAG流程和难点](static/RAG流程和难点.png)

## 基于Agent架构开发

### agent架构
![Agent架构](static/Agent架构.png)

![Agent架构1](static/Agent架构1.png)

短期记忆： 就是类似上下文会话，文件记录的上下文，每次模型都要根据你传递的上下文进行学习思考
长期记忆: 就是通过微调大模型，让大模型自己记住相关的知识点，不用依赖上下文