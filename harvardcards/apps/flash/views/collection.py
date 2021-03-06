from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.context_processors import csrf
from django.core.exceptions import ViewDoesNotExist

from django.utils import simplejson as json

from django.forms.formsets import formset_factory
from harvardcards.apps.flash.models import Collection, Users_Collections, Deck, Field
from harvardcards.apps.flash.forms import CollectionForm, FieldForm, DeckForm

def index(request):
    collections = Collection.objects.all()
    user_collection_role = Users_Collections.get_role_buckets(request.user, collections)
    decks = Deck.objects.all().prefetch_related('collection', 'cards')

    decks_by_collection = {}
    for deck in decks:
        if deck.collection.id not in decks_by_collection:
            decks_by_collection[deck.collection.id] = []
        decks_by_collection[deck.collection.id].append(deck)


    collection_list = []
    for collection in collections:
        collection_decks = []
        for deck in decks_by_collection[collection.id]:
            collection_decks.append({
                'id': deck.id,
                'title': deck.title,
                'num_cards': deck.cards.count()
            })
        collection_list.append({
            'id': collection.id,
            'title':collection.title,
            'decks': collection_decks
        })

    context = {
        "collections": collection_list,
        "user_collection_role": user_collection_role
    }

    return render(request, 'collection_index.html', context)
    
def create(request, collection_id=None):
    # is it a post?
    message = '';
    if request.method == 'POST':

        #for key in request.POST:
        #    value = request.POST[key]
        #    message += "{0} => {1}<br>".format(key, value)
        #return HttpResponse(message)
        
        if 'collection_id' in request.POST:
            collection = Collection.objects.get(id=request.POST['collection_id'])
            collectionForm = CollectionForm(request.POST, instance=collection)
            
        else:
            collectionForm = CollectionForm(request.POST)

        if collectionForm.is_valid():
            collection = collectionForm.save()

            # create the formset from the base fieldform
            #FieldFormSet = formset_factory(FieldForm)
            # decode json
            data = json.loads(request.POST['field_data'])            
            #return HttpResponse(repr(data))

            # is it an edit?
            # get all ids from data
            editList = []
            for d in data:
                if 'id' in d:
                    editList.append(d['id']);
            if len(editList):
                # then run through all ids in the db
                # if they are not in edit list, delete them
                existingFields = Field.objects.filter(collection=collection.id)
                for ef in existingFields:
                    if ef.id not in editList:
                        ef.delete()
                

            # run through field_data
            for d in data:
                if 'id' in d:
                    field = Field.objects.get(id=d['id'])
                    fieldForm = FieldForm(d, instance=field)
                else:
                    fieldForm = FieldForm(d)
                
                f = fieldForm.save(commit=False)
                # this is how relationships have to be done -- forms cannot handle this
                # so you have to do it directly at the model
                f.collection = collection
                f.save()
                
                

            return redirect(index)
        else:
            return render(request, 'collections/create.html')
    
    # is it an edit?
    elif collection_id:
        collection = Collection.objects.get(id=collection_id)
        fields = collection.field_set.all().order_by('sort_order')
        if collection:
            return render(request, 'collections/create.html', {"collection": collection, "fields": fields})
        else:
            raise ViewDoesNotExist("Course does not exist.")
    
            
    else:
        return render(request, 'collections/create.html')

def delete(request):
    returnValue = "false"
    if request.GET['id']:
        collection_id = request.GET['id']
        Collection.objects.filter(id=collection_id).delete()
        if not Collection.objects.filter(id=collection_id):
            returnValue = "true"
    
    return HttpResponse('{"success": %s}' % returnValue, mimetype="application/json")
    
def fields(request):
    if 'collection_id' in request.POST:
        collection_id = request.POST['collection_id']
        collection = Collection.objects.get(id=collection_id)
        fields = collection.field_set.all().order_by('sort_order')
        errorMsg = '';
        field_list = []
        for field in fields:
            f = {}
            f['label'] = field.label
            f['id'] = field.id
            f['field_type'] = field.field_type
            f['sort_order'] = field.sort_order
            f['display'] = field.display
            field_list.append(f)
            
        fields_json = json.dumps(field_list)
        return HttpResponse('{"success": true, "fields": %s}' % fields_json, mimetype="application/json")
        
    else:
        errorMsg = "No collection_id specified."
        for key, value in request.POST.iteritems():
            errorMsg += "<br>" + key + " => " + value
    return HttpResponse('{"success": true, "error": "%s"}' % errorMsg, mimetype="application/json")
