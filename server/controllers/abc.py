'''Abstract base classes'''


class DatabaseDriver:
    def __init__(self, database_client=None):
        self.database_client = database_client

    def add_student(self, data):
        raise NotImplementedError()

    def add_testimonial(self, data):
        raise NotImplementedError()

    def get_testimonials(self):
        raise NotImplementedError()

    def delete(self, data):
        raise NotImplementedError()

    def update(self, identifier, update):
        raise NotImplementedError()

    def set_student_verified(self, id_str):
        raise NotImplementedError()

    def set_testimonial_verified(self, id_str):
        raise NotImplementedError()

    def count_records(self, identifier):
        raise NotImplementedError()


class EmailDriver:
    def __init__(self, api_key, mail_domain):
        raise NotImplementedError()

    def send_validation_mail(self, target_name, target_email, link_id):
        raise NotImplementedError()

    def send_contact_mail(self, sender_name, sender_email, sender_comment):
        raise NotImplementedError()


class SocialDriver:
    def __init__(self, api_url):
        raise NotImplementedError()

    def post_comment(self, comment, **metadata):
        raise NotImplementedError()

    def post_testimonial(self, testimonial, name, program, year, id_str):
        raise NotImplementedError()
