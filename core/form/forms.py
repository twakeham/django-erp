# Copyright (c) 2009-2011, Carl Meyer and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of the author nor the names of other
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals
from copy import deepcopy

from django import forms
from django.forms.util import flatatt, ErrorDict
from django.utils import six
from django.utils.safestring import mark_safe


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass.
    I'm not sure exactly why this is needed, but the implementation in six
    changed (see
    https://github.com/django/django/commit/a2340ac6d6b7e31c7e97e8fdaf3e1d73e43b24ba)
    and the new version doesn't work here.
    """
    return meta(str("NewBase"), bases, {})


class Fieldset(object):
    """An iterable Fieldset with a legend and a set of BoundFields."""
    def __init__(self, form, name, boundfields, legend='', classes='',
                 description=''):
        self.form = form
        self.boundfields = boundfields
        if legend is None:
            legend = name
        self.legend = legend and mark_safe(legend)
        self.classes = classes
        self.description = mark_safe(description)
        self.name = name

    def _errors(self):
        return ErrorDict(((k, v) for (k, v) in six.iteritems(self.form.errors)
                          if k in [f.name for f in self.boundfields]))
    errors = property(_errors)

    def __iter__(self):
        for bf in self.boundfields:
            yield _mark_row_attrs(bf, self.form)

    def __repr__(self):
        return "%s('%s', %s, legend='%s', classes='%s', description='%s')" % (
            self.__class__.__name__, self.name,
            [f.name for f in self.boundfields], self.legend, self.classes,
            self.description)


class FieldsetCollection(object):
    def __init__(self, form, fieldsets):
        self.form = form
        self.fieldsets = fieldsets
        self._cached_fieldsets = []

    def __len__(self):
        return len(self.fieldsets) or 1

    def __iter__(self):
        if not self._cached_fieldsets:
            self._gather_fieldsets()
        for field in self._cached_fieldsets:
            yield field

    def __getitem__(self, key):
        if not self._cached_fieldsets:
            self._gather_fieldsets()
        for field in self._cached_fieldsets:
            if field.name == key:
                return field
        raise KeyError

    def _gather_fieldsets(self):
        if not self.fieldsets:
            self.fieldsets = (('main', {'fields': self.form.fields.keys(),
                                        'legend': ''}),)
        for name, options in self.fieldsets:
            try:
                field_names = [n for n in options['fields']
                               if n in self.form.fields]
            except KeyError:
                message = "Fieldset definition must include 'fields' option."
                raise ValueError(message)
            boundfields = [forms.forms.BoundField(self.form,
                                                  self.form.fields[n], n)
                           for n in field_names]
            self._cached_fieldsets.append(Fieldset(self.form, name,
                boundfields, options.get('legend', None),
                ' '.join(options.get('classes', ())),
                options.get('description', '')))


def _get_meta_attr(attrs, attr, default):
    try:
        ret = getattr(attrs['Meta'], attr)
    except (KeyError, AttributeError):
        ret = default
    return ret


def _set_meta_attr(attrs, attr, value):
    try:
        setattr(attrs['Meta'], attr, value)
        return True
    except KeyError:
        return False


def get_fieldsets(bases, attrs):
    """Get the fieldsets definition from the inner Meta class."""
    fieldsets = _get_meta_attr(attrs, 'fieldsets', None)
    if fieldsets is None:
        #grab the fieldsets from the first base class that has them
        for base in bases:
            fieldsets = getattr(base, 'base_fieldsets', None)
            if fieldsets is not None:
                break
    fieldsets = fieldsets or []
    return fieldsets


def get_fields_from_fieldsets(fieldsets):
    """Get a list of all fields included in a fieldsets definition."""
    fields = []
    try:
        for name, options in fieldsets:
            fields.extend(options['fields'])
    except (TypeError, KeyError):
        raise ValueError('"fieldsets" must be an iterable of two-tuples, '
                         'and the second tuple must be a dictionary '
                         'with a "fields" key')
    return fields or None


def get_row_attrs(bases, attrs):
    """Get the row_attrs definition from the inner Meta class."""
    return _get_meta_attr(attrs, 'row_attrs', {})


def _mark_row_attrs(bf, form):
    row_attrs = deepcopy(form._row_attrs.get(bf.name, {}))
    if bf.field.required:
        req_class = 'required'
    else:
        req_class = 'optional'
    if bf.errors:
        req_class += ' error'
    if 'class' in row_attrs:
        row_attrs['class'] = row_attrs['class'] + ' ' + req_class
    else:
        row_attrs['class'] = req_class
    bf.row_attrs = mark_safe(flatatt(row_attrs))
    return bf


class BetterFormBaseMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['base_fieldsets'] = get_fieldsets(bases, attrs)
        fields = get_fields_from_fieldsets(attrs['base_fieldsets'])
        if (_get_meta_attr(attrs, 'fields', None) is None and
            _get_meta_attr(attrs, 'exclude', None) is None):
            _set_meta_attr(attrs, 'fields', fields)
        attrs['base_row_attrs'] = get_row_attrs(bases, attrs)

        new_class = super(BetterFormBaseMetaclass,
                          cls).__new__(cls, name, bases, attrs)
        return new_class


class BetterFormMetaclass(BetterFormBaseMetaclass,
                          forms.forms.DeclarativeFieldsMetaclass):
    pass


class BetterModelFormMetaclass(BetterFormBaseMetaclass,
                               forms.models.ModelFormMetaclass):
    pass


class BetterBaseForm(object):
    """
    ``BetterForm`` and ``BetterModelForm`` are subclasses of Form
    and ModelForm that allow for declarative definition of fieldsets
    and row_attrs in an inner Meta class.
    The row_attrs declaration is a dictionary mapping field names to
    dictionaries of attribute/value pairs.  The attribute/value
    dictionaries will be flattened into HTML-style attribute/values
    (i.e. {'style': 'display: none'} will become ``style="display:
    none"``), and will be available as the ``row_attrs`` attribute of
    the ``BoundField``.  Also, a CSS class of "required" or "optional"
    will automatically be added to the row_attrs of each
    ``BoundField``, depending on whether the field is required.
    There is no automatic inheritance of ``row_attrs``.
    The fieldsets declaration is a list of two-tuples very similar to
    the ``fieldsets`` option on a ModelAdmin class in
    ``django.contrib.admin``.
    The first item in each two-tuple is a name for the fieldset, and
    the second is a dictionary of fieldset options.
    Valid fieldset options in the dictionary include:
    ``fields`` (required): A tuple of field names to display in this
    fieldset.
    ``classes``: A list of extra CSS classes to apply to the fieldset.
    ``legend``: This value, if present, will be the contents of a ``legend``
    tag to open the fieldset.
    ``description``: A string of optional extra text to be displayed
    under the ``legend`` of the fieldset.
    When iterated over, the ``fieldsets`` attribute of a
    ``BetterForm`` (or ``BetterModelForm``) yields ``Fieldset``s.
    Each ``Fieldset`` has a ``name`` attribute, a ``legend``
    attribute, , a ``classes`` attribute (the ``classes`` tuple
    collapsed into a space-separated string), and a description
    attribute, and when iterated over yields its ``BoundField``s.
    Subclasses of a ``BetterForm`` will inherit their parent's
    fieldsets unless they define their own.
    A ``BetterForm`` or ``BetterModelForm`` can still be iterated over
    directly to yield all of its ``BoundField``s, regardless of
    fieldsets.
    """
    def __init__(self, *args, **kwargs):
        self._fieldsets = deepcopy(self.base_fieldsets)
        self._row_attrs = deepcopy(self.base_row_attrs)
        self._fieldset_collection = None
        super(BetterBaseForm, self).__init__(*args, **kwargs)

    @property
    def fieldsets(self):
        if not self._fieldset_collection:
            self._fieldset_collection = FieldsetCollection(
                self, self._fieldsets)
        return self._fieldset_collection

    def __iter__(self):
        for bf in super(BetterBaseForm, self).__iter__():
            yield _mark_row_attrs(bf, self)

    def __getitem__(self, name):
        bf = super(BetterBaseForm, self).__getitem__(name)
        return _mark_row_attrs(bf, self)


class FieldsetForm(with_metaclass(BetterFormMetaclass, BetterBaseForm),
                 forms.Form):
    __doc__ = BetterBaseForm.__doc__


class FieldsetModelForm(with_metaclass(BetterModelFormMetaclass,
                                     BetterBaseForm), forms.ModelForm):
    __doc__ = BetterBaseForm.__doc__


class BasePreviewFormMixin(object):
    """
    Mixin to add preview functionality to a form.  If the form is submitted
    with the following k/v pair in its ``data`` dictionary:
        'submit': 'preview'    (value string is case insensitive)
    Then ``PreviewForm.preview`` will be marked ``True`` and the form will
    be marked invalid (though this invalidation will not put an error in
    its ``errors`` dictionary).
    """
    def __init__(self, *args, **kwargs):
        super(BasePreviewFormMixin, self).__init__(*args, **kwargs)
        self.preview = self.check_preview(kwargs.get('data', None))

    def check_preview(self, data):
        if data and data.get('submit', '').lower() == u'preview':
            return True
        return False

    def is_valid(self, *args, **kwargs):
        if self.preview:
            return False
        return super(BasePreviewFormMixin, self).is_valid()


class PreviewModelForm(BasePreviewFormMixin, FieldsetModelForm):
    pass


class PreviewForm(BasePreviewFormMixin, FieldsetForm):
    pass