from author import get_author_metrics
from issue_avg_open_issues_by_repo import get_avg
from issue_median_close_by_repo import get_median
from issue_median_open_time import get_median_open
from organizations_metrics import get_org

if __name__ == "__main__":
    print(get_author_metrics())
    get_avg()
    get_median()
    get_median_open()
    get_org()
