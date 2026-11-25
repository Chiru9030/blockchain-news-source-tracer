import sys
import argparse
from src.news_service import NewsService
from src.analyzer import SourceAnalyzer
from src.blockchain import BlockchainManager

def main():
    parser = argparse.ArgumentParser(description="Fake News Source-Tracer")
    parser.add_argument("query", type=str, help="Headline or topic to trace")
    args = parser.parse_args()

    print(f"\n🔍 Tracing source for: '{args.query}'...\n")

    # 1. Fetch News
    news_service = NewsService()
    articles = news_service.find_related_articles(args.query)
    
    if not articles:
        print("❌ No articles found.")
        sys.exit(1)

    print(f"✅ Found {len(articles)} related articles.")

    # 2. Analyze Source
    analyzer = SourceAnalyzer()
    result = analyzer.analyze_sources(articles)
    
    if not result:
        print("❌ Could not analyze articles.")
        sys.exit(1)

    original = result['original_article']
    confidence = result['confidence_score']
    
    print("\n------------------------------------------------")
    print("🏆 IDENTIFIED ORIGINAL SOURCE")
    print("------------------------------------------------")
    print(f"Source: {original['source']['name']}")
    print(f"Title:  {original['title']}")
    print(f"Date:   {original['publishedAt']}")
    print(f"URL:    {original['url']}")
    print(f"Confidence Score: {confidence}/100")
    print("------------------------------------------------\n")

    # 3. Record on Blockchain
    print("🔗 Recording to Decentralized Ledger (Polygon)...")
    blockchain = BlockchainManager()
    tx_hash = blockchain.record_verification(original['url'], confidence)
    
    print(f"✅ Verified & Recorded!")
    print(f"Transaction Hash: {tx_hash}\n")

if __name__ == "__main__":
    main()
