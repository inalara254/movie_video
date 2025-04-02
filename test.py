
from encrpyt import send_request
def get_search_list(query):
    url=f"/m-station/search/drama?keywords={query}&size=10&order=match&search_after=&isExecuteVipActivity=true"
    result = send_request(url)
    return  result
def get_episodes(id):
    url=f"/m-station/drama/page?hsdrOpen=0&isAgeLimit=0&dramaId={id}&quality=UHD4K&hevcOpen=1"
    result = send_request(url)
    return  result
def get_episodes_video(id,episodeSid):
    url=f"/m-station/drama/page?hsdrOpen=0&isAgeLimit=0&dramaId={id}&episodeSid={episodeSid}&quality=UHD4K&hevcOpen=1"
    result = send_request(url)
    return  result




