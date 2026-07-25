from enum import Enum


class CaseStage(str, Enum):
    IDEA = 'idea'
    VALIDATION = 'validation'
    PROTOTYPE = 'prototype'
    MVP = 'mvp'
    LAUNCHED = 'launched'
