import pandas as pd
from datetime import datetime

class GuildData:
    def __init__(self):
        self.members_data = []
        
    def add_member(self, member_info):
        """길드원 정보 추가"""
        member_info['timestamp'] = datetime.now()
        self.members_data.append(member_info)
        
    def save_to_csv(self, filename):
        """데이터를 CSV 파일로 저장"""
        try:
            df = pd.DataFrame(self.members_data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"데이터가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"저장 중 오류 발생: {e}")
            
    def load_from_csv(self, filename):
        """CSV 파일에서 데이터 로드"""
        try:
            df = pd.read_csv(filename, encoding='utf-8-sig')
            self.members_data = df.to_dict('records')
            print(f"{filename}에서 데이터를 불러왔습니다.")
        except Exception as e:
            print(f"로드 중 오류 발생: {e}")
            
    def get_member_stats(self):
        """길드원 통계 정보 반환"""
        if not self.members_data:
            return None
            
        df = pd.DataFrame(self.members_data)
        stats = {
            '총 길드원 수': len(df),
            '직업별 분포': df.get('직업', pd.Series()).value_counts().to_dict(),
            '평균 버프력': df.get('버프력', pd.Series()).mean(),
            '데이터 갱신 시각': datetime.now()
        }
        return stats