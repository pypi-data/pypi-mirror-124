from __future__ import print_function

import time
import requests
from threading import Thread, Lock
from datetime import datetime


class Getmetric:
    def __init__(self, async_dump=True, max_queue_len=25000, send_period_sec=60, batch_max_size=250, send_debug=False):
        self.__is_async = async_dump
        self.__max_queue_len = max_queue_len
        self.__send_period_sec = send_period_sec
        self.__batch_max_size = batch_max_size
        self.__sent_count = 0
        self.__send_retry_count = 3
        self.__queue_mutex = Lock()
        self.__running = True
        self.__queue = []
        self.__per_sec_queue_mutex = Lock()
        self.__per_sec_map = {}
        self.__send_debug = send_debug
        if async_dump:
            self.__thread = Thread(target=self.__sending_thread)
            self.__thread.start()
        self.__batch_url = "https://node.getmetric.net/api1/batch"

    @staticmethod
    def __check_value(value):
        if type(value) is int or type(value) is float:
            return True
        return False

    def __push_measures_to_queue(self, _type, code, dt, values):
        with self.__queue_mutex:
            if len(self.__queue) > self.__max_queue_len:
                return False
            self.__queue.append([_type, code, dt, values])
            return True

    def __push_per_sec_measures_to_queue(self, _type, code, dt, values):
        with self.__per_sec_queue_mutex:
            if code in self.__per_sec_map:
                existing = self.__per_sec_map[code]
                if len(values) != len(existing[3]) or _type != existing[0]:
                    # overwrite
                    self.__per_sec_map[code] = [_type, code, dt, values]
                    return False

                diff = (dt - existing[2]).total_seconds()
                if diff > 1:
                    res = self.__push_measures_to_queue(existing[0], existing[1], existing[2], existing[3])
                    self.__per_sec_map[code] = [_type, code, dt, values]
                    return res

                # inc values
                for ei in range(len(existing[3])):
                    for v in values:
                        if existing[3][ei][0] == v[0]:
                            existing[3][ei][1] += v[1]

                self.__per_sec_map[code] = existing
            else:
                # add new
                self.__per_sec_map[code] = [_type, code, dt, values]

        return True

    def __check_and_dump_per_sec(self):
        dt = datetime.utcnow()
        with self.__per_sec_queue_mutex:
            keys = list(self.__per_sec_map.keys())
            for k in keys:
                existing = self.__per_sec_map[k]
                diff = (dt - existing[2]).total_seconds()
                if diff > 1:
                    self.__push_measures_to_queue(existing[0], existing[1], existing[2], existing[3])
                    del self.__per_sec_map[k]

    def push_measure(self, code, value):
        """
        push single measure with default field value

        :param code: getmetric measurement code
        :param value: (int, float) value
        :return: True for successful push to send queue
        """
        if len(code) < 1:
            # just pass
            return True

        if not self.__check_value(value):
            return False

        return self.__push_measures_to_queue(1, code, datetime.utcnow(), [["", value]])

    def push_measures(self, code, values):
        """
        push multiple measure fields with their value

        :param code: getmetric measurement code
        :param values: dict of values ex.: {"int_field": 1, "float_field": 1.1, ...}
        :return: True for successful push to send queue
        """
        if len(code) < 1:
            # just pass
            return True

        if type(values) is not dict or len(values) < 1:
            return False

        _values = []
        for k in values.keys():
            if len(k) < 1:
                return False
            if not self.__check_value(values[k]):
                return False
            _values.append([k, values[k]])

        return self.__push_measures_to_queue(1, code, datetime.utcnow(), _values)

    def push_per_second_measure(self, code, value):
        """
        push default field measure with per second value aggregation (increment by value)

        :param code: getmetric measurement code
        :param value: (int, float) increment value
        :return: bool
        """
        if len(code) < 1:
            # just pass
            return True

        if not self.__check_value(value):
            return False

        return self.__push_per_sec_measures_to_queue(1, code, datetime.utcnow(), [["", value]])

    def push_per_second_measures(self, code, values):
        """
        push multiple fields measure with per second value aggregation (increment by value)

        :param code: getmetric measurement code
        :param values: dict of values ex.: {"int_field": 1, "float_field": 1.1, ...}
        :return: bool
        """
        if len(code) < 1:
            # just pass
            return True

        if type(values) is not dict or len(values) < 1:
            return False

        _values = []
        for k in values.keys():
            if len(k) < 1:
                return False
            if not self.__check_value(values[k]):
                return False
            _values.append([k, values[k]])

        return self.__push_per_sec_measures_to_queue(1, code, datetime.utcnow(), _values)

    def __send_queue(self, batch_queue):
        if len(batch_queue) < 1:
            return True

        js_arr = []
        for bq in batch_queue:
            values = []
            for v in bq[3]:
                values.append({"name": v[0], "value": v[1]})
            js_arr.append({"type": bq[0], "code": bq[1], "time": bq[2].isoformat() + 'Z', "values": values})

        if self.__send_debug:
            print("getmetric send:")
            print(js_arr)
            self.__sent_count += len(js_arr)
            return True

        x = requests.post(self.__batch_url, json=js_arr, timeout=3)
        if x.status_code == 200:
            self.__sent_count += len(js_arr)
            return True

        return False

    def send(self):
        while True:
            self.__check_and_dump_per_sec()

            # cut batch
            with self.__queue_mutex:
                batch_queue = self.__queue[:self.__batch_max_size]
                self.__queue = self.__queue[self.__batch_max_size:]
            if len(batch_queue) < 1:
                break

            res = False
            for n in range(self.__send_retry_count):
                res = self.__send_queue(batch_queue)
                if res:
                    break

            if not res:
                # restore queue
                with self.__queue_mutex:
                    batch_queue.extend(self.__queue)
                    self.__queue = batch_queue
                return False

        return True

    def __sending_thread(self):
        counter = 0
        while self.__running:
            while self.__running and counter < self.__send_period_sec:
                time.sleep(1)
                counter += 1

            counter = 0
            if not self.__running:
                continue

            self.send()

    def get_queue_len(self):
        with self.__queue_mutex:
            return len(self.__queue)

    def get_sent_count(self):
        return self.__sent_count

    def stop(self):
        if not self.__running:
            return
        self.__running = False

        if self.__is_async:
            self.__thread.join()


def test_write(code):
    send_debug = False
    if len(code) < 1:
        code = "dummy_code"
        send_debug = True
    gm = Getmetric(async_dump=False, send_debug=send_debug)
    gm.push_measure(code, 1000)
    time.sleep(0.3)
    gm.push_measures(code, {"test": 1500})
    time.sleep(0.3)
    gm.push_measures(code, {"test": 2000})
    time.sleep(1)
    for x in range(10):
        gm.push_per_second_measure(code, 1)
        time.sleep(0.1)
    time.sleep(1)
    gm.send()


if __name__ == '__main__':
    test_write("")
