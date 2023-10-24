import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

class LoggerUtil:
    @staticmethod
    def log_method_start(method_name, input_parameter=None, api_name=None):
        builder = f"****Method Starts**** \n ****Method Name***** {method_name}"
        if input_parameter is not None:
            builder = f"{builder} ***Input parameters: {input_parameter} ***Api Name: {api_name}"

        logger.info(builder)

    @staticmethod
    def log_method_end(method_name, ret_value):
        builder = f"***Method Returned***: {method_name}"
        if ret_value is None:
            builder = f"{builder} null return value - *****POTENTIAL CODE ISSUE*****"
        else:
            builder = f"{builder} return value {ret_value}"

        logger.debug(builder)

    @staticmethod
    def info(message):
        logger.info(f"Info message: {message}")

    @staticmethod
    def debug(message, value):
        logger.debug(f"Debug message: {message} Debug value: {value}")

    @staticmethod
    def error(message):
        logger.error(f"Error message: {message}")

    @staticmethod
    def log_exception(method_name, exception=None, var_args=None):
        builder = "Exception was observed: "

        if var_args is not None:
            builder = f"{builder} ***Object's state when exception occurred : *** Message for *** {method_name}() " \
                      f"Args {var_args}"

        if exception is not None:
            logger.error(f"{builder} {exception}")
        else:
            logger.error(builder)
