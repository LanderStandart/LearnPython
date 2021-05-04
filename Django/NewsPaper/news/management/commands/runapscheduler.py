import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Post,Category,PostCategory
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)
#today = date.today()

# наша задача по выводу текста на экран
def my_job():
    # #  Your job processing logic here...
    # new_post = Post.objects.filter(insertdt__gt=datetime.now()-timedelta(days=7))
    # sub= Category.objects.all()
    # for cat in sub:
    #     post = Post.objects.filter(category_id=cat.id,insertdt__gt=datetime.now()-timedelta(days=7))
    #     if post.count()>0:
    #         q = cat.subscribers.all()
    #         for mail in q:
    #
    #             print(mail.email)
    #             for postn in post:
    #                 print(postn.id,postn.caption)
    #             html_content = render_to_string(
    #                 'week_news.html', {
    #                     'post': post,
    #                     'user': mail.username,
    #                     'category':cat.name
    #                 }
    #             )
    #             msg = EmailMultiAlternatives(
    #                 subject='Django NewsPortal WeekNews',
    #                 body='d',
    #                 from_email='landerneo@yandex.ru',
    #                 to=[mail.email]
    #             )
    #             msg.attach_alternative(html_content, "text/html")
    #             msg.send()
    # #print(datetime.now()-timedelta(days=7),'hello from job',sub)
    # print(html_content)
    # print('------------')


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger= CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ),
            #CronTrigger(second="*/10"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")