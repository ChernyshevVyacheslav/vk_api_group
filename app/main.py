from models import Group

from apscheduler.schedulers.background import BlockingScheduler


def main():
    group_posts = group.posts_of_group(2)
    new_posts = group.check_posts(group_posts)
    group.send_to_chat(new_posts)


if __name__ == '__main__':
    group = Group('domain')
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', seconds=3)
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass
    scheduler.shutdown()
