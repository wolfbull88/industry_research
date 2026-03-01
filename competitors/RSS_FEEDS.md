# RSS订阅源配置

## 已验证可用的RSS源

### 🚗 微出行/出行行业

| 网站 | RSS URL | 状态 |
|-----|--------|------|
| **Zag Daily** | https://zagdaily.com/feed/ | ✅ 推荐 |
| **Electrek** | https://electrek.co/feed/ | ✅ 电动出行 |
| **TechCrunch** | https://techcrunch.com/feed/ | ✅ 科技媒体 |
| Smart Cities Dive | https://www.smartcitiesdive.com/feeds/news/ | ✅ 智慧城市 |

### 📰 备选行业源

| 网站 | 订阅方式 |
|-----|---------|
| Micromobility.com | 邮件订阅 (无RSS) |
| The Verge Transportation | 无独立RSS |
| Traffic Technology Today | https://www.traffictechnologytoday.com/?feed=rss2 |

---

## 使用方法

### 运行RSS聚合器
```bash
cd ~/projects/industry_research/scripts
python3 rss_aggregator.py
```

### 自动化 (可选)

可以设置cron job每天自动运行:
```bash
# 每天早上8点运行
0 8 * * * cd /home/wolfbull/.openclaw/workspace-mars/projects/industry_research/scripts && python3 rss_aggregator.py >> logs/rss_$(date +\%Y-\%m-\%d).log 2>&1
```

---

## 最近抓取的新闻示例

最新文章:
1. **Zag Daily**: Joby posts 2025 results alongside Uber air taxi tie-up
2. **Zag Daily**: Young Scots and Welsh voters call for safer cycling streets
3. **Electrek**: How a young bike racer helped shape America's best-selling low-cost e-bike
4. **TechCrunch**: Why China's humanoid robot industry is winning
5. **Smart Cities Dive**: Traffic deaths declined 12% in 2025

---

*更新于: 2026-03-01*
