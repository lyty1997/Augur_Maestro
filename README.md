# Augur_Maestro

Augur_Maestro 是量化研究与交易系统项目。当前 M1 阶段优先建设 A 股研究回测闭环和交易安全边界，不接真实交易。

## 本地开发

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.lock.txt
.venv/bin/python -m pre_commit install
```

## 质量检查

```bash
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m mypy -p rq_core
.venv/bin/detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
.venv/bin/python -m pip_audit -r requirements-dev.lock.txt
.venv/bin/python src/scripts/quality/markdown_docs_check.py
.venv/bin/python -m pytest
```

## 依赖锁定

`requirements-dev.txt` 是人工维护的开发依赖输入，`requirements-dev.lock.txt` 是 CI 和本地安装使用的锁定结果。更新依赖后运行：

```bash
.venv/bin/python -m piptools compile requirements-dev.txt \
  --output-file requirements-dev.lock.txt \
  --no-emit-index-url \
  --no-emit-trusted-host
```

## 项目文档

- 文档入口：[docs/README.md](docs/README.md)
- 项目规范：[AGENTS.md](AGENTS.md)
- Codex 规则入口：[codex-rules/global-AGENTS.md](codex-rules/global-AGENTS.md)

## 安全边界

M1 默认只允许研究、回测、dry-run 和只读查询设计。真实下单、撤单、改单、条件单、预埋单或任何会改变券商侧订单状态的调用，必须先完成设计确认、风控、OMS、人工确认、交易时间检查、审计日志和对账机制。
