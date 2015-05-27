from django.test import TestCase
from django.db import DataError

# Create your tests here.
from core.dynamic.models import *
from core.dynamic.models.fields import *

Animal = Model.objects.create(name='Animal')

Field.objects.create(name='name', type=CHAR, model=Animal)
Field.objects.create(name='legs', type=INT, model=Animal)
Field.objects.create(name='colour', type=CHAR, model=Animal)
Field.objects.create(name='species', type=CHAR, model=Animal)

class ModelTestCase(TestCase):

    def test_model_creation(self):
        Animal = Model.objects.get(name='Animal')
        print Animal.model._meta.fields
        self.assertTrue(Animal.table_exists)

    def test_field_creation(self):
        #Animal = Model.objects.create(name='Animal')
        Animal = Model.objects.get(name='Animal')
        age = Field.objects.create(name='age', type=INT, model=Animal)

        Animal.model.objects.create(name='Cat', age=5)
        self.assertEqual(Animal.model.objects.get(name='Cat').age, 5)

    def test_base_field_modification(self):
        Animal = Model.objects.get(name='Animal')

        legs = Field.objects.get(name='legs')
        legs.type = CHAR
        legs.save()

        animal = Animal.model.objects.create(name='dog', legs='four')
        self.assertEqual(Animal.model.objects.get(pk=animal.pk).legs, 'four')

    def test_extended_field_modification(self):
        Animal = Model.objects.get(name='Animal')
        colour = Field.objects.get(name='colour')

        extended = CharField.objects.get(field=colour)
        extended.max_length = 5
        extended.save()

        animal = Animal.model
        animal.objects.create(colour='red')

        with self.assertRaises(DataError) as context:
            animal.objects.create(colour='purple')

    def test_field_deletion(self):
        Animal = Model.objects.get(name='Animal')
        animal = Animal.model

        print an

        animal.objects.create(name='Bee', species='Hymenoptera')

        Field.objects.get(name='species').delete()

        with self.assertRaises(TypeError) as context:
            animal.objects.create(name='Bat', species='Chiroptera')



    # def test_database_table_create(self):
    #
    #     # ensure creating Model row creates a new database table
    #     model = Model.objects.get(name='animal')
    #     self.assertTrue(model.table_exists)
    #
    # def test_field_create(self):
    #     model = Model.objects.get(name='animal')
    #
    #     # create new field
    #     field = Field(name='name', type=CHAR, model=model)
    #     field.save()
    #
    #     # save row with new field
    #     obj = model.model.objects.create(name='Cat')
    #     obj.save()
    #
    #     # using wrong field name raises error
    #     with self.assertRaises(TypeError) as context:
    #         obj = model.model.objects.create(type='Cat')
    #         obj.save()
    #
    # def test_field_type_change(self):
    #     model = Model.objects.get(name='animal')
    #
    #     field = Field(name='name', type=CHAR, model=model)
    #     field.save()
    #
    #     field = Field(name='legs', type=INT, model=model)
    #     field.save()
    #
    #     obj = model.model.objects.create(name='Human', legs=2)
    #     obj.save()
    #
    #     # change int to char field
    #     field.type = CHAR
    #     field.save()
    #
    #     # ensure char is now returned
    #     obj = model.model.objects.get(name='Human')
    #     self.assertIsInstance(obj.legs, basestring)
    #
    #     # char cannot be casted to int field
    #     with self.assertRaises(ProgrammingError) as context:
    #         field.type = INT
    #         field.save()
    #
    # def test_field_extended_opt_change(self):
    #
    #     model = Model.objects.get(name='animal')
    #
    #     field = Field(name='name', type=CHAR, model=model)
    #     field.save()
    #
    #     field = Field(name='description', type=CHAR, model=model)
    #     field.save()
    #
    #     obj = model.model.objects.create(name='Dog', description='Mans best friend')
    #     obj.save()
    #
    #     # ensure data returned is as expected
    #     obj = model.model.objects.get(name='Dog')
    #     self.assertTrue(obj.description, 'Mans best friend')
    #
    #     # change field length and update database
    #     extended_opts = field.specific
    #     extended_opts.max_length = 16
    #     extended_opts.save()
    #
    #     # too long data fails to save
    #     obj.description = 'Man and womens best friend'
    #     with self.assertRaises(DataError) as context:
    #         obj.save()
    #
    # def test_model_inheritance(self):
    #     # add fields to animal
    #     model = Model.objects.get(name='animal')
    #
    #     field = Field(name='name', type=CHAR, model=model)
    #     field.save()
    #
    #     # add fields to cat
    #     model = Model.objects.get(name='cat')
    #
    #     field = Field(name='colour', type=CHAR, model=model)
    #     field.save()
    #
    #     obj = model.model.objects.create(name='Siamese', colour='Grey')
    #
    #     # ensure animal fields are accessible/saved from cat
    #     self.assertEqual(model.model.objects.get(name='Siamese').colour, 'Grey')
    #
    # def test_foreign_key_relation(self):
    #     person = Model(name='person')
    #     person.save()
    #
    #     phone = Model(name='phone')
    #     phone.save()
    #
    #     Field.objects.create(name='name', type=CHAR, model=person)
    #     Field.objects.create(name='number', type=CHAR, model=phone)
    #     Relation.objects.create(name='person', type=FOREIGN_KEY, related_model=person, model=phone)
    #
    #     person = Model.objects.get(name='person')
    #     phone = Model.objects.get(name='phone')
    #
    #     pobj = person.model(name='Tim')
    #     pobj.save()
    #
    #     print person.model.objects.all()[0].name
    #     print pobj
    #
    #     ph = phone.model(number='123456789')
    #     ph.save()
    #
    #     ph.person = pobj
    #     ph.save()


