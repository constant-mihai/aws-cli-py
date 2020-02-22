#!/bin/python3
# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2
from PyInquirer import Validator, ValidationError


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    # if answers['size'] == 'jumbo':
    #     options.append('helicopter')
    return options

class FilterValidator(Validator):
    def validate(self, document):
        print("TODO")

def ask_for_tags():
    search_filter = [
        {
            'type': 'input',
            'name': 'filter',
            'message': "What would you like to filter by? E.g.: 'tag:Squad'",
            'validate': FilterValidator 
        }
    ]

    return prompt(search_filter, style=custom_style_2)


def ask_for_selection(choices):
    selection = [ 
        {
            'type': 'list',
            'name': 'action',
            'message': 'Select action to perform:',
            'choices': ['ssm', 'ssh'],
        },
        {
            'type': 'list',
            'name': 'selection',
            'message': 'Select the EC2 instance:',
            'choices': choices,
        },
    ]

    selection_answers = prompt(selection, style=custom_style_2)

    pprint(answers)
