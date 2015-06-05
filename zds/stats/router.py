class StatsRouter(object):
    """
    A router to control all database operations on models in the
    stats application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read stats models go to stats_db.
        """
        print "1 ====================> {} \n\n\n".format(model._meta.app_label)
        if model._meta.app_label == 'stats':
            return 'stats_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write stats models go to stats_db.
        """
        print "2 ====================> {} \n\n\n".format(model._meta.app_label)
        if model._meta.app_label == 'stats':
            return 'stats_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the stats app is involved.
        """
        print "3====================> {} \n\n\n".format(obj1._meta.app_label)
        print "4====================> {} \n\n\n".format(obj2._meta.app_label)
        if obj1._meta.app_label == 'stats' or \
           obj2._meta.app_label == 'stats':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the stats app only appears in the 'stats_db'
        database.
        """
        print "5====================> {} \n\n\n".format(model._meta.app_label)
        if db == 'stats_db':
            return model._meta.app_label == 'stats'
        elif model._meta.app_label == 'stats':
            return False
        return None