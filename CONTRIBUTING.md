# 贡献指南

感谢你考虑为 WorldQuant Factor Optimizer 项目做出贡献！

## 🚀 如何贡献

### 报告 Bug

如果你发现了一个 bug，请：

1. 检查现有的 [Issues](https://github.com/your-username/worldquant-factor-optimizer/issues) 是否已经报告
2. 如果没有，创建一个新的 Issue
3. 使用 Bug 报告模板，并提供以下信息：
   - 详细的 bug 描述
   - 重现步骤
   - 预期行为 vs 实际行为
   - 环境信息（操作系统、Python 版本等）
   - 错误日志或截图

### 请求新功能

如果你想要新功能：

1. 检查现有的 [Issues](https://github.com/your-username/worldquant-factor-optimizer/issues) 是否已经提出
2. 如果没有，创建一个新的 Issue
3. 使用功能请求模板，并描述：
   - 你希望看到的功能
   - 为什么需要这个功能
   - 你希望如何实现（如果有想法的话）

### 提交代码

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📋 开发环境设置

1. 克隆你的 fork：
```bash
git clone https://github.com/your-username/worldquant-factor-optimizer.git
cd worldquant-factor-optimizer
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
```

3. 安装开发依赖：
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果存在的话
```

4. 安装预提交钩子（可选）：
```bash
pre-commit install
```

## 🧪 测试

在提交代码之前，请确保：

1. 所有测试都通过：
```bash
python -m pytest
```

2. 代码符合风格指南：
```bash
flake8 .
black .
isort .
```

3. 类型检查通过：
```bash
mypy .
```

## 📝 代码风格

我们使用以下工具来保持代码质量：

- **Black**: 代码格式化
- **isort**: import 语句排序
- **flake8**: 代码风格检查
- **mypy**: 类型检查

### Python 代码风格

- 遵循 PEP 8 风格指南
- 使用类型提示
- 编写文档字符串
- 保持函数简洁（不超过 50 行）
- 使用有意义的变量和函数名

### 提交信息格式

使用清晰的提交信息：

```
类型(范围): 简短描述

详细描述（如果需要）

相关问题: #123
```

类型包括：
- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 文档更新
- `style`: 代码风格更改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 🔍 代码审查

所有 Pull Request 都需要通过代码审查：

1. 确保 CI 检查通过
2. 代码审查者会检查：
   - 代码质量和风格
   - 功能正确性
   - 测试覆盖率
   - 文档完整性

3. 根据反馈进行必要的修改

## 📚 文档

如果你添加了新功能，请：

1. 更新 README.md（如果需要）
2. 添加代码注释和文档字符串
3. 更新相关的示例代码

## 🆘 需要帮助？

如果你在贡献过程中遇到问题：

1. 查看现有的文档
2. 搜索现有的 Issues 和 Discussions
3. 创建一个新的 Issue 寻求帮助

## 🎉 致谢

所有贡献者都会被列在项目的贡献者列表中。感谢你的贡献！

---

再次感谢你为 WorldQuant Factor Optimizer 项目做出贡献！
