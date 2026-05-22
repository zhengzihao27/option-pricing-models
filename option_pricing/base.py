from enum import Enum
from abc import ABC, abstractmethod

class OPTION_TYPE(Enum):
    CALL_OPTION = 'Call Option'
    PUT_OPTION = 'Put Option'

class OptionPricingModel(ABC):
    """定义期权定价模型接口的抽象类。"""

    def calculate_option_price(self, option_type):
        """根据指定期权类型计算看涨或看跌期权价格。"""
        if option_type == OPTION_TYPE.CALL_OPTION.value:
            return self._calculate_call_option_price()
        elif option_type == OPTION_TYPE.PUT_OPTION.value:
            return self._calculate_put_option_price()
        else:
            return -1

    @classmethod
    @abstractmethod
    def _calculate_call_option_price(cls):
        """计算看涨期权价格。"""
        pass

    @classmethod
    @abstractmethod
    def _calculate_put_option_price(cls):
        """计算看跌期权价格。"""
        pass
