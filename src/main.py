# -*- coding: utf-8 -*-
import alfred
import time
from datetime import datetime


def process(query_str):
    query_str = str(query_str).strip('"\' ')
    timestamp = parse_query_str(query_str)
    if timestamp is None:
        return
    results = gen_alfred_items(timestamp)
    xml = alfred.xml(results)
    alfred.write(xml)


# 返回时间戳
def parse_query_str(query_str):
    try:
        if query_str == 'now':
            t = int(time.time())
        else:
            try:
                t = int(query_str)
            except ValueError:
                t = parse_datetime(query_str)
    except (TypeError, ValueError):
        t = None
    return t


# 解析字符串格式时间
def parse_datetime(query_str):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y%m%d%H%M%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%Y%m%d%H%M",
    ]
    t = None
    for format in formats:
        try:
            t = int(time.mktime(time.strptime(query_str, format)))
            break
        except ValueError:
            pass
    return t


# 生成alfred格式数据
def gen_alfred_items(timestamp):
    index = 0
    results = []
    results.append(alfred.Item(
        title=str(timestamp),
        subtitle='',
        icon='icon.png',
        attributes={
            'uid': alfred.uid(index),
            'arg': timestamp,
        },
    ))
    index += 1

    # Various formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y%m%d%H%M%S",
    ]
    for format in formats:
        date_str = datetime.strftime(datetime.fromtimestamp(timestamp), format)
        results.append(alfred.Item(
            title=str(date_str),
            subtitle='',
            attributes={
                'uid': alfred.uid(index),
                'arg': date_str,
            },
            icon='icon.png',
        ))
        index += 1

    return results


if __name__ == "__main__":
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
