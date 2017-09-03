# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from Audits.models import *
import json
import os


class IndexTestCase(TestCase):
    def setUp(self):
        Permission.objects.create(codename='gestor', name='Gestor', content_type_id = 4)
        Permission.objects.create(codename='user', name='User', content_type_id = 4)
        Permission.objects.create(codename='auditor', name='Auditor', content_type_id = 4)

        permission = Permission.objects.get(codename='gestor')
        user = User.objects.create_user('gestor','diego_gn@hotmail.es','gestor')
        user.user_permissions.add(permission)
        gestor = user

        user = User.objects.create_user('gestor2','diego_gn@hotmail.es','gestor2')
        user.user_permissions.add(permission)

        usuario = User.objects.create_user('usuario', 'diego@hotmail.es', 'usuario')
        usuario.user_permissions.add(Permission.objects.get(codename='user'))


        User.objects.create_user('usuario2', 'diego@hotmail.es', 'usuario2').\
            user_permissions.add(Permission.objects.get(codename='user'))

        auditor = User.objects.create_user('auditor', 'diego@hotmail.es', 'auditor')
        auditor.user_permissions.add(Permission.objects.get(codename='auditor'))

        User.objects.create_user('auditor2', 'diego@hotmail.es', 'auditor2').\
            user_permissions.add(Permission.objects.get(codename='auditor'))
        #Creamos la auditoría a editar y luego borrar
        tag = Tag.objects.create(name='test tag', weight=1.0, public=False, create_user=gestor)
        audit = Audit.objects.create(name='audit', description='test',start_date= '2017-01-05', usuario=usuario,
                            creation_date= '2017-01-05', auditor=auditor, state='INACTIVE', gestor=gestor)

        audit2 = Audit.objects.create(name='audit', description='test',start_date= '2017-01-05', usuario=usuario,
                            creation_date= '2017-01-05', auditor=auditor, state='ACTIVE', gestor=gestor)
        audit.tags.add(tag)
        audit2.tags.add(tag)
        #Creamos el item para editar y borrar, asociado a la etiqueta creada anteriormente
        item = Item.objects.create(name='ItemTest', question='QuestionTest', obligatory='SHALL', tag=tag)

        #Creamos tag pública para ver si puede ser vista por otros usuarios (su lista de items)
        tag_public = Tag.objects.create(name='test tag poublic', weight=1.0, public=True, create_user=gestor)
        item_public = Item.objects.create(name='ItemTestPublic', question='QuestionTest', obligatory='SHALL', tag=tag_public)
        #Creamos Answer a ser modificada y eliminada
        answer = Answer.objects.create(name="AnswerTest", value="1.0", item_id=1)
        Answer.objects.create(name="AnswerTest2", value="0.5", item_id=1)
        Answer.objects.create(name="AnswerTest3", value="0.0", item_id=1)

        #Creamos un documento para ser borrado
        Document.objects.create(filename="test.txt", docFile="test.txt", item=item)

        #Creamos instancia para auditoría
        self.client.login(username='auditor', password='auditor')
        response = self.client.post('/audits/create/instance/2',{'level':'LOW'})

    def test_view_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_list_audits_as_anonymous(self):
        response = self.client.get('/audits/list/gestor/audits/')
        #Se devuelve 302, que es una redirección hacia la página de login pues no se ha autenticado
        self.assertEqual(response.status_code, 302)

    def test_view_list_audits_as_gestor(self):
        login_success = self.client.login(username='gestor', password='gestor')
        response = self.client.get('/audits/list/gestor/audits/')
        #Se devuelve 200 pues el usuario está logado
        self.assertEqual(login_success, True)
        self.assertEqual(response.status_code, 200)

    def test_view_create_audits_as_anonymous(self):
        response = self.client.get('/audits/create/audit/')
        self.assertEqual(response.status_code, 302)

    def test_view_create_audits_as_usuario(self):
        self.client.login(username="usuario", password="usuario")
        response = self.client.get('/audits/create/audit/')

        self.assertEqual(response.status_code, 302)

    def test_view_create_audits_as_auditor(self):
        self.client.login(username="auditor", password="auditor")
        response = self.client.get('/audits/create/audit/')

        self.assertEqual(response.status_code, 302)

    def test_view_create_audits_as_gestor(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.get('/audits/create/audit/')

        self.assertEqual(response.status_code, 200)

    def test_create_bad_audit_as_gestor(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/audit/')

        self.assertEqual(response.context['form'].is_valid(), False)

    def test_create_good_audit_as_gestor(self):
        self.client.login(username = "gestor", password = 'gestor')
        gestor = User.objects.get(username='gestor')
        usuario = User.objects.get(username='usuario')
        auditor = User.objects.get(username='auditor')
        tag = Tag.objects.create(name='test tag', weight=1.0, public=False, create_user=gestor)
        response = self.client.post('/audits/create/audit/', {'name': 'test', 'description': 'test',
                                                              'start_date': '01/05/2017', 'period': 0, 'usuario':usuario.id,
                                                              'auditor':auditor.id, 'tags':{tag.id}})

        self.assertIsNotNone(Audit.objects.get(name="test"))

    def test_edit_audit_no_gestor(self):
        response = self.client.get('/audits/edit/gestor/audit/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/edit/gestor/audit/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/edit/gestor/audit/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_edit_audit_as_gestor(self):
        #Creamos la auditoría y luego la editamos
        self.client.login(username="gestor", password="gestor")
        gestor = User.objects.get(username='gestor')
        usuario = User.objects.get(username='usuario')
        auditor = User.objects.get(username='auditor')
        tag = Tag.objects.create(name='test tag', weight=1.0, public=False, create_user=gestor)
        self.client.post('/audits/create/audit/',
                         {'name': 'test', 'description': 'test',
                                 'start_date': '01/05/2017', 'period': 0, 'usuario':usuario.id,
                                 'auditor':auditor.id, 'tags':{tag.id}})

        audit = Audit.objects.get(id=1)
        response = self.client.post('/audits/edit/gestor/audit/'+str(audit.id), {'name': 'test2', 'description': 'test',
                                                              'start_date': '01/05/2017', 'period': 0, 'usuario':usuario.id,
                                                              'auditor':auditor.id, 'tags':{tag.id}})
        #Obtenemos la auditoría por su nuevo nombre
        audit_edit = Audit.objects.get(name="test2")
        #Comprobamos que se obtiene y que es la misma que se creo
        self.assertTrue(audit_edit and audit_edit.id == audit.id)

    def test_delete_audit_no_gestor(self):
        response = self.client.get('/audits/delete/gestor/audit/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/delete/gestor/audit/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/delete/gestor/audit/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_delete_audit_as_gestor(self):
        #Creamos la auditoría y luego la eliminamos
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/delete/gestor/audit/1')
        #Obtenemos la auditoría por su nuevo nombre
        #Comprobamos que se obtiene y que es la misma que se creo
        self.assertRaises(Audit.DoesNotExist, Audit.objects.get, id=1)

    def test_create_bad_user(self):
        #Creamos el usuario
        response = self.client.post("/audits/create/user/")
        self.assertEqual(response.context['form'].is_valid(), False)

    def test_create_good_user(self):
        #Creamos el usuario
        response = self.client.post("/audits/create/user/", {'username':'testUser', 'email':'test@test.com',
                                'password1':'test', 'password2':"test", 'name':'test', 'surname':'test', 'rol': 1})
        self.assertIsNotNone(User.objects.get(username="testUser"))

    def test_create_tag_no_gestor(self):
        response = self.client.get('/audits/create/tag/')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/create/tag/')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/create/tag/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_create_bad_tag(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/tag/')

        self.assertEqual(response.context['form'].is_valid(), False)

    def test_create_good_tag(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/tag/', {'name':'TagTest', 'weight':1.0, 'public':False})

        self.assertIsNotNone(Tag.objects.get(name="TagTest"))

    def test_edit_tag_no_gestor(self):
        response = self.client.get('/audits/edit/gestor/tag/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/edit/gestor/tag/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/edit/gestor/tag/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_edit_tag_as_gestor(self):
        self.client.login(username="gestor", password="gestor")
        #Obtenemos etiqueta de gestor1
        tag = Tag.objects.get(id=1)
        response = self.client.post('/audits/edit/gestor/tag/'+str(tag.id), {'name':'TagTestEdit', 'weight':1.0,
                                                                        'public':False, 'parent': ''})
        #Buscamos por el nuevo nombre
        tag_edit = Tag.objects.get(name="TagTestEdit")
        #Comprobamos que no sea nula y que tenga el mismo identificador
        self.assertTrue(tag_edit and tag_edit.id == tag.id)

    def test_edit_tag_no_owner(self):
        #Entramos como otro usuario
        self.client.login(username="gestor2", password="gestor2")
        #Intentamos editar la etiqueta que pertenece a otro gestor
        tag = Tag.objects.get(id=1)
        response = self.client.post('/audits/edit/gestor/tag/'+str(tag.id), {'name':'TagTestEdit', 'weight':1.0,
                                                                        'public':False, 'parent': ''})

        self.assertEqual(response.status_code, 302)

    def test_delete_tag_no_gestor(self):
        response = self.client.get('/audits/delete/gestor/tag/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/delete/gestor/tag/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/delete/gestor/tag/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_delete_tag_gestor(self):
        self.client.login(username="gestor", password="gestor")
        tag = Tag.objects.get(id=1)
        response = self.client.post('/audits/delete/gestor/tag/'+str(tag.id))

        self.assertRaises(Tag.DoesNotExist, Tag.objects.get, id=1)

    def test_delete_tag_no_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        tag = Tag.objects.get(id=1)
        response = self.client.post('/audits/delete/gestor/tag/'+str(tag.id))

        self.assertEqual(response.status_code, 302)

    def test_view_gestor_tags_tree_no_gestor(self):
        response = self.client.get('/audits/list/gestor/tags_tree')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/list/gestor/tags_tree')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/list/gestor/tags_tree')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_view_gestor_tags_tree_as_gestor(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.get('/audits/list/gestor/tags_tree')

        #Tenemos una etiqueta luego la lista debe tener tamaño 1
        self.assertEqual(len(response.context['tags']), 2)

    def test_view_gestor_tags_items_no_gestor(self):
        response = self.client.get('/audits/list/gestor/items/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/list/gestor/items/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/list/gestor/items/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_view_gestor_tags_items_no_owner_private(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.get('/audits/list/gestor/items/1')

        self.assertEqual(response.status_code, 302)

    def test_view_gestor_tags_items_no_owner_public(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.get('/audits/list/gestor/items/2')

        self.assertEqual(len(response.context['element_page']),1)

    def test_view_gestor_tags_items(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.get('/audits/list/gestor/items/1')

        self.assertEqual(len(response.context['element_page']),1)

    def test_create_gestor_item_no_gestor(self):
        response = self.client.get('/audits/create/gestor/item/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/create/gestor/item/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/create/gestor/item/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_create_gestor_item_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/create/gestor/item/1',
                                    {'name':'ItemCreate', 'question':'question','obligatory':'SHALL'})
        self.assertEqual(response.status_code, 302)

    def test_create_gestor_bad_item(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/gestor/item/1?page=1',{'name':'', 'question':'','obligatory':''})
        self.assertEqual(response.context['form'].is_valid(), False)

    def test_create_gestor_good_item(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/gestor/item/1',
                                    {'name':'ItemCreate', 'question':'question','obligatory':'SHALL'})

        self.assertIsNotNone(Item.objects.get(name='ItemCreate'))

    def test_details_gestor_item_no_gestor(self):
        response = self.client.get('/audits/item/gestor/details/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/item/gestor/details/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/item/gestor/details/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_details_gestor_item_no_owner_private(self):
        self.client.login(username="gestor2", password='gestor2')
        response = self.client.get('/audits/item/gestor/details/1')

        self.assertEqual(response.status_code, 302)

    def test_details_gestor_item_no_owner_public(self):
        self.client.login(username="gestor2", password='gestor2')
        response = self.client.get('/audits/item/gestor/details/2')

        self.assertEqual(response.status_code, 200)

    def test_details_gestor_item_owner(self):
        self.client.login(username="gestor", password='gestor')
        response = self.client.get('/audits/item/gestor/details/1')

        self.assertEqual(response.status_code, 200)

    def test_edit_gestor_item_no_gestor(self):
        response = self.client.get('/audits/edit/gestor/item/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/edit/gestor/item/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/edit/gestor/item/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_edit_gestor_item_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/edit/gestor/item/1',
                                    {'name':'ItemCreate', 'question':'question','obligatory':'SHALL'})
        self.assertEqual(response.status_code, 302)

    def test_edit_gestor_bad_item(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/edit/gestor/item/1',{'name':'', 'question':'','obligatory':''})
        self.assertEqual(response.context['form'].is_valid(), False)

    def test_edit_gestor_good_item(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/gestor/item/1',
                                    {'name':'ItemCreateEdit', 'question':'question','obligatory':'SHALL'})

        self.assertIsNotNone(Item.objects.get(name='ItemCreateEdit'))


    def test_delete_gestor_item_no_gestor(self):
        response = self.client.get('/audits/delete/gestor/item/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/delete/gestor/item/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/delete/gestor/item/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_edit_gestor_item_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/delete/gestor/item/1')
        self.assertEqual(response.status_code, 302)

    def test_delete_gestor_item_no_empty(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/delete/gestor/item/1')

        self.assertEqual(response.status_code, 302)

    def test_delete_gestor_item(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/delete/gestor/item/2')

        self.assertRaises(Item.DoesNotExist, Item.objects.get, id=2)

    def test_view_audit_details_no_users(self):
        self.client.login(username="auditor2", password="auditor2")
        response = self.client.get('/audits/audit/details/1')
        self.client.login(username="usuario2", password="usuario2")
        response2 = self.client.get('/audits/audit/details/1')
        self.client.login(username="gestor2", password="gestor2")
        response3 = self.client.get('/audits/audit/details/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_view_audit_details(self):
        #Editamos la auditoría a estado empezada
        audit = Audit.objects.get(id=1)
        audit.state = 'ACTIVE'
        audit.save()
        self.client.login(username="auditor", password="auditor")
        response = self.client.get('/audits/audit/details/1')
        self.client.login(username="usuario", password="usuario")
        response2 = self.client.get('/audits/audit/details/1')
        self.client.login(username="gestor", password="gestor")
        response3 = self.client.get('/audits/audit/details/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_view_audit_user_auditor_inactive(self):
        #Editamos la auditoría a estado inactiva
        audit = Audit.objects.get(id=1)
        audit.state = 'INACTIVE'
        audit.save()

        #Comprobamos que el usuario y el auditor no pueden verla aun
        self.client.login(username="auditor", password="auditor")
        response = self.client.get('/audits/audit/details/1')
        self.client.login(username="usuario", password="usuario")
        response2 = self.client.get('/audits/audit/details/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_view_audit_eliminated(self):
        #Editamos el estado a eliminada
        audit = Audit.objects.get(id=1)
        audit.state = 'ELIMINATED'
        audit.save()

        #Comprabamos que ninguno de sus usuarios tiene acceso a la misma
        self.client.login(username="auditor", password="auditor")
        response = self.client.get('/audits/audit/details/1')
        self.client.login(username="usuario", password="usuario")
        response2 = self.client.get('/audits/audit/details/1')
        self.client.login(username="gestor", password="gestor")
        response3 = self.client.get('/audits/audit/details/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_change_audit_state_no_gestor(self):
        self.client.login(username="auditor2", password="auditor2")
        response = self.client.get('/audits/audit/change/state/1')
        self.client.login(username="usuario2", password="usuario2")
        response2 = self.client.get('/audits/audit/change/state/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_change_audit_state_gestor_no_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.get('/audits/audit/change/state/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Audit.objects.get(id=1).state, 'INACTIVE')

    def test_change_audit_state_gestor(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.get('/audits/audit/change/state/1')

        self.assertEqual(Audit.objects.get(id=1).state, 'ACTIVE')

        self.client.get('/audits/audit/change/state/1')
        self.assertEqual(Audit.objects.get(id=1).state, 'FINISH')

        response = self.client.get('/audits/audit/change/state/1')
        self.assertEqual(Audit.objects.get(id=1).state, 'ELIMINATED')

    def test_create_gestor_item_answer_no_gestor(self):
        response = self.client.get('/audits/create/gestor/answer/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/create/gestor/answer/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/create/gestor/answer/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_create_gestor_item_answer_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/create/gestor/answer/1',
                                    {'name':'AnswerTest', 'value':1})
        self.assertEqual(response.status_code, 302)

    def test_create_gestor_bad_item_answer(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/gestor/answer/1',
                                    {'name':'', 'value':0})

        self.assertEqual(json.loads(response.content)['name'][0], "Este campo es obligatorio.")

    def test_create_gestor_good_item_answer(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/create/gestor/answer/1',
                                    {'name':'AnswerTestCreate', 'value':1})

        self.assertIsNotNone(Answer.objects.get(name='AnswerTestCreate'))

    def test_edit_gestor_item_answer_no_gestor(self):
        response = self.client.get('/audits/edit/gestor/answer/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/edit/gestor/answer/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/edit/gestor/answer/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_edit_gestor_item_answer_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/edit/gestor/answer/1',
                                    {'name':'AnswerTest', 'value':1})
        self.assertEqual(response.status_code, 302)

    def test_edit_gestor_bad_item_answer(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/edit/gestor/answer/1',
                                    {'name':'', 'value':0})

        self.assertEqual(response.context['form'].is_valid(), False)

    def test_edit_gestor_good_item_answer(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/edit/gestor/answer/1',
                                    {'name':'AnswerTestEdit', 'value':1})

        self.assertIsNotNone(Answer.objects.get(name='AnswerTestEdit'))

    def test_delete_gestor_item_answer_no_gestor(self):
        response = self.client.get('/audits/delete/gestor/answer/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/delete/gestor/answer/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/delete/gestor/answer/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

        self.assertIsNotNone(Answer.objects.get(id=1))

    def test_delete_gestor_item_answer_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/delete/gestor/answer/1')
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Answer.objects.get(id=1))

    def test_delete_gestor_item_answer(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/delete/gestor/answer/1')

        self.assertRaises(Answer.DoesNotExist, Answer.objects.get, id=1)

    def test_create_gestor_item_document_no_gestor(self):
        response = self.client.get('/audits/document/gestor/create/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/document/gestor/create/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/document/gestor/create/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_create_gestor_item_document_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/document/gestor/create/1',
                                    {'fileName':'Document', 'docFile': open('test.doc', 'w+')})
        self.assertEqual(response.status_code, 302)

    def test_create_gestor_bad_item_document(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/document/gestor/create/1',
                                    {'filename':'', 'docFile': open('test.doc', 'w+')})

        self.assertEqual(json.loads(response.content)['filename'][0], "Este campo es obligatorio.")
        self.assertEqual(json.loads(response.content)['docFile'][0], "El fichero enviado está vacío.")

    def test_create_gestor_good_item_document(self):
        self.client.login(username="gestor", password="gestor")
        #Creamos fichero
        file = open('test.txt', 'w+')
        file.write('Test');
        file.close()

        with open("test.txt") as filePost:
            response = self.client.post('/audits/document/gestor/create/1',
                                    {'filename':'Document', 'docFile': filePost})

        os.remove("test.txt")

        self.assertIsNotNone(Document.objects.get(filename="Document"))

    def test_delete_gestor_item_document_no_gestor(self):
        response = self.client.get('/audits/document/gestor/delete/1')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/document/gestor/delete/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/document/gestor/delete/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

        self.assertIsNotNone(Answer.objects.get(id=1))

    def test_delete_gestor_item_document_no_tag_owner(self):
        self.client.login(username="gestor2", password="gestor2")
        response = self.client.post('/audits/document/gestor/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Document.objects.get(id=1))

    def test_delete_gestor_item_document(self):
        self.client.login(username="gestor", password="gestor")
        response = self.client.post('/audits/document/gestor/delete/1')

        self.assertRaises(Document.DoesNotExist, Document.objects.get, id='1')

    def test_list_user_audit_no_user(self):
        response = self.client.get('/audits/list/user/audits/')
        self.client.login(username="auditor", password="auditor")
        response2 = self.client.get('/audits/list/user/audits/')
        self.client.login(username="gestor", password="gestor")
        response3 = self.client.get('/audits/list/user/audits/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_list_user_audit_as_user(self):
        self.client.login(username="usuario", password='usuario')
        response = self.client.get('/audits/list/user/audits/')

        self.assertEqual(len(response.context['element_page']),1)

    def test_list_auditor_audit_no_auditor(self):
        self.client.logout()
        response = self.client.get('/audits/list/auditor/audits/')
        self.client.login(username="usuario", password="usuario")
        response2 = self.client.get('/audits/list/auditor/audits/')
        self.client.login(username="gestor", password="gestor")
        response3 = self.client.get('/audits/list/auditor/audits/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_list_auditor_audit_as_auditor(self):
        self.client.login(username="auditor", password='auditor')
        response = self.client.get('/audits/list/auditor/audits/')

        self.assertEqual(len(response.context['element_page']),1)

    def test_create_instance_gestor(self):
        self.client.login(username='gestor', password='gestor')
        response = self.client.post('/audits/create/instance/2',{'level':'SHALL'})

        self.assertEqual(response.status_code,302)

    def test_create_instance_usuario_no_owner(self):
        self.client.login(username='usuario2', password='usuario2')
        response = self.client.post('/audits/create/instance/2',{'level':'SHALL'})

        self.assertEqual(response.status_code,302)

    def test_create_instance_auditor_no_owner(self):
        self.client.login(username='auditor2', password='auditor2')
        response = self.client.post('/audits/create/instance/2',{'level':'SHALL'})

        self.assertEqual(response.status_code,302)

    def test_create_instance_usuario_auditor_owner_inactive(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.post('/audits/create/instance/1',{'level':'SHALL'})

        self.client.login(username='auditor', password='auditor')
        response2 = self.client.post('/audits/create/instance/1',{'level':'SHALL'})

        self.assertEqual(response.status_code,302)
        self.assertEqual(response2.status_code,302)

    def test_create_bad_instance_usuario_auditor(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.post('/audits/create/instance/2',{'level':'WRONG'})

        self.client.login(username='auditor', password='auditor')
        response2 = self.client.post('/audits/create/instance/2',{'level':'WRONG'})

        self.assertEqual(response.context['form'].is_valid(), False)
        self.assertEqual(response2.context['form'].is_valid(), False)

    def test_create_instance_usuario(self):
        self.client.login(username='usuario', password='usuario')
        self.assertEqual(Audit.objects.get(id=2).instance_set.count(), 1)

        response = self.client.post('/audits/create/instance/2',{'level':'LOW'})

        self.assertEqual(Audit.objects.get(id=2).instance_set.count(), 2)

    def test_create_instance_usuario(self):
        self.client.login(username='auditor', password='auditor')
        self.assertEqual(Audit.objects.get(id=2).instance_set.count(), 1)

        response = self.client.post('/audits/create/instance/2',{'level':'LOW'})

        self.assertEqual(Audit.objects.get(id=2).instance_set.count(), 2)

    def test_evaluate_instance_gestor(self):
        self.client.login(username='gestor', password='gestor')
        response = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(response.status_code,302)

    def test_evaluate_instance_usuario_no_owner(self):
        self.client.login(username='usuario2', password='usuario2')
        response = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(response.status_code,302)

    def test_evaluate_instance_auditor_no_owner(self):
        self.client.login(username='auditor2', password='auditor2')
        response = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(response.status_code,302)

    def test_evaluate_instance_finish_usuario_auditor(self):
        instance = Instance.objects.get(id=1)
        instance.state = 'FINISH'
        instance.save()

        self.client.login(username='auditor', password='auditor')
        response = self.client.get('/audits/evaluate/instance/1')
        self.client.login(username='usuario', password='usuario')
        response2 = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(response.status_code,302)
        self.assertEqual(response2.status_code,302)

    def test_evaluate_instance_usuario(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(len(response.context['results']),1)

    def test_evaluate_instance_auditor(self):
        self.client.login(username='auditor', password='auditor')
        response = self.client.get('/audits/evaluate/instance/1')

        self.assertEqual(len(response.context['results']),1)

    def test_evaluate_instance_search(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.get('/audits/evaluate/instance/1?q=test')

        self.assertEqual(len(response.context['results']),1)

    def test_evaluate_instance_search_empty(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.get('/audits/evaluate/instance/1?q=wrong')

        self.assertEqual(len(response.context['results']),0)

    def test_finish_instance_no_user_or_auditor(self):
        self.client.logout()
        response = self.client.get('/audits/finish/instance/1')
        self.client.login(username='gestor', password='gestor')
        response2 = self.client.get('/audits/finish/instance/1')
        self.client.login(username='auditor2', password='auditor2')
        response3 = self.client.get('/audits/finish/instance/1')
        self.client.login(username='usuario2', password='usuario2')
        response4 = self.client.get('/audits/finish/instance/1')

        self.assertEqual(response.status_code,302)
        self.assertEqual(response2.status_code,302)
        self.assertEqual(response3.status_code,302)
        self.assertEqual(response4.status_code,302)

    def test_finish_instance_auditor(self):
        self.client.login(username='auditor', password='auditor')
        response = self.client.get('/audits/finish/instance/1')

        self.assertEqual(Instance.objects.get(id=1).state, 'FINISHED')

    def test_finish_instance_usuario(self):
        self.client.login(username='usuario', password='usuario')
        response = self.client.get('/audits/finish/instance/1')

        self.assertEqual(Instance.objects.get(id=1).state, 'FINISHED')

    def test_evaluate_instance_item_no_user_or_auditor(self):
        self.client.logout()
        response = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})
        self.client.login(username='gestor', password='gestor')
        response2 = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})
        self.client.login(username='auditor2', password='auditor2')
        response3 = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})
        self.client.login(username='usuario2', password='usuario2')
        response4 = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})

        self.assertEqual(response.status_code,302)
        self.assertEqual(response2.status_code,302)
        self.assertEqual(response3.status_code,403)
        self.assertEqual(response4.status_code,403)

    def test_evaluate_instance_item_usuario(self):
        self.client.login(username='usuario', password='usuario')
        self.assertEqual(Result.objects.get(id=1).answer_id, 3)
        response = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})

        self.assertEqual(Result.objects.get(id=1).answer_id, 1)

    def test_evaluate_instance_item_auditor(self):
        self.client.login(username='auditor', password='auditor')
        self.assertEqual(Result.objects.get(id=1).answer_id, 3)
        response = self.client.post('/audits/evaluate/item/', {'answer':1, 'result':1})

        self.assertEqual(Result.objects.get(id=1).answer_id, 1)

    def test_instance_evaluation_no__auditor(self):
        self.client.logout()
        response = self.client.get('/audits/view/auditor/evaluation/1')
        self.client.login(username='gestor', password='gestor')
        response2 = self.client.get('/audits/view/auditor/evaluation/1')
        self.client.login(username='auditor2', password='auditor2')
        response3 = self.client.get('/audits/view/auditor/evaluation/1')
        self.client.login(username='usuario', password='usuario')
        response4 = self.client.get('/audits/view/auditor/evaluation/1')

        self.assertEqual(response.status_code,302)
        self.assertEqual(response2.status_code,302)
        self.assertEqual(response3.status_code,302)
        self.assertEqual(response4.status_code,302)

    def test_instance_evaluation_auditor_no_finished(self):
         self.client.login(username='auditor', password='auditor')
         response = self.client.get('/audits/view/auditor/evaluation/1')

         self.assertEqual(response.status_code, 302)

    def test_instance_evaluation_auditor(self):
        #Evaluamos la instancia para que el resultado sea 50 y finalizamos
        self.client.login(username='auditor', password='auditor')
        self.client.post('/audits/evaluate/item/', {'answer':2, 'result':1})
        self.client.get('/audits/finish/instance/1')
        response = self.client.get('/audits/view/auditor/evaluation/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['res'], 50)
        dict = response.context['dicc']
        self.assertEqual(dict[dict.keys()[0]], [1,0.5,50])

    def test_create_instance_document_no_auditor(self):
        self.client.logout()
        response = self.client.get('/audits/document/auditor/create/1')
        self.client.login(username="gestor", password="gestor")
        response2 = self.client.get('/audits/document/auditor/create/1')
        self.client.login(username="usuario", password="usuario")
        response3 = self.client.get('/audits/document/auditor/create/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response3.status_code, 302)

    def test_create_auditor_bad_instance_document(self):
        self.client.login(username="auditor", password="auditor")
        self.client.get('/audits/finish/instance/1')
        response = self.client.post('/audits/document/auditor/create/1',
                                    {'filename':'', 'docFile': open('test.doc', 'w+')})

        self.assertEqual(json.loads(response.content)['filename'][0], "Este campo es obligatorio.")
        self.assertEqual(json.loads(response.content)['docFile'][0], "El fichero enviado está vacío.")

    def test_create_auditor_good_instance_document(self):
        self.client.login(username="auditor", password="auditor")
        self.client.get('/audits/finish/instance/1')
        #Creamos fichero
        file = open('test.txt', 'w+')
        file.write('Test');
        file.close()

        with open("test.txt") as filePost:
            response = self.client.post('/audits/document/auditor/create/1',
                                    {'filename':'Document', 'docFile': filePost})

        os.remove("test.txt")

        self.assertIsNotNone(Document.objects.get(filename="Document"))

    def test_create_auditor_document_not_finished_instance(self):
        self.client.login(username="auditor", password="auditor")
        #Creamos fichero
        file = open('test.txt', 'w+')
        file.write('Test');
        file.close()

        with open("test.txt") as filePost:
            response = self.client.post('/audits/document/auditor/create/1',
                                    {'filename':'Document', 'docFile': filePost})

        os.remove("test.txt")

        self.assertIsNotNone(response.status_code, 302)