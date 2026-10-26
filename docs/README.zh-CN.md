<div align="center">

<img src="assets/overview.png" alt="LexBench Web Fetch — 评测实际返回的内容。" width="100%">

[English](../README.md) · **简体中文**

[![CI](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml/badge.svg)](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-51735b)](../LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-356a91)](../pyproject.toml)

[任务集](#任务集) · [快速开始](#快速开始) · [评分](#给响应评分) · [版本](#版本) · [相关仓库](#相关仓库) · [参与贡献](../CONTRIBUTING.md)

</div>

LexBench Web Fetch 定义了 550 条网页获取任务，评测返回的正文、带有效链接的记录、资源和文件。可以用自己的运行器，也可以接入 [Browser Eval](https://github.com/lexmount/browser-eval)，比较浏览器、提取工具和在线服务。

本仓库维护题目、验收规则和冻结输入绑定。Browser Eval 负责服务调用、计时、证据保存和对比报告。

## 任务集

| 任务集 | 题数 | 范围 |
| --- | ---: | --- |
| `webfetch` | 150 | 网页、文档、图片、视频和挑战页 |
| `dynamic-content` | 100 | 初始响应之后加载的内容和记录 |
| `popular-sites` | 100 | 常用网站的内容 |
| `access-restrictions` | 100 | 曾观察到访问限制的 URL |
| `articles` | 100 | 文章正文、初始评论和帖子列表 |

题库共五个任务集、550 条题目。公开定义包含任务说明和验收规则，完整冻结参考输入需另行获取。详见[数据与获取方式](../docs/data.md)和[文章验收要求](../src/lexbench_webfetch/definitions/evaluation/articles/README.md)。

## 快速开始

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，然后运行：

```sh
git clone https://github.com/lexmount/lexbench-webfetch.git
cd lexbench-webfetch
uv sync --frozen
uv run --frozen lexbench-webfetch list
uv run --frozen lexbench-webfetch validate
```

这些命令离线检查仓库自带的定义，无需浏览器或 API 密钥。

导出任务集前，先获取其输入清单列出的冻结文件，再运行：

```sh
uv run --frozen lexbench-webfetch export \
  --suite webfetch --source /absolute/path/approved-inputs \
  --output /absolute/path/new-input-directory
```

导出会验证输入哈希，将清单中的文件写入新目录。仓库不分发完整参考快照，目前也没有公开输入包。所需文件和获取条件见[数据指南](../docs/data.md)。

## 给响应评分

用一个应通过和一个应失败的示例试跑：

```sh
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/answer.txt
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/missing.txt
```

实际评测应使用经过验证的数据集中的完整任务。结构化响应字段通过 `--metadata metadata.json` 传入，交付文件通过 `--file /absolute/path/file` 传入。评分要求和结果发布规则见[评测协议](../docs/protocol.md)。

## 运行浏览器并生成报告

按 [Browser Eval 接入指南](https://github.com/lexmount/browser-eval/blob/main/docs/benchmarks.md)执行导出的任务，调用浏览器或在线服务，生成对比报告。服务账号、API 密钥和实测输出由运行环境管理。上面的命令只检查输入、给已保存的响应评分，不调用服务。

## 版本

当前完整题库的评测版本为 `2.0.1`（`bench-v2.0.1`），共 550 条题目；Python 工具包版本为 `0.3.0`。评测版本固定题目、参考输入和评分规则，工具包版本标识命令与 Python 实现。

运行 `uv run --frozen lexbench-webfetch version` 验证安装的题库。用 `release` 将实际选用的题目和评分器固定在 `benchmark-release.json` 中，用 `compare-releases` 判断结果能直接比较、需要重算评分，还是属于不同题目范围。升级包不会替换已有报告的评测版本。命令和版本变更规则见[版本说明](../docs/versions.md)。

## 相关仓库

| 仓库 | 用途 |
| --- | --- |
| [Browser Eval](https://github.com/lexmount/browser-eval) | 运行浏览器与服务、保存证据、生成对比报告 |
| [LexBench Web Search](https://github.com/lexmount/lexbench-websearch) | 搜索问题、来源参考和检索评分 |
| [Moli](https://github.com/lexmount/moli) | 可使用本题库评测的浏览器 |
| [WebFetch CLI](https://github.com/lexmount/webfetch-cli) | Lexmount WebFetch 服务的命令行客户端 |
| [Artifact Site](https://github.com/lexmount/artifact-site) | 报告托管、版本管理和分享 |
| [Lexbench-Headless-Browser](https://github.com/lexmount/Lexbench-Headless-Browser) | 协议、自动化驱动和 Web 平台评测 |

评分依赖和来源权利见[第三方说明](../THIRD_PARTY.md)。WebMainBench、WCXB 和 WebArena 是独立评测集，不计入这里的 550 条题目。

## 参与贡献

修改任务要求或评分前，请阅读 [CONTRIBUTING](../CONTRIBUTING.md)。运行 `make check` 检查定义和测试。

[安全](../SECURITY.md) · [第三方内容](../THIRD_PARTY.md) · [Apache 2.0](../LICENSE)

## 引用 LexBench Web Fetch

使用以下引用或 [CITATION.cff](../CITATION.cff)，并注明评测版本、任务集和代码版本。以下引用标识工具包版本，题库评测版本为 `2.0.1`。

```bibtex
@software{lexbench_webfetch_2026,
  author = {{LexBench Web Fetch contributors}},
  title = {LexBench Web Fetch},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/lexmount/lexbench-webfetch}
}
```
