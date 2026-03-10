from datetime import datetime, timedelta

class Helper:
    
    @staticmethod
    def format_time(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def format_date_yyyymmdd(dt):
        return dt.strftime("%Y-%m-%d")
    
    @staticmethod
    def now():
        return datetime.now()
    
    @staticmethod
    def get_prev_day(days_behind):
        return datetime.now() - timedelta(days=days_behind)