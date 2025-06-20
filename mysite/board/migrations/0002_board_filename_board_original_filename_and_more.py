# Generated by Django 5.1.3 on 2024-12-07 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='filename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='파일명'),
        ),
        migrations.AddField(
            model_name='board',
            name='original_filename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='원본파일명'),
        ),
        migrations.AlterField(
            model_name='board',
            name='content',
            field=models.TextField(verbose_name='내용'),
        ),
        migrations.AlterField(
            model_name='board',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='작성일시'),
        ),
        migrations.AlterField(
            model_name='board',
            name='created_by',
            field=models.CharField(max_length=20, verbose_name='글쓴이'),
        ),
        migrations.AlterField(
            model_name='board',
            name='password',
            field=models.CharField(max_length=20, verbose_name='비밀번호'),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=100, verbose_name='제목'),
        ),
    ]
