import os
from flask import Flask, render_template_string, request, jsonify
from src.news_service import NewsService
from src.analyzer import SourceAnalyzer
from src.blockchain import BlockchainManager

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsTrace — Decentralized Provenance & Source Verifier</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
    <!-- Navbar -->
    <header class="border-b border-slate-800 bg-slate-900/70 backdrop-blur sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-purple-600 flex items-center justify-center font-black text-white shadow-lg shadow-purple-500/30">
                    N
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-lg font-bold tracking-tight text-white">NewsTrace</h1>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-400 border border-purple-500/30 uppercase">
                            Polygon Ledger
                        </span>
                    </div>
                    <p class="text-xs text-slate-400">Automated NLP Provenance & Blockchain Anchor</p>
                </div>
            </div>
            <div class="text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
                Network: <span class="text-emerald-400 font-semibold">Polygon Proof-of-Stake</span>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto px-6 py-10">
        <!-- Hero Title -->
        <div class="text-center max-w-2xl mx-auto mb-10">
            <h2 class="text-3xl font-extrabold text-white tracking-tight sm:text-4xl">
                Trace News to Its Primary Origin
            </h2>
            <p class="mt-3 text-sm text-slate-400">
                Identify the first publisher, compute chronological & lexical confidence scores, and anchor cryptographic receipts to decentralized storage.
            </p>
        </div>

        <!-- Search Form -->
        <div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-2xl mb-8">
            <form method="POST" class="flex flex-col sm:flex-row gap-3">
                <input 
                    type="text" 
                    name="query" 
                    required 
                    placeholder="Enter headline, topic, or keyword (e.g. AI Breakthrough, Mars Rover)..." 
                    value="{{ query or '' }}"
                    class="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-purple-500"
                >
                <button 
                    type="submit" 
                    class="bg-purple-600 hover:bg-purple-500 text-white font-bold px-6 py-3 rounded-xl transition-all shadow-lg shadow-purple-500/30 text-sm whitespace-nowrap"
                >
                    Trace & Verify
                </button>
            </form>

            <div class="flex items-center gap-2 mt-4 text-xs text-slate-500">
                <span>Quick Demos:</span>
                <a href="/trace?q=AI breakthrough" class="text-purple-400 hover:underline">AI Breakthrough</a> &bull;
                <a href="/trace?q=Quantum Computing record" class="text-purple-400 hover:underline">Quantum Computing</a> &bull;
                <a href="/trace?q=Deep space radio signal" class="text-purple-400 hover:underline">Deep Space Signal</a>
            </div>
        </div>

        {% if result %}
        <!-- Results Section -->
        <div class="space-y-6">
            <!-- Source Card -->
            <div class="bg-slate-900 border border-purple-500/30 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
                <div class="absolute -top-12 -right-12 w-40 h-40 bg-purple-500/10 rounded-full blur-2xl pointer-events-none"></div>
                
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
                    <div>
                        <span class="text-[11px] uppercase font-bold text-purple-400 tracking-wider">Identified Original Source</span>
                        <h3 class="text-xl font-bold text-white mt-1">{{ result.original_article.title }}</h3>
                        <p class="text-xs text-slate-400 mt-1">
                            Publisher: <span class="text-slate-200 font-semibold">{{ result.original_article.source.name }}</span> &bull; 
                            Published: <span class="font-mono text-slate-300">{{ result.original_article.publishedAt }}</span>
                        </p>
                    </div>

                    <div class="bg-purple-950/60 border border-purple-500/40 px-5 py-3 rounded-xl text-center shrink-0">
                        <span class="text-[10px] text-purple-300 uppercase font-semibold">Credibility Confidence</span>
                        <div class="text-3xl font-black text-purple-300">{{ result.confidence_score }}<span class="text-base text-purple-400 font-normal">/100</span></div>
                    </div>
                </div>

                <!-- Blockchain Proof -->
                <div class="mt-5 p-4 rounded-xl bg-slate-950 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                        <span class="text-[10px] text-slate-500 uppercase font-semibold">Polygon Ledger Anchor Receipt</span>
                        <p class="text-xs font-mono text-emerald-400 break-all">{{ tx_hash }}</p>
                    </div>
                    <span class="text-xs px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-full font-semibold shrink-0">
                        Immutable Seal Verified
                    </span>
                </div>
            </div>

            <!-- Timeline -->
            <div class="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl">
                <h4 class="font-bold text-white text-base mb-1">Chronological Propagation Timeline</h4>
                <p class="text-xs text-slate-400 mb-5">Order of publication demonstrating the earliest recorded claim.</p>

                <div class="space-y-3">
                    {% for item in result.timeline %}
                    <div class="flex items-start gap-4 p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80">
                        <div class="w-2 h-2 rounded-full {% if loop.first %}bg-purple-500 ring-4 ring-purple-500/20{% else %}bg-slate-600{% endif %} mt-2 shrink-0"></div>
                        <div class="flex-1 min-w-0">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                                <span class="text-sm font-semibold text-white truncate">{{ item.title or item.source }}</span>
                                <span class="text-xs font-mono text-slate-400 shrink-0">{{ item.time }}</span>
                            </div>
                            <span class="text-xs text-slate-400 mt-0.5 block">Source: {{ item.source }}</span>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </main>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    query = None
    result = None
    tx_hash = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()
    elif request.args.get("q"):
        query = request.args.get("q", "").strip()

    if query:
        news_service = NewsService()
        articles = news_service.find_related_articles(query)
        if articles:
            analyzer = SourceAnalyzer()
            result = analyzer.analyze_sources(articles)
            if result:
                blockchain = BlockchainManager()
                tx_hash = blockchain.record_verification(
                    result['original_article'].get('url', 'http://example.com'),
                    result['confidence_score']
                )

    return render_template_string(HTML_TEMPLATE, query=query, result=result, tx_hash=tx_hash)

@app.route("/trace")
def trace_get():
    return index()

@app.route("/api/trace")
def api_trace():
    q = request.args.get("q", "AI breakthrough").strip()
    news_service = NewsService()
    articles = news_service.find_related_articles(q)
    if not articles:
        return jsonify({"success": False, "message": "No articles found"}), 404

    analyzer = SourceAnalyzer()
    result = analyzer.analyze_sources(articles)
    blockchain = BlockchainManager()
    tx_hash = blockchain.record_verification(
        result['original_article'].get('url', 'http://example.com'),
        result['confidence_score']
    )
    return jsonify({
        "success": True,
        "query": q,
        "result": result,
        "blockchain_receipt": tx_hash
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 NewsTrace Web Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
