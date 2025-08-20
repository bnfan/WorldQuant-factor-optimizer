# WorldQuant Factor Optimizer

一个基于GPT-5的WorldQuant量化因子优化工具，使用AI技术自动生成和改进量化因子表达式。

## 🚀 功能特性

- 🤖 使用GPT-5自动生成因子改进建议
- 📊 自动测试因子性能（夏普比率、适应度等）
- 🔧 支持WorldQuant Brain平台的所有操作符
- 📈 智能优化策略，提升因子Sharpe比率
- 💾 自动保存测试结果和优化建议

## 📋 系统要求

- Python 3.8+
- WorldQuant Brain账户
- OpenRouter API密钥（用于访问GPT-5）

## 🛠️ 安装

1. 克隆仓库
```bash
git clone https://github.com/your-username/worldquant-factor-optimizer.git
cd worldquant-factor-optimizer
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置凭证
```bash
cp credentials_example.txt credentials.txt
# 编辑 credentials.txt 文件，填入你的真实凭证
```

## ⚙️ 配置

在 `credentials.txt` 文件中配置以下信息：

```json
["your_worldquant_email", "your_worldquant_password"]
OPENROUTER_API_KEY="your_openrouter_api_key"
```

**注意：** 请确保 `credentials.txt` 文件不会被提交到版本控制系统中。

## 🎯 使用方法

### 基本用法

```python
from gpt_optimizer import WorldQuantFactorOptimizer

# 创建优化器实例
optimizer = WorldQuantFactorOptimizer()

# 运行优化流程
optimizer.run_optimization()
```

### 交互式使用

直接运行主程序：

```bash
python gpt_optimizer.py
```

程序会提示你输入要优化的因子表达式，或者使用默认因子。

## 📊 支持的因子函数

### 基础数学运算
- `abs(x)`, `add(x, y)`, `divide(x, y)`, `multiply(x, y)`
- `power(x, y)`, `sqrt(x)`, `subtract(x, y)`
- `max(x, y)`, `min(x, y)`, `sign(x)`, `log(x)`, `inverse(x)`

### 时间序列函数
- `ts_corr(x, y, d)`, `ts_covariance(x, y, d)`
- `ts_mean(x, d)`, `ts_std_dev(x, d)`, `ts_delta(x, d)`
- `ts_delay(x, d)`, `ts_decay_linear(x, d)`, `ts_rank(x, d)`
- `ts_sum(x, d)`, `ts_product(x, d)`, `ts_zscore(x, d)`

### 截面函数
- `rank(x)`, `scale(x)`, `normalize(x)`, `quantile(x)`
- `zscore(x)`, `winsorize(x)`

### 分组函数
- `group_rank(x, group)`, `group_mean(x, weight, group)`
- `group_neutralize(x, group)`

### 逻辑函数
- `if_else(condition, x, y)`, `and(x, y)`, `or(x, y)`, `not(x)`

## 🔍 优化策略

工具会自动应用以下优化策略：

1. **时间序列稳定性优化** - 使用平滑函数减少噪音
2. **截面标准化优化** - 提高横截面可比性
3. **波动率调整** - 处理异常值，提高稳定性
4. **多因子组合优化** - 组合多个有效信号
5. **均值回归策略** - 利用市场均值回归特性

## 📁 输出结果

程序会生成包含以下信息的JSON结果文件：

- 原始因子性能
- 改进建议的详细说明
- 每个建议因子的性能指标
- 夏普比率、适应度、换手率等关键指标

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

- 本工具仅供学习和研究使用
- 因子优化结果不构成投资建议
- 使用本工具进行实际投资的风险由用户自行承担
- 请遵守WorldQuant Brain平台的使用条款

## 📞 支持

如果你遇到问题或有建议，请：

1. 查看 [Issues](https://github.com/your-username/worldquant-factor-optimizer/issues)
2. 创建新的Issue
3. 联系项目维护者

---

⭐ 如果这个项目对你有帮助，请给它一个星标！
