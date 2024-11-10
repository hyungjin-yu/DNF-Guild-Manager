from src.crawler.guild_crawler import GuildCrawler
import time

def main():
    # 테스트할 캐릭터 정보
    character = {
        "name": "기도하는여자",
        "server": "프레이"
    }
    
    print("[{}] 크롤러 초기화 중...".format(
        time.strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    crawler = GuildCrawler()
    crawler.setup_driver()
    
    try:
        server_info = f"{character['server']} 서버의 " if character['server'] else ""
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {server_info}{character['name']} 캐릭터 정보 수집 중...")
        
        character_info = crawler.get_character_info(character['name'], character['server'])
        
        print("\n=== 캐릭터 정보 ===")
        if character_info:
            for key, value in character_info.items():
                print(f"{key}: {value}")
        else:
            print("캐릭터 정보를 찾을 수 없습니다.")
            
    finally:
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 크롤러 종료 중...")
        crawler.close()

if __name__ == "__main__":
    main()