# paper-to-patent-cn

`paper-to-patent-cn` 是一个 Codex skill，用于将学术论文、PDF、摘要或方法说明转换为中文发明专利申请书草稿，并生成最终版式的 DOCX/PDF 审阅文件。

本项目的重点不是把论文逐句翻译成专利，而是从论文中提取可专利化的技术事实，建立“技术问题-技术方案-技术效果”的闭环，并在不虚构论文未披露内容的前提下组织为权利要求书和说明书。

## 功能特点

- 从论文或结构化笔记中提取专利技术事实。
- 生成结构化 `patent_content.json`。
- 按最终版 Word 格式生成中国发明专利申请书 DOCX。
- 可生成 PDF 审阅副本。
- 在摘要附图和说明书附图部分默认只插入 `图1`、`图2` 等图题，不嵌入图片或空白图片占位。
- 提供内容 JSON 审计和 DOCX XML 版式校验。
- 将论文未披露但可能影响专利支撑的内容记录为材料缺口。

## 输出结构

生成的专利申请书采用以下顺序：

1. 专利信息页
2. `说   明   书   摘   要`
3. `摘    要   附   图`
4. `权  利  要  求  书`
5. `说   明   书`
6. 发明名称
7. `技术领域`
8. `背景技术`
9. `发明内容`
10. `附图说明`
11. `具体实施方式`
12. `说 明 书 附 图`

## 仓库结构

```text
paper-to-patent-cn-repo/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── SECURITY.md
├── requirements.txt
├── .gitignore
└── paper-to-patent-cn/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

`paper-to-patent-cn/` 是 Codex skill 本体；仓库根目录文件用于 GitHub 展示、授权、依赖和安全说明。

## 安装

将 skill 文件夹复制到 Codex skills 目录：

```powershell
Copy-Item -Recurse .\paper-to-patent-cn "$env:USERPROFILE\.codex\skills\paper-to-patent-cn"
```

安装辅助脚本依赖：

```powershell
python -m pip install -r requirements.txt
```

## 使用方式

在 Codex 中直接请求：

```text
Use $paper-to-patent-cn to convert this paper into a Chinese invention patent application DOCX/PDF.
```

如果已经有结构化 JSON：

```powershell
python .\paper-to-patent-cn\scripts\audit_patent_content_json.py .\patent_content.json
python .\paper-to-patent-cn\scripts\generate_final_patent_docx.py .\patent_content.json --output-dir .\outputs --pdf
python .\paper-to-patent-cn\scripts\validate_final_word_format.py .\outputs\patent_application.docx
```

## 内容原则

- 所有技术内容必须来自论文、用户提供材料或可追溯的源事实。
- 不编造结构、尺寸、器件参数、工艺窗口、实验数据或技术效果。
- 权利要求应避免 `大约`、`可能`、`优选`、`可以`、`比如`、`不限于` 等不确定表述。
- 缺失但重要的信息应写入 `gaps`，而不是写进正式专利正文。
- 生成的 DOCX 默认不包含嵌入图片。

## 隐私与披露警告

专利草稿可能包含未公开技术披露。上传或分享前，请确认没有提交：

- 论文 PDF 或全文抽取文本；
- 生成的专利 DOCX/PDF；
- 真实发明披露材料；
- 专利内容 JSON；
- 图片、截图、SVG/PNG 附图资产；
- 个人姓名、电话、邮箱、身份证号、本机路径、API key、token；
- 机构内部模板或未公开流程。

建议发布前运行：

```powershell
rg -n "api_key|secret|password|Authorization|Bearer|sk-|身份证|电话|邮箱" .
```

## 授权

Copyright (c) 2026 LYJ. All rights reserved.

本仓库采用禁止商用的 source-available 授权：允许个人、学术和研究等非商业用途查看、复制、运行和修改；未经 LYJ 书面授权，不得商用、用于付费服务、商业产品再分发、模型训练、数据集构建、再发布或声称为原创。详见 `LICENSE`。
