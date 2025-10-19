🧠 Eternal — AI News Source Reference & Update Mechanism
Overview

Eternal automatically gathers and organizes real-time updates from the world’s most reliable, first-source AI platforms — the same sources top researchers, developers, and creators track before information reaches YouTube or social media.

This document lists every source used in Eternal’s data pipeline, how each category is collected, and the logic used by the backend scraper to produce daily structured reports.

⚙️ How Eternal Collects AI News

Update Frequency:

Twice daily — at 05:00 UTC and 17:00 UTC.

Uses a Python-based collector executed through GitHub Actions (zero-cost automation).

Data Flow:

Source Feeds → Python Collector → JSON Output → GitHub Pages → Web App (Normal + Advanced)


Modes:

Normal Mode → Displays today’s aggregated news (today.json).

Advanced Mode → Allows selection of the previous six days using /data/index.json.

🧩 Master List of AI Update Sources
1. 📰 Daily and Instant Updates

Real-Time News Sites

Source	Description	URL
arXiv AI Section	New academic papers on core AI topics.	arxiv.org/list/cs.AI/new

Hugging Face Blog	Model releases, dataset launches, partnerships, developer updates.	huggingface.co/blog

Product Hunt (AI Category)	Daily tracker of new AI tools and startups.	producthunt.com/topics/artificial-intelligence

AI News Aggregators

Platform	Description	URL
ArtificialIntelligence-News.com	Real-time AI industry and research summaries.	artificialintelligence-news.com

Crescendo AI News	Focused coverage on AI tool updates and research trends.	crescendo.ai/news

There’s An AI For That	Catalog of daily new AI tools.	theresanaiforthat.com

Superhuman Newsletter	Daily digest of new AI startups and tools.	superhuman.ai
2. 🏢 Official Company & Research Blogs
Company	URL
OpenAI Blog	openai.com/blog

Anthropic Blog	anthropic.com/news

DeepMind Blog	deepmind.google/discover/blog

Google AI Blog	ai.googleblog.com
3. 📚 Research Repositories & Communities
Source	Focus	URL
Papers with Code	AI research papers with implementation links.	paperswithcode.com

AlphaXiv	Trending AI research with social tracking.	alphaxiv.org

GitHub Trending (AI)	Daily hot projects in AI and agent systems.	github.com/trending

Reddit Research Threads	Live discussions on new research and tools.	r/artificial
, r/MachineLearning
, r/ClaudeAI
4. ⚙️ Prompt Engineering Innovations
Source	Description
Anthropic XML Prompting Docs – shows use of <context>, <instruction>, <response> for structured prompts.	
Microsoft Azure Prompt Strategies – enterprise-level prompt formats and injection protection.	
Gemini API Prompt Design (Google) – XML and block syntax reference.	
LearnPrompting.org – free structured tutorials on prompt engineering.	
Reddit r/ClaudeAI – user-driven experiments improving prompt precision.	
5. 🧑‍💻 Developer & Researcher Channels

GitHub Projects

DAIR.AI: “ML Papers of the Week” annotated summaries.

Trending AI Repositories: Multi-agent frameworks, lightweight model launches.

Discord Servers

Learn AI Together – education, project collaboration.

OpenAI & Anthropic – official prompt discussion servers.

Community-curated AI Agent Discords (GitHub-maintained list).

Reddit Threads

r/artificial – tool launches & discussions.

r/singularity – research and trend conversations.

r/ClaudeAI – structured prompt testing.

6. 📰 Curated Newsletters & Substacks

The Rundown AI

Ahead of AI

Superhuman

Ben’s Bites

AI Supremacy Digest

Each provides daily/weekly summaries that Eternal aggregates or links to when relevant.

7. 🎧 Visual & Audio Sources
Type	Channel	Focus
YouTube	Two Minute Papers	Quick research breakdowns
	Yannic Kilcher	Deep dives into new AI papers
	Matt Wolfe / AI Advantage	Tool launches & updates
	Krish Naik	Hands-on tutorials
Podcasts	Lex Fridman Podcast	Expert interviews
	The AI Breakdown	Daily AI industry recap
8. 🧰 AI Tool Discovery Platforms
Platform	Description	URL
Product Hunt (AI section)	Daily ranking of new AI apps	producthunt.com

AI Scout	Categorized AI databases	aiscout.io

There’s An AI For That	1000+ categorized tools	theresanaiforthat.com

Futurepedia	Weekly updated AI product catalog	futurepedia.io
9. 🧾 Academic Conferences & Live Releases
Event	URL
NeurIPS	neurips.cc

ICLR	iclr.cc

ICML	icml.cc

ACL (Linguistics)	aclweb.org

Stanford AI Lab	ai.stanford.edu

Eternal fetches pre-publication announcements and accepted paper summaries from these conference feeds.

10. 🧭 Staying Ahead (Suggested Routine)
Frequency	Action
Daily	Check Eternal Normal Mode (today’s feed) or Product Hunt manually.
Weekly	Browse arXiv cs.AI/new, read “Ahead of AI”, and skim Hugging Face Blog.
Monthly	Read OpenAI/Anthropic/DeepMind blogs, join research Discords, and watch one detailed YouTube breakdown.

Bonus Tip:
For power users, Eternal’s feed can be imported into Feedly, Readwise Reader, or Hugging Face Spaces dashboards to merge multiple AI news streams into one personalized view.

🔍 How Eternal Uses These Sources
Step	Description
1. Collection	The Python backend scrapes or fetches RSS/API feeds for the sources above twice daily.
2. Filtering	Removes duplicates, spam, and repeated summaries.
3. Categorization	Groups entries into Research, Tools, Prompting, or Community.
4. Structuring	Exports to data/YYYY-MM-DD.json with summaries, links, and timestamps.
5. Hosting	Commits the output automatically to GitHub Pages (HTTPS).
6. Frontend Display	HTML/JS WebView renders results with Normal/Advanced filtering.
🔒 Security & Transparency

All operations are public and versioned in the Eternal GitHub repository.

No API keys or private data are exposed.

JSON endpoints are read-only.

Users can verify or fork Eternal to customize their feed sources.

🧩 Contribution & Expansion

Developers can:

Add new sources to /collector/generate_news.py.

Propose specialized feeds (e.g., “AI in Healthcare” or “Agent Frameworks”).

Fork and modify the schedule (cron) in .github/workflows/auto-update.yml.