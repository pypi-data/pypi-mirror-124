# Health Watchdog is a script health supervisor.
# Author: Andrés Eduardo Torres Hernández
import time


class Health_Watchdog:
    def __init__(
            self,
            target_class_name,
            logger,
            diagnostics_callback=None,
            timers_configuration=None):
        self._logger = logger
        self._target_class_name = target_class_name
        # Stamp types:
        self._BEGINNING_STAMP = 0
        self._BEGINNING2END_STAMP = 1
        # Begin a dictionary of timers:
        if (timers_configuration != None):
            try:
                self.TIMERS = {timer_name: {
                    "warning_timer_value": float(timer_config["warning_timer_value"]),
                    "error_timer_value": float(timer_config["error_timer_value"]),
                    "warning_start2end_function_timer_value": float(timer_config["warning_start2end_function_timer_value"]),
                    "error_start2end_function_timer_value": float(timer_config["error_start2end_function_timer_value"]),
                    "_tracker": {
                        "beginning_time": float(0),
                        "endpoint_function_time": float(0),
                        "on_flag": False
                    },
                    "_statistics": {
                        "beginning_timer": {
                            "current_laps": int(0),
                            "last_lap_time": float(0),
                            "last_10_laps_average_time": float(0),
                            "total_laps_average_time": float(0),
                            "total_deltatime_laps": int(0),
                            "most_delayed_lap_time": float(0)
                        },
                        "beginning2end_timer": {
                            "current_laps": int(0),
                            "last_lap_time": float(0),
                            "last_10_laps_average_time": float(0),
                            "total_laps_average_time": float(0),
                            "total_deltatime_laps": int(0),
                            "most_delayed_lap_time": float(0)
                        },
                        "_to_compute_data_list": []
                    }
                } for timer_name, timer_config in timers_configuration.items()}
            except Exception as e:
                self._logger.error(
                    "The timers configuration descriptor is invalid: {}".format(e))
                raise Exception
        else:
            self.TIMERS = None
        # Diagnostics callback
        if (diagnostics_callback != None and
                callable(diagnostics_callback) == True):
            self._diagnostics_callback = diagnostics_callback
        else:
            self._diagnostics_callback = None
            self._logger.info("There is not a diagnostics callback function on the class {}. The health watchdog will report issues to the default logger instead.".format(
                self._target_class_name
            ))

    def begin_track(self, timer):
        '''Begin the tracking of a thread or periodic function. Therefore, reset the watchdog timer.'''
        if (self.TIMERS != None):
            _current_time = time.time()
            # Begin the watchdog timer:
            if (self.TIMERS[timer]["_tracker"]["on_flag"] == False):
                self.TIMERS[timer]["_tracker"]["on_flag"] = True
                self.TIMERS[timer]["_tracker"]["beginning_time"] = _current_time
                self.TIMERS[timer]["_tracker"]["endpoint_function_time"] = _current_time
            # Statistics:
            self._feed_beginning_statistics_data(timer, _current_time)
            # Set current time:
            self.TIMERS[timer]["_tracker"]["beginning_time"] = _current_time
        else:
            pass

    def flash_endpoint_function(self, timer):
        '''Reset the timer where this function is placed. It's useful to determine if a piece of function is executed
        under a determined estimated time according to the developer criteria.'''
        if (self.TIMERS != None):
            _current_time = time.time()
            self.TIMERS[timer]["_tracker"]["endpoint_function_time"] = _current_time
            # Statistics:
            self._feed_beginning2end_statistics_data(timer, _current_time)
        else:
            pass

    def _feed_beginning_statistics_data(self, timer, current_time):
        '''Add timestamps into a list, then such data will be computed by the function each serve strobe period.'''
        # // Current quantity of laps:
        self.TIMERS[timer]["_statistics"]["beginning_timer"]["current_laps"] += 1
        # get timestamp:
        self.TIMERS[timer]["_statistics"]["_to_compute_data_list"].append(
            (current_time, self._BEGINNING_STAMP))

    def _feed_beginning2end_statistics_data(self, timer, current_time):
        '''Add timestamps into a list, then such data will be computed by the function each serve strobe period.'''
        # // Current quantity of laps:
        self.TIMERS[timer]["_statistics"]["beginning2end_timer"]["current_laps"] += 1
        # get timestamp:
        self.TIMERS[timer]["_statistics"]["_to_compute_data_list"].append(
            (current_time, self._BEGINNING2END_STAMP))

    def _compute_beginning_point_statistics(self, timer):
        '''Computes the current statistics data of such timer.'''
        collected_data_qty = len(
            self.TIMERS[timer]["_statistics"]["_to_compute_data_list"])
        # // Compute deltatimes of the beginning and beginning to end functions stamps:
        _deltatimes_lists = self._compute_deltatimes_between_strobes(
            timer=timer,
            collected_data_qty=collected_data_qty)
        # // The last laps:
        # Beginning to beginning time:
        try:
            self.TIMERS[timer]["_statistics"]["beginning_timer"]["last_lap_time"] = _deltatimes_lists[
                "_beginning_deltatimes"][0]
        except Exception:
            self.TIMERS[timer]["_statistics"]["beginning_timer"]["last_lap_time"] = "N/D"
        # Beginning to end function time:
        try:
            self.TIMERS[timer]["_statistics"]["beginning2end_timer"]["last_lap_time"] = _deltatimes_lists[
                "_beginning2end_deltatimes"][0]
        except Exception:
            self.TIMERS[timer]["_statistics"]["beginning2end_timer"]["last_lap_time"] = "N/D"
        _computed_data = self._compute_statistics_data_from_deltatimes(
            _deltatimes_lists)
        # // The last 10 laps average time:
        # Beginning to beginning time average:
        self.TIMERS[timer]["_statistics"]["beginning_timer"][
            "last_10_laps_average_time"] = _computed_data["10_last_beginning_deltatimes_average"]
        # Beginning to end function time average:
        self.TIMERS[timer]["_statistics"]["beginning2end_timer"][
            "last_10_laps_average_time"] = _computed_data["10_last_beginning2end_deltatimes_average"]
        # // The total laps average time:
        # Beginning to beginning time average:
        self.TIMERS[timer]["_statistics"]["beginning_timer"][
            "total_laps_average_time"] = _computed_data["total_beginning_deltatimes_average"]
        # Beginning to end function time average:
        self.TIMERS[timer]["_statistics"]["beginning2end_timer"][
            "total_laps_average_time"] = _computed_data["total_beginning2end_deltatimes_average"]
        # // Total deltatime laps:
        # Beginning to beginning:
        self.TIMERS[timer]["_statistics"]["beginning_timer"][
            "total_deltatime_laps"] = _computed_data["total_beginning_laps"]
        # Beginning to end function:
        self.TIMERS[timer]["_statistics"]["beginning2end_timer"][
            "total_deltatime_laps"] = _computed_data["total_beginning2end_laps"]
        # // The most delayed lap time:
        # Beginning to beginning:
        self.TIMERS[timer]["_statistics"]["beginning_timer"][
            "most_delayed_lap_time"] = _computed_data["beginning_deltatimes_most_delayed_lap"]
        # Beginning to end function:
        self.TIMERS[timer]["_statistics"]["beginning2end_timer"][
            "most_delayed_lap_time"] = _computed_data["beginning2end_deltatimes_most_delayed_lap"]

    def _compute_statistics_data_from_deltatimes(self, deltatimes_lists):
        '''Compute the statistics according to deltatimes of a function executions.'''
        # // 10 last laps variables:
        # Beginning:
        _10_last_beginning_deltatimes_accumulated = 0
        # It's possible that there are less than 10:
        _10_last_beginning_deltatimes_qty = 0
        # Beginning to end function:
        _10_last_beginning2end_deltatimes_accumulated = 0
        # It's possible that there are less than 10:
        _10_last_beginning2end_deltatimes_qty = 0
        # // Total laps variables:
        # Beginning:
        _total_beginning_deltatimes_accumulated = 0
        # It's possible that there are less than 10:
        _total_beginning_deltatimes_qty = 0
        # Beginning to end function:
        _total_beginning2end_deltatimes_accumulated = 0
        # It's possible that there are less than 10:
        _total_beginning2end_deltatimes_qty = 0
        # // Most delayed lap:
        # Beginning:
        _beginning_most_delayed_lap = 0
        # Beginning to end function:
        _beginning2end_most_delayed_lap = 0
        # // Accumulate deltatimes:
        # Beginning:
        for dt_position in range(len(deltatimes_lists["_beginning_deltatimes"])):
            # 10 last laps:
            if (dt_position <= 10):
                _10_last_beginning_deltatimes_accumulated += deltatimes_lists[
                    "_beginning_deltatimes"][dt_position]
                _10_last_beginning_deltatimes_qty += 1
            # Total laps
            _total_beginning_deltatimes_accumulated += deltatimes_lists["_beginning_deltatimes"][dt_position]
            _total_beginning_deltatimes_qty += 1
            # Most delayed lap:
            if (_beginning_most_delayed_lap < deltatimes_lists["_beginning_deltatimes"][dt_position]):
                _beginning_most_delayed_lap = deltatimes_lists["_beginning_deltatimes"][dt_position]
        # Beginning to end function:
        for dt_position in range(len(deltatimes_lists["_beginning2end_deltatimes"])):
            # 10 last laps:
            if (dt_position <= 10):
                _10_last_beginning2end_deltatimes_accumulated += deltatimes_lists[
                    "_beginning2end_deltatimes"][dt_position]
                _10_last_beginning2end_deltatimes_qty += 1
            # Total laps
            _total_beginning2end_deltatimes_accumulated += deltatimes_lists["_beginning2end_deltatimes"][dt_position]
            _total_beginning2end_deltatimes_qty += 1
            # Most delayed lap:
            if (_beginning2end_most_delayed_lap < deltatimes_lists["_beginning2end_deltatimes"][dt_position]):
                _beginning2end_most_delayed_lap = deltatimes_lists[
                    "_beginning2end_deltatimes"][dt_position]
        # // Get averages:
        # 10 last laps:
        try:
            _10_last_beginning_deltatimes_average = _10_last_beginning_deltatimes_accumulated / \
                _10_last_beginning_deltatimes_qty
        except Exception:
            _10_last_beginning_deltatimes_average = "N/D"
        try:
            _10_last_beginning2end_deltatimes_average = _10_last_beginning2end_deltatimes_accumulated / \
                _10_last_beginning2end_deltatimes_qty
        except Exception:
            _10_last_beginning2end_deltatimes_average = "N/D"
        # Total laps:
        try:
            _total_beginning_deltatimes_average = _total_beginning_deltatimes_accumulated / \
                _total_beginning_deltatimes_qty
        except Exception:
            _total_beginning_deltatimes_average = "N/D"
        try:
            _total_beginning2end_deltatimes_average = _total_beginning2end_deltatimes_accumulated / \
                _total_beginning2end_deltatimes_qty
        except Exception:
            _total_beginning2end_deltatimes_average = "N/D"
        return {
            "10_last_beginning_deltatimes_average": _10_last_beginning_deltatimes_average,
            "10_last_beginning2end_deltatimes_average": _10_last_beginning2end_deltatimes_average,
            "total_beginning_deltatimes_average": _total_beginning_deltatimes_average,
            "total_beginning2end_deltatimes_average": _total_beginning2end_deltatimes_average,
            "total_beginning_laps": _total_beginning_deltatimes_qty,
            "total_beginning2end_laps": _total_beginning2end_deltatimes_qty,
            "beginning_deltatimes_most_delayed_lap": _beginning_most_delayed_lap,
            "beginning2end_deltatimes_most_delayed_lap": _beginning2end_most_delayed_lap
        }

    def _compute_deltatimes_between_strobes(self, timer, collected_data_qty):
        '''Compute de differences between contiguous strobes, from the last to the first.'''
        _beginning_deltatimes = []
        _beginning2end_deltatimes = []
        _ordered_lists_for_types_stamps = self._filter_b_and_b2e_lists(
            timer=timer,
            collected_data_qty=collected_data_qty)
        # Beginning deltatimes:
        for b_ts_position in range(0, (len(_ordered_lists_for_types_stamps["_beginning_timestamps"]) - 1), 1):
            r = _ordered_lists_for_types_stamps["_beginning_timestamps"][
                b_ts_position] - _ordered_lists_for_types_stamps["_beginning_timestamps"][b_ts_position + 1]
            _beginning_deltatimes.append(r)
        # Beginning to end function deltatimes:
        for b2e_ts_position_tuple in _ordered_lists_for_types_stamps["_beginning2end_timestamps_tuples"]:
            r = b2e_ts_position_tuple[0] - b2e_ts_position_tuple[1]
            _beginning2end_deltatimes.append(r)
        return {
            "_beginning_deltatimes": _beginning_deltatimes,
            "_beginning2end_deltatimes": _beginning2end_deltatimes
        }

    def _filter_b_and_b2e_lists(self, timer, collected_data_qty):
        '''Filter the list into 2 lists:
        1. Beginning stamps list.
        2. Beginning to end function stamps list.'''
        _beginning_timestamps = []
        _beginning2end_timestamps_tuples = []
        for timestamp_position in range((collected_data_qty - 1), -1, -1):
            # // Fill the lists:
            # Beginning to beginning stamps:
            if (self.TIMERS[timer]["_statistics"]["_to_compute_data_list"][
                    timestamp_position][1] == self._BEGINNING_STAMP):
                # Insert stamp on list:
                _beginning_timestamps.append(self.TIMERS[timer][
                    "_statistics"]["_to_compute_data_list"][timestamp_position][0])
            # Beginning to end function stamps tuples:
            elif (self.TIMERS[timer]["_statistics"]["_to_compute_data_list"][
                    timestamp_position][1] == self._BEGINNING2END_STAMP):
                # Insert stamp on list:
                b2e_ts = self.TIMERS[timer]["_statistics"]["_to_compute_data_list"][
                    timestamp_position][0]
                b_ts = None
                # Seek the previous beginning stamp:
                try:
                    for prev_beginning_timestamp_position in range((timestamp_position - 1), -1, -1):
                        if (self.TIMERS[timer]["_statistics"]["_to_compute_data_list"][
                                prev_beginning_timestamp_position][1] == self._BEGINNING_STAMP):
                            b_ts = self.TIMERS[timer]["_statistics"]["_to_compute_data_list"][
                                prev_beginning_timestamp_position][0]
                            break
                except Exception as e:
                    # Probably there is no more data:
                    pass
                # There is a full beginning2end stamps tuple:
                if (b_ts != None):
                    _beginning2end_timestamps_tuples.append(
                        (b2e_ts, b_ts))
        # Clean the used timestamps data:
        for timestamp_position in range(collected_data_qty):
            self.TIMERS[timer]["_statistics"]["_to_compute_data_list"].pop(0)
        # self._logger.debug("Data to compute queue length: {}".format(
        #     len(self.TIMERS[timer]["_statistics"]["_to_compute_data_list"])))
        return {
            "_beginning_timestamps": _beginning_timestamps,
            "_beginning2end_timestamps_tuples": _beginning2end_timestamps_tuples
        }

    def end_track(self, timer):
        '''Ends the tracking of a thread or periodic function.'''
        if (self.TIMERS != None):
            # self._logger.debug("Finish the check the {} watchdog timer...".format(timer))
            self.TIMERS[timer]["_tracker"]["on_flag"] = False
        else:
            pass

    def serve(self):
        '''Execute the watchdogs (timers) fleet. It must be thrown into a dedicated thread or process.'''
        if (self.TIMERS != None):
            for timer_name, timer_config in self.TIMERS.items():
                # Compute the statistics:
                self._compute_beginning_point_statistics(timer_name)
                # Expose statistics (debug mode):
                self._logger.debug("{}: {}: {}:: {}".format(
                    self._target_class_name,
                    timer_name,
                    "Beginning point",
                    timer_config["_statistics"]["beginning_timer"]))
                self._logger.debug("{}: {}: {}:: {}".format(
                    self._target_class_name,
                    timer_name,
                    "Beginning to end function",
                    timer_config["_statistics"]["beginning2end_timer"]))
                # Check for errors:
                if (timer_config["_tracker"]["on_flag"] == True):
                    # Begin points:
                    _current_beginning_lap_time = time.time(
                    ) - timer_config["_tracker"]["beginning_time"]
                    _current_beginning2end_lap_time = time.time(
                    ) - timer_config["_tracker"]["endpoint_function_time"]
                    if (_current_beginning_lap_time > timer_config["error_timer_value"]):
                        self._throw_error_message(
                            timer_name=timer_name,
                            tracking_type="Beginning point",
                            current_lap_time=_current_beginning_lap_time)
                    elif (_current_beginning_lap_time > timer_config["warning_timer_value"]):
                        self._throw_warning_message(
                            timer_name=timer_name,
                            tracking_type="Beginning point",
                            current_lap_time=_current_beginning_lap_time)
                    # End points:
                    if (_current_beginning2end_lap_time > timer_config["error_start2end_function_timer_value"]):
                        self._throw_error_message(
                            timer_name=timer_name,
                            tracking_type="Beginning to end function",
                            current_lap_time=_current_beginning2end_lap_time)
                    elif (_current_beginning2end_lap_time > timer_config["warning_start2end_function_timer_value"]):
                        self._throw_warning_message(
                            timer_name=timer_name,
                            tracking_type="Beginning to end function",
                            current_lap_time=_current_beginning2end_lap_time)
            return
        self._logger.info("There is not any health watchdogs setted on an instance of the class {}.".format(
            self._target_class_name))

    def shutdown(self):
        self.TIMERS = None

    def _throw_error_message(
            self,
            timer_name,
            tracking_type,
            current_lap_time):
        msg = "UNHEALTHY: tracking type: {}: {}: {}:: current lap time: {}".format(
            tracking_type,
            self._target_class_name,
            timer_name,
            current_lap_time)
        if (self._diagnostics_callback != None):
            self._diagnostics_callback(msg)
            self._logger.debug(msg)
        else:
            self._logger.error(msg)

    def _throw_warning_message(
            self,
            timer_name,
            tracking_type,
            current_lap_time):
        msg = "DELAYED: tracking type: {}: {}: {}:: current lap time: {}".format(
            tracking_type,
            self._target_class_name,
            timer_name,
            current_lap_time)
        if (self._diagnostics_callback != None):
            self._diagnostics_callback(msg)
            self._logger.debug(msg)
        else:
            self._logger.warning(msg)
