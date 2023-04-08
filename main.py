from unification import parse, unification
from typing import List, Tuple, Dict, Callable
from copy import deepcopy
import math
import numpy as np


def forward_planner(start_state: List, goal: List, actions: Dict, debug=False) -> List:
    plan = []
    for key, values in actions.items():
        for key1, values1 in values.items():
            if key1 == 'action':
                continue
            elif key1 == 'conditions':
                for val in values1:
                    temp = parse(val)
                    for expression in start_state:
                        temp2 = parse(expression)
                        result = unification(temp2, temp)
                        if not result:
                            continue
                        else:
                            plan.append(apply_result(temp2, temp, result))
    final_plan = create_output(plan)
    return final_plan


def create_output(plan: List) -> List:
    new_plan = []
    for el in plan:
        for tup in el:
            if len(tup) == 2:
                new_plan.append('(' + tup[0] + ' ' + tup[1] + ')')
            else:
                new_plan.append('(' + tup[0] + ' ' + tup[1] + ' ' + tup[2] + ')')
    return new_plan


def apply_result(list_expression1, list_expression2, result) -> Tuple[List[str], List[str]]:
    if result:
        key = list(result.keys())[0]
        value = list(result.values())[0]
        if type(value) is list:
            result[key] = '(' + ' '.join(value) + ')'
        if type(list_expression1) is str:
            _range = range(len(list_expression2))
        else:
            _range = range(len(list_expression1))
        for i in _range:
            if type(list_expression1[i]) is list or type(list_expression2[i]) is list:
                list_expression1[i], list_expression2[i] = apply_result(list_expression1[i], list_expression2[i],
                                                                        result)
            if list_expression1[i] == list(result.keys())[0]: list_expression1[i] = list(result.values())[0]
            if list_expression2[i] == list(result.keys())[0]: list_expression2[i] = list(result.values())[0]
        return list_expression1, list_expression2
    return list_expression1, list_expression2


def list_check(parsed_expression: List):
    if isinstance(parsed_expression, list):
        return parsed_expression
    return [parsed_expression]


def unify(s_expression1, s_expression2):
    list_expression1 = list_check(s_expression1)
    list_expression2 = list_check(s_expression2)
    return unification(list_expression1, list_expression2)


if __name__ == "__main__":
    start_state = [
        "(item Saw)",
        "(item Drill)",
        "(place Home)",
        "(place Store)",
        "(place Bank)",
        "(agent Me)",
        "(at Me Home)",
        "(at Saw Store)",
        "(at Drill Store)"
    ]

    goal = [
        "(item Saw)",
        "(item Drill)",
        "(place Home)",
        "(place Store)",
        "(place Bank)",
        "(agent Me)",
        "(at Me Home)",
        "(at Drill Me)",
        "(at Saw Store)"
    ]

    actions = {
        "drive": {
            "action": "(drive ?agent ?from ?to)",
            "conditions": [
                "(agent ?agent)",
                "(place ?from)",
                "(place ?to)",
                "(at ?agent ?from)"
            ],
            "add": [
                "(at ?agent ?to)"
            ],
            "delete": [
                "(at ?agent ?from)"
            ]
        },
        "buy": {
            "action": "(buy ?purchaser ?seller ?item)",
            "conditions": [
                "(item ?item)",
                "(place ?seller)",
                "(agent ?purchaser)",
                "(at ?item ?seller)",
                "(at ?purchaser ?seller)"
            ],
            "add": [
                "(at ?item ?purchaser)"
            ],
            "delete": [
                "(at ?item ?seller)"
            ]
        }
    }

    plan = forward_planner(start_state, goal, actions)
    for el in plan:
        print(el)
