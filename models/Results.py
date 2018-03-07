from models.RethinkDB import RethinkDB


class Results(RethinkDB):

    def __init__(self):
        super().__init__()
        super().set_entity('results')
