import asyncio
from urllib import parse
import aiohttp
import time
from pyquery import PyQuery as pq

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

INDEX_URL = 'https://static4.scrape.cuiqingcai.com/page/{page}'
BASE = 'https://static4.scrape.cuiqingcai.com'


class Movie(object):
	def __init__(self):
		self.headers = headers
	
	async def reqeust_func(self, url):
		try:
			async with self.session.get(url) as response:
				if response.status == 200:
					return await response.text()
				return None
				# else:
				# 	return None
		except aiohttp.ClientError as e:
			return print(f"e:>>>{e}")
		
		
	async def scrape_index(self, page):
		url = INDEX_URL.format(page = page)
		return await self.reqeust_func(url)
	
	async def parse_index_page(self, content):
		set_url =  set()
		for html in content:
			doc = pq(html)
			results = doc('#app #index .el-row .el-col .el-card .el-card__body .el-row .p-h .name')
			for h in results.items():
				detail_url = h.attr('href')
				detail_url = parse.urljoin(BASE, detail_url)
				set_url.add(detail_url)
		return set_url
	
	async def main(self):
		self.session = aiohttp.ClientSession(headers = headers)
		tasks = [asyncio.ensure_future(self.scrape_index(page)) for page in range(11)]
		results = await asyncio.gather(*tasks)
		detail_page_url = await self.parse_index_page(results)
		print(detail_page_url)
		await self.session.close()
	
if __name__ == '__main__':
	start_time = time.time()
	loop = asyncio.get_event_loop()
	movie = Movie()
	loop.run_until_complete(movie.main())
	print(time.time() - start_time)

	
		
	
	
	
	