class AppRouter:
    app_labels_db_map = {
        'book': 'book_app',
        'book_categories': 'book_app',
        'clothes': 'clothes_app',
        'clothes_categories': 'clothes_app',
        'mobile': 'mobile_app',
        'mobile_categories': 'mobile_app',
    }

    def db_for_read(self, model, **hints):
        return self.app_labels_db_map.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = self.db_for_read(obj1)
        db_obj2 = self.db_for_read(obj2)
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name = None, **hints):
        return db == self.app_labels_db_map.get(app_label, 'default')
