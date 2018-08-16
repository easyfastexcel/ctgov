import sys
import time
import datetime


# TIME MANAGEMENT
def time_stamp(stamp_type='default'):
    now = datetime.datetime.now()
    if stamp_type == 'default' or stamp_type == 'yyyy.mm.dd hh:mm:ss':
        return '{}.{}.{} {}:{}:{}'.format(now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
                                          now.strftime('%H'), now.strftime('%M'), now.strftime('%S'))
    elif stamp_type == 'file_name' or stamp_type == 'yyyymmdd_hhmmss':
        return '{}{}{}_{}{}{}'.format(now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
                                      now.strftime('%H'), now.strftime('%M'), now.strftime('%S'))
    elif stamp_type == 'yyyymmdd':
        return '{}{}{}'.format(now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'))
    elif stamp_type == 'dd-mmm-yy':
        return '{}-{}-{}'.format(now.strftime('%d'), now.strftime('%h'), now.strftime('%y'))
    else:
        timestamp_error = '{}.{}.{} {}:{}:{}'.format(now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
                                                     now.strftime('%H'), now.strftime('%M'), now.strftime('%S'))
        error_message = '[ ERROR: ' + timestamp_error + ' ] "' + str(stamp_type) + '" is not a known stamp_type.'
        sys.exit(error_message)


def wait_sec(seconds, print_seconds=False):
    for sec, rsec in zip(range(seconds+1), reversed(range(seconds+1))):
        time.sleep(1)
        sec += 1
        if print_seconds:
            print('[', time_stamp(), ']', 'WAIT TIME:', rsec, 'sec.')


if __name__ == "__main__":
    pass
