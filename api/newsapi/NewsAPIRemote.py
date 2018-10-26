import requests

from .Response import Response, Status
from .Request import Request, SortBy
from .Article import Article

class NewsAPIRemote:
    def __init__(self, baseUrl: str, apiKey: str):
        self.baseUrl = baseUrl
        self.apiKey = apiKey

    def create_request(self, 
        q: str,
        sources: str = None,
        fromDate: str = None,
        toDate: str = None,
        sortBy: SortBy = SortBy.PUBLISH,
        pageSize:int = 20,
        page:int = None
    ) -> Request:
        return Request(
            baseUrl=self.baseUrl,
            apiKey=self.apiKey,
            q=q,
            sources=sources,
            fromDate=fromDate,
            toDate=toDate,
            sortBy=sortBy,
            pageSize=pageSize,
            page=page,
        )
    
    def process_request(self, request_obj: Request) -> Response:
        return Response.from_json(
            requests.get(request_obj.to_url()).json()
        )