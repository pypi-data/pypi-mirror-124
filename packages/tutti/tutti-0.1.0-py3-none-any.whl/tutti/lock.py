#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Hamilton Kibbe <ham@hamiltonkib.be>

"""Base class for distributed lock"""
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type


class LockABC(ABC):

    @abstractmethod
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        pass

    @abstractmethod
    def release(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> "LockABC":
        pass

    @abstractmethod
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> Optional[bool]:
        pass

class SemaphoreABC(ABC):

    @abstractmethod
    def acquire(self, blocking: bool = True, timeout: Optional[float] = None) -> bool:
        pass

    @abstractmethod
    def release(self, n: int = 1) -> None:
        pass