from typing import List

from tinydb import Query

from chat_thief.models.database import db_table


class SFXVote:
    table_name = "sfx_votes"
    database_folder = ""
    database_path = "db/sfx_votes.json"

    def __init__(self, command, supporters=[], detractors=[]):
        self.command = command
        self.supporters = supporters
        self.detractors = detractors

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def support(self, supporter):
        vote = self._find_or_create_vote()
        def show_support(supporter):
            def transform(doc):
                if supporter not in doc["supporters"]:
                    doc["supporters"].append(supporter)
                if supporter in doc["detractors"]:
                    doc["detractors"].remove(supporter)
            return transform
        self.db().update(show_support(supporter), Query().command == self.command)

    def detract(self, detractor):
        vote = self._find_or_create_vote()
        def detract_support(detractor):
            def transform(doc):
                if detractor not in doc["detractors"]:
                    doc["detractors"].append(detractor)
                if detractor in doc["supporters"]:
                    doc["supporters"].remove(detractor)
            return transform
        self.db().update(detract_support(detractor), Query().command == self.command)

    def supporter_count(self):
        vote = self._find_or_create_vote()
        return len(vote["supporters"])

    def detractor_count(self):
        vote = self._find_or_create_vote()
        return len(vote["detractors"])

    def _find_or_create_vote(self):
        vote = self.db().get(Query().command == self.command)

        if vote:
            return vote
        else:
            print(f"Creating New SFXVote: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def doc(self):
        return {
            "command": self.command,
            "supporters": self.supporters,
            "detractors": self.detractors
        }


class ChatModerator:
    def __init__(self, user):
        self.user = user


    # We could use the health there
    # How do we want this to work
    # How do we prevent voting abuse
    #
    #
    # Everyone gets one vote per command
    # Should we create a structure
    # tracking votes

    # User
    #     - Pro: List
    #     - Cons: List
    # Command
    #     - Pro: List
    #     - Cons: List
    # SFXVote
    #     - Command
    #     - Pros
    #     - Cons

    def remove(self, target_user=None, target_command=None):
        pass
