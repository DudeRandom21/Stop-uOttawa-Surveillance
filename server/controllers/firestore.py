from google.cloud import firestore
from server.controllers.abc import DatabaseDriver


class FirestoreDriver(DatabaseDriver):
    valid_counts = {'verified', 'total'},

    def __init__(self, project_id, oauth2_credentials):
        db = firestore.Client(
            project=project_id,
            credentials=oauth2_credentials
        )
        client = db.collection('students')
        self.metadata = client.document('metadata')
        super(FirestoreDriver, self).__init__(client)

    def add(self, data):
        doc_ref = self.database_client.add(data)
        self.metadata.update({
            'total_documents': firestore.Increment(1)
        })
        return doc_ref.id

    def _find(self, identifier):
        search_fields = identifier.keys()
        query = self.database_client
        for field in search_fields:
            query = query.where(field, '==', identifier[field])
        document = next(query.stream())
        return document

    def delete(self, identifier):
        document = self._find(identifier)
        doc_data = document.get().to_dict()
        if doc_data['verified']:
            self.metadata.update({
                'total_verified': firestore.Increment(-1),
                'total_ducments': firestore.Increment(-1)
            })
        document.delete()

    def update(self, identifier, update):
        document = self._find(identifier)
        document.update(update)

    def set_verified(self, id_str):
        document = self.database_client.document(id_str)

        document.update({'verified': True})
        self.metadata.update({
            'total_verified': firestore.Increment(1)
        })

        return True

    def count_records(self, identifier):
        if not all((_id in self.valid_counts for _id in identifier.keys())):
            raise TypeError('Cannot count records with this identifier')

        if 'total' in identifier:
            return self.metadata.get().to_dict()['total_documents']

        if 'verified' in identifier and identifier['verified']:
            return self.metadata.get().to_dict()['total_verified']

        if 'verified' in identifier and not identifier['verified']:
            doc = self.metadata.get().to_dict()
            not_verified = doc['total_documents'] - doc['total_verified']
            return not_verified