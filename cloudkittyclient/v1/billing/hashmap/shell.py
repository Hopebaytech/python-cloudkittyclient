# Copyright 2015 Objectif Libre
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cloudkittyclient.common import utils
from cloudkittyclient import exc


@utils.arg('-n', '--name',
           help='Service name',
           required=True)
def do_hashmap_service_create(cc, args={}):
    """Create a service."""
    arg_to_field_mapping = {
        'name': 'name'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap_services.create(**fields)
    utils.print_dict(out.to_dict())


def do_hashmap_service_list(cc, args={}):
    """List services."""
    try:
        services = cc.hashmap_services.list()
    except exc.HTTPNotFound:
        raise exc.CommandError('Services not found: %s' % args.counter_name)
    else:
        field_labels = ['Name', 'Service id']
        fields = ['name', 'service_id']
        utils.print_list(services, fields, field_labels,
                         sortby=0)


@utils.arg('-s', '--service-id',
           help='Service uuid',
           required=True)
def do_hashmap_service_delete(cc, args={}):
    """Delete a service."""
    try:
        cc.hashmap_services.delete(service_id=args.service_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Service not found: %s' % args.counter_name)


@utils.arg('-n', '--name',
           help='Field name',
           required=True)
@utils.arg('-s', '--service-id',
           help='Service id',
           required=True)
def do_hashmap_field_create(cc, args={}):
    """Create a field."""
    arg_to_field_mapping = {
        'name': 'name',
        'service_id': 'service_id'
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap_fields.create(**fields)
    utils.print_dict(out.to_dict())


@utils.arg('-s', '--service-id',
           help='Service id',
           required=True)
def do_hashmap_field_list(cc, args={}):
    """Create a field."""
    try:
        created_field = cc.hashmap_fields.list(service_id=args.service_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Fields not found: %s' % args.counter_name)
    else:
        field_labels = ['Name', 'Field id']
        fields = ['name', 'field_id']
        utils.print_list(created_field, fields, field_labels,
                         sortby=0)


@utils.arg('-f', '--field-id',
           help='Field uuid',
           required=True)
def do_hashmap_field_delete(cc, args={}):
    """Delete a field."""
    try:
        cc.hashmap_fields.delete(field_id=args.field_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Field not found: %s' % args.counter_name)


@utils.arg('-c', '--cost',
           help='Mapping cost',
           required=True)
@utils.arg('-v', '--value',
           help='Mapping value',
           required=False)
@utils.arg('-t', '--type',
           help='Mapping type (flat, rate)',
           required=False)
@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@utils.arg('-g', '--group-id',
           help='Group id',
           required=False)
def do_hashmap_mapping_create(cc, args={}):
    """Create a ampping."""
    arg_to_field_mapping = {
        'cost': 'cost',
        'value': 'value',
        'type': 'type',
        'service_id': 'service_id',
        'field_id': 'field_id',
        'group_id': 'group_id',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    out = cc.hashmap_mappings.create(**fields)
    utils.print_dict(out)


@utils.arg('-m', '--mapping-id',
           help='Mapping id',
           required=True)
@utils.arg('-c', '--cost',
           help='Mapping cost',
           required=False)
@utils.arg('-v', '--value',
           help='Mapping value',
           required=False)
@utils.arg('-t', '--type',
           help='Mapping type (flat, rate)',
           required=False)
@utils.arg('-g', '--group-id',
           help='Group id',
           required=False)
def do_hashmap_mapping_update(cc, args={}):
    """Update a mapping."""
    arg_to_field_mapping = {
        'mapping_id': 'mapping_id',
        'cost': 'cost',
        'value': 'value',
        'type': 'type',
        'group_id': 'group_id',
    }
    try:
        mapping = cc.hashmap_mappings.get(mapping_id=args.mapping_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Modules not found: %s' % args.counter_name)
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                setattr(mapping, k, v)
    cc.hashmap_mappings.update(**mapping.dirty_fields)


@utils.arg('-s', '--service-id',
           help='Service id',
           required=False)
@utils.arg('-f', '--field-id',
           help='Field id',
           required=False)
@utils.arg('-g', '--group-id',
           help='Group id',
           required=False)
def do_hashmap_mapping_list(cc, args={}):
    """List mappings."""
    if args.service_id is None and args.field_id is None:
        raise exc.CommandError("Provide either service-id or field-id")
    try:
        mappings = cc.hashmap_mappings.list(service_id=args.service_id,
                                            field_id=args.field_id,
                                            group_id=args.group_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Mapping not found: %s' % args.counter_name)
    else:
        field_labels = ['Mapping id', 'Value', 'Cost',
                        'Type', 'Field id',
                        'Service id', 'Group id']
        fields = ['mapping_id', 'value', 'cost',
                  'type', 'field_id',
                  'service_id', 'group_id']
        utils.print_list(mappings, fields, field_labels,
                         sortby=0)


@utils.arg('-m', '--mapping-id',
           help='Mapping uuid',
           required=True)
def do_hashmap_mapping_delete(cc, args={}):
    """Delete a mapping."""
    try:
        cc.hashmap_mappings.delete(mapping_id=args.mapping_id)
    except exc.HTTPNotFound:
        raise exc.CommandError('Mapping not found: %s' % args.mapping_id)


@utils.arg('-n', '--name',
           help='Group name',
           required=True)
def do_hashmap_group_create(cc, args={}):
    """Create a group."""
    arg_to_field_mapping = {
        'name': 'name',
    }
    fields = {}
    for k, v in vars(args).items():
        if k in arg_to_field_mapping:
            if v is not None:
                fields[arg_to_field_mapping.get(k, k)] = v
    cc.hashmap_groups.create(**fields)


def do_hashmap_group_list(cc, args={}):
    """List groups."""
    try:
        groups = cc.hashmap_groups.list()
    except exc.HTTPNotFound:
        raise exc.CommandError('Mapping not found: %s' % args.counter_name)
    else:
        field_labels = ['Name',
                        'Group id']
        fields = ['name', 'group_id']
        utils.print_list(groups, fields, field_labels,
                         sortby=0)


@utils.arg('-g', '--group-id',
           help='Group uuid',
           required=True)
@utils.arg('-r', '--recursive',
           help="""Delete the group's mappings""",
           required=False,
           default=False)
def do_hashmap_group_delete(cc, args={}):
    """Delete a group."""
    try:
        cc.hashmap_groups.delete(group_id=args.group_id,
                                 recursive=args.recursive)
    except exc.HTTPNotFound:
        raise exc.CommandError('Group not found: %s' % args.group_id)
