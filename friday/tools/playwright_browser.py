"""
Browser Automation — Playwright-based web browsing capabilities adapted from JARVIS.
"""

def register(mcp):

    @mcp.tool()
    async def web_search(query: str) -> str:
        """
        Search the web using DuckDuckGo and return the top results.
        Requires Playwright to be installed.
        """
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return "The 'playwright' library is not installed, sir. I cannot search the web interactively."
            
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(f"https://html.duckduckgo.com/html/?q={query}", wait_until="domcontentloaded")
                
                raw = await page.evaluate('''
                    () => {
                        const items = document.querySelectorAll('.result');
                        return Array.from(items).slice(0, 5).map(item => ({
                            title: (item.querySelector('.result__title a') || item.querySelector('.result__a'))?.textContent?.trim() || '',
                            url: (item.querySelector('.result__title a') || item.querySelector('.result__a'))?.href || '',
                            snippet: item.querySelector('.result__snippet')?.textContent?.trim() || ''
                        }));
                    }
                ''')
                
                await browser.close()
                
                if not raw:
                    return f"No results found for '{query}', sir."
                    
                lines = [f"Search Results for '{query}':"]
                for r in raw:
                    if r.get("title") and r.get("url"):
                        lines.append(f"- {r['title']}")
                        lines.append(f"  URL: {r['url']}")
                        lines.append(f"  Snippet: {r.get('snippet', '')}")
                        lines.append("")
                        
                return "\\n".join(lines)
        except Exception as e:
            return f"Search failed: {str(e)}"

    @mcp.tool()
    async def read_webpage(url: str) -> str:
        """
        Visit a URL and extract the main text content using Playwright.
        Use this when you need to read an article or website.
        """
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            return "The 'playwright' library is not installed, sir."
            
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                
                data = await page.evaluate('''
                    () => {
                        const title = document.title || '';
                        const main = document.querySelector('main')
                            || document.querySelector('article')
                            || document.querySelector('[role="main"]')
                            || document.body;

                        const clone = main.cloneNode(true);
                        for (const el of clone.querySelectorAll(
                            'script, style, nav, header, footer, aside, .sidebar, .menu, .ad, iframe'
                        )) {
                            el.remove();
                        }

                        const text = clone.innerText || clone.textContent || '';
                        return { title: title, text: text.substring(0, 5000).trim() };
                    }
                ''')
                
                await browser.close()
                
                title = data.get("title", "")
                text = data.get("text", "")
                return f"Title: {title}\\nURL: {url}\\n\\n{text}"
                
        except Exception as e:
            return f"Failed to read webpage '{url}': {str(e)}"
