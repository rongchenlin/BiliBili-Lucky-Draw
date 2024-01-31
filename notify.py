from service.notify_service.notify_service import NotifyService
from service.remove_share import RemoveShareService
from service.statistics_service import StatisticsService
from utils import globals


if __name__ == '__main__':
    cnt, content = StatisticsService().today_data()
    NotifyService().fangtang_msg_push_by_content(title="每日统计", content=content)
    print('每日统计结果: ' + content)
    RemoveShareService(globals.my_user_id, cnt=globals.remove_cnt).start_remove_service()
