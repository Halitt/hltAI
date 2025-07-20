from typing import List
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult

class Scraper:
    def __init__(self, urls: list[str]):
        self.urls = urls

    async def scrape(self) -> List[str]:
        news = []
        async with AsyncWebCrawler() as crawler:
            config = CrawlerRunConfig(
                excluded_tags=['form', 'header', 'footer', 'nav'],
                exclude_external_links=True,    
                exclude_social_media_links=True,
                exclude_internal_links=True,
                excluded_selector=".post__socials-block, .tags-list__list",
                exclude_all_images=True,
                target_elements=["article"]
            )
            
            results: List[CrawlResult] = await crawler.arun_many(
                urls=self.urls,
                config=config
            )

            for result in results:
                news.append(result.markdown.raw_markdown)
        
        return news
