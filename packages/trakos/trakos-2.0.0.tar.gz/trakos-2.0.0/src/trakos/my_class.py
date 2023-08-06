from user_agent import generate_user_agent
class iq:
    def run():
        print("Hello Python :)")
        return " Dont Forgot, Install Library :)"
    
class fake:
        def get():
            return (generate_user_agent())
class check:
    def Tiktok(self,user):
        response=requests.get(f'https://www.tiktok.com/@{user}',headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36","Connection": "close","Host": "www.tiktok.com","Accept-Encoding": "gzip, deflate","Cache-Control": "max-age=0"}).status_code
        return response
        pass    