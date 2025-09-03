import requests
import json
import time
import pandas as pd
from os.path import expanduser
from requests.auth import HTTPBasicAuth
from typing import List, Dict, Any
from openai import OpenAI


class WorldQuantFactorOptimizer:
    def __init__(self, factor=None):
        # 加载凭证
        self.load_credentials()
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openrouter_api_key,
        )
        
        # 初始化WorldQuant会话
        self.sess = self.sign_in()
        
        # 先加载可用的操作符（用于输入校验）
        self.available_operators = self.load_operators()

        # 获取用户输入的原始因子
        if factor:
            self.original_factor = factor
        else:
            self.original_factor = self.get_user_input_factor()
        
        # 提示词模板
        self.prompt_template = """
你是一个专业的量化金融因子优化专家。请针对以下WorldQuant alpha因子给出5条具体的改进建议：

原始因子: {original_factor}

**重要：请只使用以下WorldQuant Brain平台支持的操作符和函数：**

**基础数学运算：**
- abs(x), add(x, y), divide(x, y), multiply(x, y), power(x, y), sqrt(x), subtract(x, y)
- max(x, y), min(x, y), sign(x), log(x), inverse(x)

**时间序列函数：**
- ts_corr(x, y, d), ts_covariance(x, y, d), ts_mean(x, d), ts_std_dev(x, d)
- ts_delta(x, d), ts_delay(x, d), ts_decay_linear(x, d), ts_rank(x, d)
- ts_sum(x, d), ts_product(x, d), ts_zscore(x, d), ts_scale(x, d)

**截面函数：**
- rank(x), scale(x), normalize(x), quantile(x), zscore(x), winsorize(x)

**分组函数：**
- group_rank(x, group), group_mean(x, weight, group), group_neutralize(x, group)

**逻辑函数：**
- if_else(condition, x, y), and(x, y), or(x, y), not(x)

要求：
1. 每条建议必须包含具体的改进逻辑说明
2. 每条建议必须提供完整的改进后的因子表达式
3. 因子表达式必须只使用上述支持的操作符和函数
4. 只给出5条建议，不要多也不要少
5. 每条建议要针对不同的优化方向，重点关注能提升Sharpe比率的策略：
   - 时间序列稳定性优化（如使用ts_decay_linear、ts_mean等平滑函数）
   - 截面标准化优化（如使用zscore、normalize等函数）
   - 波动率调整（如使用ts_std_dev、winsorize等函数）
   - 多因子组合优化（如使用multiply、add等函数组合多个有效信号）
   - 均值回归策略（如使用ts_zscore、ts_rank等函数）
6. 建议要具体、可操作，避免过于抽象的描述
7. **重要：优先考虑能显著提升Sharpe比率的改进策略，避免过度复杂化导致过拟合**

请按以下格式输出：
建议1: [改进逻辑说明]
改进后因子: [完整的因子表达式]

建议2: [改进逻辑说明]
改进后因子: [完整的因子表达式]

建议3: [改进逻辑说明]
改进后因子: [完整的因子表达式]

建议4: [改进逻辑说明]
改进后因子: [完整的因子表达式]

建议5: [改进逻辑说明]
改进后因子: [完整的因子表达式]

注意：因子表达式必须是完整的、可执行的WorldQuant Brain代码，只使用上述支持的操作符。

**Sharpe比率优化指导：**
- 使用ts_decay_linear、ts_mean等函数平滑时间序列，减少噪音
- 使用zscore、normalize等函数进行截面标准化，提高横截面可比性
- 使用winsorize、ts_std_dev等函数处理异常值，提高稳定性
- 避免过度复杂的嵌套函数，保持表达式的简洁性
- 优先使用经过验证有效的函数组合，如ts_corr+rank、ts_covariance+zscore等
"""

    def load_operators(self) -> str:
        """加载可用的操作符列表"""
        try:
            with open('operators.txt', 'r', encoding='utf-8') as f:
                operators_content = f.read()
            print("✅ 成功加载WorldQuant Brain操作符列表")
            return operators_content
        except FileNotFoundError:
            print("⚠️ 未找到operators.txt文件，使用内置操作符列表")
            return """
基础数学运算: abs(x), add(x, y), divide(x, y), multiply(x, y), power(x, y), sqrt(x), subtract(x, y)
时间序列函数: ts_corr(x, y, d), ts_covariance(x, y, d), ts_mean(x, d), ts_std_dev(x, d), ts_delta(x, d), ts_decay_linear(x, d), ts_rank(x, d)
截面函数: rank(x), scale(x), normalize(x), quantile(x), zscore(x), winsorize(x)
分组函数: group_rank(x, group), group_mean(x, weight, group), group_neutralize(x, group)
逻辑函数: if_else(condition, x, y), and(x, y), or(x, y), not(x)
"""
        except Exception as e:
            print(f"⚠️ 加载操作符文件失败: {e}，使用内置操作符列表")
            return """
基础数学运算: abs(x), add(x, y), divide(x, y), multiply(x, y), power(x, y), sqrt(x), subtract(x, y)
时间序列函数: ts_corr(x, y, d), ts_covariance(x, y, d), ts_mean(x, d), ts_std_dev(x, d), ts_delta(x, d), ts_decay_linear(x, d), ts_rank(x, d)
截面函数: rank(x), scale(x), normalize(x), quantile(x), zscore(x), winsorize(x)
分组函数: group_rank(x, group), group_mean(x, weight, group), group_neutralize(x, group)
逻辑函数: if_else(condition, x, y), and(x, y), or(x, y), not(x)
"""

    def get_user_input_factor(self) -> str:
        """获取用户输入的原始因子表达式"""
        print("🎯 WorldQuant 因子优化器")
        print("=" * 50)
        print("请输入你想要优化的原始因子表达式")
        print("示例: (-1 * ts_corr(rank(open), rank(volume), 10))")
        print("或者直接按回车使用默认因子")
        print("-" * 50)
        
        while True:
            user_input = input("请输入因子表达式 (或按回车使用默认): ").strip()
            
            if not user_input:
                default_factor = "(-1 * ts_corr(rank(open), rank(volume), 10))"
                print(f"使用默认因子: {default_factor}")
                return default_factor
            
            # 验证输入格式
            if self.validate_factor_input(user_input):
                print(f"✅ 使用用户输入的因子: {user_input}")
                return user_input
            else:
                print("❌ 因子表达式格式不正确，请重新输入")
                print("提示：确保表达式完整且没有重复部分")
    
    def validate_factor_input(self, factor: str) -> bool:
        """验证因子输入格式
        - 基于支持的操作符/函数列表进行校验
        - 放宽长度限制，避免误报
        """
        if not factor:
            return False

        # 从已加载的操作符文本中提取函数名（例如 abs(x) -> abs）
        import re

        allowed_functions = set()
        if hasattr(self, 'available_operators') and isinstance(self.available_operators, str):
            for line in self.available_operators.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # 匹配以 函数名( 开头的行
                m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
                if m:
                    allowed_functions.add(m.group(1))

        # 常见同义名或历史拼写，宽松允许（仅用于本地校验）
        if 'ts_std_dev' in allowed_functions:
            allowed_functions.add('ts_stddev')

        # 从用户表达式中提取调用的函数名 tokens
        used_function_tokens = set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(", factor))

        # 若至少包含一个受支持的函数，则通过函数存在性校验
        if not (allowed_functions and (used_function_tokens & allowed_functions)):
            print("   ❌ 未检测到有效的因子函数")
            return False

        # 括号匹配检查
        if factor.count('(') != factor.count(')'):
            print(
                f"   ❌ 括号不匹配: 开括号({factor.count('(')}) != 闭括号({factor.count(')')})"
            )
            return False

        # 放宽长度限制：仅在极端情况下提示
        if len(factor) > 2000:
            print("   ⚠️ 表达式过长，请检查是否存在粘贴错误")
            return False

        return True

    def load_credentials(self):
        """加载凭证文件"""
        try:
            with open(expanduser('credentials.txt')) as f:
                lines = f.readlines()
            
            # 解析第一行：WorldQuant凭证
            worldquant_creds = json.loads(lines[0].strip())
            self.username, self.password = worldquant_creds
            
            # 解析第二行：OpenRouter API key
            openrouter_api_key = None
            for line in lines[1:]:
                if line.startswith('OPENROUTER_API_KEY='):
                    openrouter_api_key = line.split('=', 1)[1].strip().strip('"')
                    break
            
            if not openrouter_api_key:
                raise ValueError("未找到OpenRouter API key")
            
            self.openrouter_api_key = openrouter_api_key
            
            print("✅ 成功加载凭证")
            
        except Exception as e:
            raise Exception(f"加载凭证失败: {str(e)}")

    def sign_in(self):
        """登录WorldQuant Brain平台"""
        sess = requests.Session()
        sess.auth = HTTPBasicAuth(self.username, self.password)
        
        response = sess.post('https://api.worldquantbrain.com/authentication')
        
        # 201状态码表示登录成功，200也表示成功
        if response.status_code in [200, 201]:
            print("✅ WorldQuant Brain平台登录成功")
            return sess
        else:
            raise Exception(f"登录失败: {response.status_code} - {response.text}")

    def get_gpt_suggestions(self) -> List[Dict[str, str]]:
        """使用OpenAI客户端获取因子改进建议"""
        print("🤖 正在使用GPT-5-chat生成因子改进建议...")
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/worldquant-factor-optimizer",
                    "X-Title": "WorldQuant Factor Optimizer",
                },
                extra_body={},
                model="openai/gpt-5-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的量化金融因子优化专家，精通WorldQuant Brain平台的因子语法和函数。"
                    },
                    {
                        "role": "user",
                        "content": self.prompt_template.format(original_factor=self.original_factor)
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # 处理GPT-5-chat的响应格式
            content = ""
            if completion.choices and len(completion.choices) > 0:
                choice = completion.choices[0]
                message = choice.message
                
                # 获取content
                content = message.content or ""
                
                if not content:
                    print("⚠️ 响应内容为空，尝试使用简化提示词...")
                    return self.get_simple_suggestions()
            
            if content:
                print("📝 GPT-5-chat回复:")
                print(content)
                print("-" * 80)
                
                # 解析建议
                suggestions = self.parse_gpt_suggestions(content)
                return suggestions
            else:
                print("❌ API响应中没有有效内容")
                print("🔄 使用默认建议作为备选...")
                return self.get_default_suggestions()
            
        except Exception as e:
            print(f"❌ GPT-5-chat API调用失败: {str(e)}")
            print("🔄 使用默认建议作为备选...")
            # 返回默认建议作为备选
            return self.get_default_suggestions()

    def get_simple_suggestions(self) -> List[Dict[str, str]]:
        """使用简化提示词获取建议"""
        print("🔄 使用简化提示词重新尝试...")
        
        try:
            simple_prompt = f"""
请针对因子 '{self.original_factor}' 给出5条改进建议，格式如下：

建议1: 添加时间衰减
改进后因子: ts_decay_linear({self.original_factor}, 5)

建议2: 结合波动率
改进后因子: ({self.original_factor} * ts_stddev(close, 10))

建议3: 截面排名
改进后因子: rank({self.original_factor})

建议4: 多指标组合
改进后因子: ({self.original_factor} * ts_corr(rank(close), rank(volume), 10))

建议5: 均值回归
改进后因子: ({self.original_factor} * rank(close - open))
"""
            
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://github.com/worldquant-factor-optimizer",
                    "X-Title": "WorldQuant Factor Optimizer",
                },
                extra_body={},
                model="anthropic/claude-sonnet-4",
                messages=[
                    {
                        "role": "user",
                        "content": simple_prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = completion.choices[0].message.content
            if content:
                print("📝 简化提示词回复:")
                print(content)
                print("-" * 80)
                
                suggestions = self.parse_gpt_suggestions(content)
                return suggestions
            else:
                print("⚠️ 简化提示词仍然没有内容，使用默认建议")
                return self.get_default_suggestions()
                
        except Exception as e:
            print(f"❌ 简化提示词调用失败: {str(e)}")
            return self.get_default_suggestions()

    def parse_gpt_suggestions(self, content: str) -> List[Dict[str, str]]:
        """解析GPT-5-chat的建议内容"""
        suggestions = []
        
        # 尝试解析新的格式 (### 建议X: 格式)
        import re
        
        # 匹配 ### 建议X: 格式
        suggestion_pattern = r'### 建议(\d+):\s*(.+?)(?=### 建议|\Z)'
        suggestion_matches = re.findall(suggestion_pattern, content, re.DOTALL)
        
        if suggestion_matches:
            print(f"🔍 检测到 {len(suggestion_matches)} 个建议 (新格式)")
            
            for match in suggestion_matches:
                suggestion_num = match[0]
                suggestion_content = match[1].strip()
                
                # 提取标题（第一行非空内容）
                lines = suggestion_content.split('\n')
                title = ""
                expression = ""
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('```') and not line.startswith('改进后因子'):
                        if not title:
                            title = line
                        else:
                            break
                
                # 提取代码块中的表达式
                code_block_pattern = r'```(?:[\w]*\n)?(.*?)```'
                code_blocks = re.findall(code_block_pattern, suggestion_content, re.DOTALL)
                
                if code_blocks:
                    expression = code_blocks[0].strip()
                else:
                    # 如果没有代码块，尝试从文本中提取
                    expression_match = re.search(r'改进后因子[：:]\s*(.+?)(?=\n|$)', suggestion_content)
                    if expression_match:
                        expression = expression_match.group(1).strip()
                
                if title and expression:
                    suggestions.append({
                        'description': title,
                        'expression': expression
                    })
        
        # 如果新格式解析失败，尝试旧的格式
        if not suggestions:
            print("🔍 尝试解析旧格式...")
            lines = content.split('\n')
            
            current_suggestion = {}
            in_code_block = False
            current_code = ""
            
            for line in lines:
                stripped_line = line.strip()
                
                # 检查是否是建议标题
                if stripped_line.startswith('**建议') and ':' in stripped_line:
                    # 保存之前的建议
                    if current_suggestion and 'expression' in current_suggestion:
                        suggestions.append(current_suggestion)
                    
                    # 开始新建议
                    title_part = stripped_line.split(':', 1)[1].split('**')[0].strip()
                    current_suggestion = {'description': title_part}
                    in_code_block = False
                    current_code = ""
                
                # 检查代码块开始
                elif stripped_line.startswith('```') and not in_code_block:
                    in_code_block = True
                    current_code = ""
                
                # 检查代码块结束
                elif stripped_line.startswith('```') and in_code_block:
                    in_code_block = False
                    if current_code.strip() and current_suggestion:
                        current_suggestion['expression'] = current_code.strip()
                    current_code = ""
                
                # 收集代码块内容
                elif in_code_block and stripped_line:
                    if current_code:
                        current_code += " " + stripped_line
                    else:
                        current_code = stripped_line
                
                # 兼容旧格式
                elif stripped_line.startswith('改进后因子:') and ':' in stripped_line:
                    expr = stripped_line.split(':', 1)[1].strip()
                    if current_suggestion:
                        current_suggestion['expression'] = expr
            
            # 添加最后一个建议
            if current_suggestion and 'expression' in current_suggestion:
                suggestions.append(current_suggestion)
        
        # 如果解析失败，返回默认建议
        if len(suggestions) != 5:
            print(f"⚠️ 解析GPT-5-chat建议失败，返回默认建议 (解析到{len(suggestions)}条)")
            # 打印调试信息
            print("调试信息：已解析的建议:")
            for i, sugg in enumerate(suggestions, 1):
                print(f"  {i}. 描述: {sugg.get('description', 'N/A')}")
                print(f"     表达式: {sugg.get('expression', 'N/A')}")
            return self.get_default_suggestions()
        
        return suggestions

    def get_default_suggestions(self) -> List[Dict[str, str]]:
        """获取默认的因子改进建议"""
        return [
            {
                "description": "结合其他市场指标",
                "expression": f"({self.original_factor} * ts_corr(rank(close), rank(volume), 10))"
            },
            {
                "description": "添加时间衰减",
                "expression": f"ts_decay_linear({self.original_factor}, 5)"
            },
            {
                "description": "包含波动率指标",
                "expression": f"({self.original_factor} * ts_stddev(close, 10))"
            },
            {
                "description": "截面排名方法",
                "expression": f"rank({self.original_factor})"
            },
            {
                "description": "结合均值回归逻辑",
                "expression": f"({self.original_factor} * rank(close - open))"
            }
        ]

    def test_factor(self, factor_expression: str, description: str) -> Dict[str, Any]:
        """测试单个因子"""
        print(f"\n🧪 正在测试因子: {description}")
        print(f"📊 表达式: {factor_expression}")
        
        # 构建模拟请求
        simulation_data = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": "USA",
                "universe": "TOP3000",
                "delay": 1,
                "decay": 6,
                "neutralization": "SUBINDUSTRY",
                "truncation": 0.08,
                "pasteurization": "ON",
                "unitHandling": "VERIFY",
                "nanHandling": "ON",
                "language": "FASTEXPR",
                "visualization": False,
            },
            "regular": factor_expression
        }
        
        try:
            # 发送模拟请求
            sim_resp = self.sess.post(
                'https://api.worldquantbrain.com/simulations',
                json=simulation_data,
            )
            
            if sim_resp.status_code != 201:
                return {
                    'status': 'failed',
                    'error': f"模拟请求失败: {sim_resp.status_code}",
                    'description': description,
                    'expression': factor_expression
                }
            
            # 获取模拟进度URL
            sim_progress_url = sim_resp.headers['Location']
            
            # 等待模拟完成
            print("⏳ 等待模拟完成...")
            while True:
                sim_progress_resp = self.sess.get(sim_progress_url)
                retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
                if retry_after_sec == 0:  # 模拟完成
                    break
                time.sleep(retry_after_sec)
            
            # 获取alpha ID
            alpha_id = sim_progress_resp.json()["alpha"]
            print(f"✅ 模拟完成，Alpha ID: {alpha_id}")
            
            # 获取详细结果
            alpha_details_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
            alpha_details_resp = self.sess.get(alpha_details_url)
            
            if alpha_details_resp.status_code == 200:
                alpha_data = alpha_details_resp.json()
                
                result = {
                    'status': 'success',
                    'alpha_id': alpha_id,
                    'description': description,
                    'expression': factor_expression,
                    'sharpe': alpha_data.get('is', {}).get('sharpe', 0),
                    'fitness': alpha_data.get('is', {}).get('fitness', 0),
                    'turnover': alpha_data.get('is', {}).get('turnover', 0),
                    'returns': alpha_data.get('is', {}).get('returns', 0),
                    'pnl': alpha_data.get('is', {}).get('pnl', 0)
                }
                
                # 打印结果
                print(f"  📊 夏普比率: {result['sharpe']:.3f}")
                print(f"  🎯 适应度: {result['fitness']:.3f}")
                print(f"  🔄 换手率: {result['turnover']:.3f}")
                print(f"  📈 收益率: {result['returns']:.3f}")
                print(f"  💰 PnL: {result['pnl']:.2f}")
                
                return result
            else:
                return {
                    'status': 'failed',
                    'error': f"无法获取Alpha详情: {alpha_details_resp.status_code}",
                    'description': description,
                    'expression': factor_expression
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'description': description,
                'expression': factor_expression
            }

    def run_optimization(self):
        """运行完整的因子优化流程"""
        print("🚀 开始WorldQuant因子优化流程")
        print("=" * 80)
        print(f"🎯 目标因子: {self.original_factor}")
        print("=" * 80)
        
        # 1. 获取GPT-5-chat建议
        suggestions = self.get_gpt_suggestions()
        
        print(f"📋 获得 {len(suggestions)} 条改进建议:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion['description']}")
            print(f"     表达式: {suggestion['expression']}")
        print("-" * 80)
        
        # 2. 测试原始因子
        print("🔍 首先测试原始因子作为基准...")
        original_result = self.test_factor(self.original_factor, "原始因子")
        
        # 3. 测试改进后的因子
        print("\n🔄 开始测试改进后的因子...")
        improved_results = []
        
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{'='*60}")
            print(f"测试第 {i} 条建议")
            print(f"{'='*60}")
            
            result = self.test_factor(suggestion['expression'], suggestion['description'])
            improved_results.append(result)
            
            # 每测试3个因子后重新登录，避免断线
            if i % 3 == 0:
                print("🔄 重新登录以保持连接...")
                self.sess = self.sign_in()
        
        # 4. 汇总结果
        self.summarize_results(original_result, improved_results)

    def summarize_results(self, original_result: Dict, improved_results: List[Dict]):
        """汇总并分析所有测试结果"""
        print("\n" + "="*80)
        print("🎯 因子优化测试结果汇总")
        print("="*80)
        
        # 收集所有成功的结果
        all_results = [original_result] + improved_results
        successful_results = [r for r in all_results if r.get('status') == 'success']
        failed_results = [r for r in all_results if r.get('status') != 'success']
        
        print(f"✅ 成功测试: {len(successful_results)} 个因子")
        print(f"❌ 测试失败: {len(failed_results)} 个因子")
        
        if successful_results:
            # 按夏普比率排序
            successful_results.sort(key=lambda x: x.get('sharpe', 0), reverse=True)
            
            print(f"\n🏆 因子排名 (按夏普比率):")
            for i, result in enumerate(successful_results, 1):
                status_icon = "🆕" if result.get('description') != "原始因子" else "📊"
                print(f"  {i}. {status_icon} {result.get('description', '未知')}")
                print(f"     夏普比率: {result.get('sharpe', 0):.3f}")
                print(f"     适应度: {result.get('fitness', 0):.3f}")
                print(f"     换手率: {result.get('turnover', 0):.3f}")
                print(f"     表达式: {result.get('expression', 'N/A')}")
                print()
            
            # 找出最佳改进
            if len(successful_results) > 1:
                best_improved = None
                for result in successful_results:
                    if result.get('description') != "原始因子":
                        best_improved = result
                        break
                
                if best_improved:
                    improvement = best_improved.get('sharpe', 0) - original_result.get('sharpe', 0)
                    print(f"💡 最佳改进因子: {best_improved.get('description')}")
                    print(f"   夏普比率提升: {improvement:.3f}")
                    print(f"   改进后表达式: {best_improved.get('expression')}")
        
        # 保存结果
        timestamp = int(time.time())
        results_file = f"gpt5chat_factor_optimization_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'original_factor': self.original_factor,
                'timestamp': timestamp,
                'results': all_results
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n📁 详细结果已保存到: {results_file}")
        print("🎉 因子优化测试完成！")


def main():
    """主函数"""
    try:
        optimizer = WorldQuantFactorOptimizer()
        optimizer.run_optimization()
    except Exception as e:
        print(f"❌ 程序执行失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
