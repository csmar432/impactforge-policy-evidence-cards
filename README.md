# ImpactForge 2026

## 项目题目

**Policy Evidence Cards**

## 定位

一个帮助学生和普通公众读懂政策数据的轻量工具：把一项公共议题拆成三张证据卡，再接上结论、局限和来源，降低政策信息的阅读门槛。

## 比赛约束

- 官方 Overview 的资格摘要：居住国已达到法定成年年龄、学生身份、非公司/专业组织；全球开放，但排除 Brazil、Crimea、Cuba、Iran、North Korea、Quebec 和 Russia。你是否符合，必须由你本人按官方规则确认。
- 官方 Rules 允许 1–5 人团队，单人参赛也可以。
- 截止日期存在官方页面冲突（核对于 2026-08-16）：Overview 显示 2026-08-23 23:45 PDT，Rules 页面显示 2026-07-23（均为 PDT）。在 Devpost 或主办方确认前，不应把任一日期当作最终有效截止日。
- 重点是社会影响、问题—方案—用户闭环和可展示的 proof of work。
- 需要项目故事、问题、解决方案、功能、工具、用户、截图/演示/文件和 impact statement；项目链接建议提供。

官方入口：[ImpactForge Devpost](https://impactforge.devpost.com/)
规则页：[ImpactForge Rules](https://impactforge.devpost.com/rules)

## MVP

主题已定为 **学生食物不安全（U.S. college students）**。MVP 做一个主题、三张证据卡和一个结论页，优先保证手机端能看懂、每张卡都能点回来源、截图能说明产品已经工作。

当前页面把 GAO 的 2020 NPSAS 分析拆成三个连续问题：规模（23%）、严重程度（2.2 million）和政策缺口（59% 未报告领取 SNAP）。页面明确标注数据年份、定义、来源和局限，不把 2020 数据包装成 2026 现状。

## 项目目录

- `src/`：最小网页或静态页面
- `data/`：三张卡使用的数据、来源和局限（`evidence.json`）
- `submission/`：截图、短演示、impact statement 和 Devpost 文案

## 交付状态

- [x] 选定一个学生真正关心的公共议题
- [x] 完成三张证据卡
- [x] 做出能打开的响应式静态页面
- [x] 加入 source-to-action 下一步交互和本地 reader check
- [x] 加入无依赖的 MVP 验收脚本
- [x] 写 impact statement、项目故事和 60 秒演示脚本
- [x] 生成与当前页面一致的 proof-of-work 截图
- [ ] 在 Devpost 提交

## 本地运行

```bash
python3 -m http.server 4173 --directory src
```

然后打开 `http://127.0.0.1:4173/`。这是本地演示地址；页面没有依赖、后端或构建步骤，可直接用于本地验收和 proof of work。评委公开访问仍需要公开仓库或部署链接。

公开演示：<https://csmar432.github.io/impactforge-policy-evidence-cards/>。GitHub Pages 由 `.github/workflows/pages.yml` 从 `src/` 自动部署。

验收：

```bash
python3 submission/check_mvp.py
python3 submission/check_mvp.py --url http://127.0.0.1:4173/
IMPACTFORGE_URL=http://127.0.0.1:4173/ python3 submission/check_browser.py  # 需要本机已有 Playwright/Chromium；同时刷新全部八张证明截图
```

如果 `4173` 已被其他本地服务占用，使用任意空闲端口启动 `src/`，再通过 `IMPACTFORGE_URL` 指向该地址；不要让验收脚本误读其他项目的页面。

## 投稿边界

这是四个项目中最轻量的增奖项目。不要复制整套研究工作流；只保留能让用户看懂证据的部分，优先交付可见成品。
