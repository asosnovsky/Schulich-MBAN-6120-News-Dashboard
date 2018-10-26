from enum import Enum
from .NewsObj import NewsObj

class SortBy(Enum):
    RELEVANCY = 'relevancy' # articles more closely related to q come first.
    POPULARITY = 'popularity' # articles from popular sources and publishers come first.
    PUBLISH = 'publishedAt' #newest articles come first.

class Request(NewsObj):
    def __init__(self,
        baseUrl: str,
        apiKey: str,
        q: str,
        sources: str = None,
        fromDate: str = None,
        toDate: str = None,
        sortBy: SortBy = SortBy.PUBLISH,
        pageSize:int = 20,
        page:int = None
    ):
        NewsObj.__init__(
            self,
            baseUrl=baseUrl,
            apiKey=apiKey,
            q=q,
            sources=sources,
            fromDate=fromDate,
            toDate=toDate,
            sortBy=sortBy,
            pageSize=pageSize,
            page=page
        )
    
    def to_url(self) -> str:
        url = self.baseUrl + f"?apiKey={self.apiKey}&q={self.q}"
        if self.sources is not None:
            url += f"&sources={self.sources}"
        if self.fromDate is not None:
            url += f"&from={self.fromDate}"
        if self.toDate is not None:
            url += f"&to={self.toDate}"
        if self.page is not None:
            url += f"&page={self.page}"
        url += f"&sortBy={self.sortBy.value}&pageSize={self.pageSize}"
        return url