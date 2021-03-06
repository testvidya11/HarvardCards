from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, through='Users_Collections')

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def __unicode__(self):
        return self.title

    def export(self):
        return repr(dict(title=self.title, description=self.description))

class Field(models.Model):
    label = models.CharField(max_length=200, blank=True)
    FIELD_TYPES = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('A', 'Audio'),
        ('V', 'Video')        
    )
    field_type = models.CharField(max_length=1, choices=FIELD_TYPES)
    show_label = models.BooleanField()
    collection = models.ForeignKey(Collection)
    display = models.BooleanField()
    sort_order = models.IntegerField()

    def __unicode__(self):
        return self.label

    def export(self):
        return repr(dict(label=self.label, field_type=self.field_type, sort_order=self.sort_order, display=self.display))

class Card(models.Model):
    collection = models.ForeignKey(Collection)
    sort_order = models.IntegerField()
    fields = models.ManyToManyField(Field, through='Cards_Fields')

    def __unicode__(self):
        return "Card: " + str(self.id) + "; Collection: " + str(self.collection.title)

#class User(models.Model):
#    name = models.CharField(max_length=200)
#    email = models.CharField(max_length=200)
    
class Users_Collections(models.Model):
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection)
    ROLES = (
        ('G', 'Guest'),
        ('S', 'Student'),
        ('A', 'Admin'),
        ('O', 'Owner')
    )
    role = models.CharField(max_length=1, choices=ROLES, default='G')
    date_joined = models.DateField()

    def __unicode__(self):
        return "User Collections: " + "user=" + str(self.user.pk) + "collection=" + str(self.collection.pk) + "role=" + str(self.role)

    @classmethod
    def get_role_buckets(self, user, collections):
        ''' Given a user and a set of collections, this function returns a
        dictionary that maps roles to collections. '''

        role_map = dict([(role[0], role[1].upper()) for role in self.ROLES])
        role_buckets = dict([(bucket, []) for bucket in role_map.values()])

        user_collections = dict([
            (item.collection_id, item.role)
            for item in self.objects.filter(user=user.id)
        ])

        for collection in collections:
            if user.is_superuser:
                role = 'A'
            elif collection.id in user_collections:
                role = user_collections[collection.id]
            else:
                role = 'G'
            role_buckets[role_map[role]].append(collection.id)

        return role_buckets

class Deck(models.Model):
    title = models.CharField(max_length=200)
    collection = models.ForeignKey(Collection)
    cards = models.ManyToManyField(Card, through='Decks_Cards')

    def __unicode__(self):
        return self.title

    def export(self):
        return repr(dict(title=self.title, collection=self.collection.id, id=self.id))

class Decks_Cards(models.Model):
    deck = models.ForeignKey(Deck)
    card = models.ForeignKey(Card)
    sort_order = models.IntegerField()

    class Meta:
        verbose_name = 'Deck Cards'
        verbose_name_plural = 'Deck Cards'

    def __unicode__(self):
        return "Deck: " + str(self.deck.title) + "; Card: " + str(self.card.id)

class Cards_Fields(models.Model):
    value = models.CharField(max_length=500)
    card = models.ForeignKey(Card)
    field = models.ForeignKey(Field)
    sort_order = models.IntegerField()

    class Meta:
        verbose_name = 'Card Fields'
        verbose_name_plural = 'Card Fields'

    def __unicode__(self):
        return self.value
