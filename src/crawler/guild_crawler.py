from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

class GuildCrawler:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        """셀레니움 드라이버 설정"""
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        
    def get_character_info(self, character_name, server_name=None):
        """캐릭터 정보를 가져옴"""
        try:
            # 던담 검색 페이지 접속
            self.driver.get("https://dundam.xyz/search")
            time.sleep(3)
            
            # 서버가 지정된 경우에만 서버 선택
            if server_name:
                server_select = Select(self.driver.find_element(By.ID, "server"))
                server_select.select_by_visible_text(server_name)
                time.sleep(2)
            
            # 캐릭터 이름 입력
            search_input = self.driver.find_element(By.NAME, "name")
            search_input.clear()
            search_input.send_keys(character_name)
            search_input.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # 검색 결과에서 캐릭터 정보 찾기
            character_div = self.driver.find_element(By.CLASS_NAME, "scon")
            
            # 캐릭터 정보 수집 (클릭하기 전)
            job = self.driver.find_element(By.CLASS_NAME, "seh_job").text
            fame = self.driver.find_element(By.CLASS_NAME, "level").text
            
            # 캐릭터 정보 클릭하여 상세 페이지로 이동
            character_div.click()
            time.sleep(5)
            
            # 길드 정보 찾기
            script = """
            return Array.from(document.getElementsByTagName('*')).find(
                element => window.getComputedStyle(element).color === 'rgb(177, 155, 119)'
            )?.textContent || '길드 정보 없음';
            """
            guild_name = self.driver.execute_script(script)
            
            # 버프/딜러 점수 찾기
            # 버프/딜러 점수 찾기
            try:
                dval_elements = self.driver.find_elements(By.CLASS_NAME, "dval")
                for dval in dval_elements:
                    if dval.text and dval.text.replace(',', '').isdigit():
                        score = dval.text
                        # 부모 요소의 텍스트를 확인하여 버프/딜러 구분
                        parent_text = dval.find_element(By.XPATH, "..").text
                        if "버프 점수" in parent_text:
                            power_info = {"buff_score": score}
                        else:
                            power_info = {"dealer_score": score}
                        break
                else:
                    power_info = {"power_type": "정보 없음"}
            except Exception as e:
                print(f"버프/딜러 정보 찾기 실패: {e}")
                power_info = {"power_type": "정보 없음"}
            
            character_info = {
                'name': character_name,
                'job': job,
                'fame': fame,
                'guild': guild_name,
                **power_info,  # 버프 점수 또는 딜러 점수 정보 추가
            }
            
            return character_info
                
        except Exception as e:
            print(f"Error: {e}")
            return None
            
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()