from datetime import datetime

import pytz


class GroupSelector(object):
    PAST = 0
    PRESENT = 2
    FUTURE = 1

    def __init__(self, now=None):
        if now is None:
            now = datetime.now(tz=pytz.UTC)

        self.now = now

    def _get_status(self, membership):
        if membership.from_date <= self.now and (membership.to_date is None or membership.to_date > self.now):
            status = self.PRESENT
        elif membership.from_date > self.now:
            status = self.FUTURE
        else:
            status = self.PAST

        return status

    def _select_past(self, a, b):
        """
        Return the membership with the latest to date.

        Settle ties using the newest membership (by ID).
        """

        if a.to_date > b.to_date:
            return a
        elif b.to_date > a.to_date:
            return b
        elif a.from_date < b.from_date:
            return a
        elif b.from_date < a.from_date:
            return b
        elif a.id > b.id:
            return a
        else:
            return b

    def _select_present(self, a, b):
        """
        Return the membership with the latest to date.

        Settle ties using the earliest from date and then the newest membership (by ID).
        """

        if a.to_date is None and b.to_date is not None:
            return a
        elif b.to_date is None and a.to_date is not None:
            return b
        elif a.to_date > b.to_date:
            return a
        elif b.to_date > a.to_date:
            return b
        elif a.from_date < b.from_date:
            return a
        elif b.from_date < a.from_date:
            return b
        elif a.id > b.id:
            return a
        else:
            return b

    def _select_future(self, a, b):
        """
        Return the membership with the earliest from date.

        Settle ties using the latest to date and then the newest membership (by ID).
        """

        if a.from_date < b.from_date:
            return a
        elif b.from_date < a.from_date:
            return b
        elif a.to_date is None and b.to_date is not None:
            return a
        elif b.to_date is None and a.to_date is not None:
            return b
        elif a.to_date > b.to_date:
            return a
        elif b.to_date > a.to_date:
            return b
        elif a.id > b.id:
            return a
        else:
            return b

    def select_group(self, membership_a, membership_b):
        """
        Return the CURRENT membership, the FUTURE membership, or the PAST membership.
        """

        status_a = self._get_status(membership_a)
        status_b = self._get_status(membership_b)

        if status_a > status_b:
            return membership_a
        elif status_b > status_a:
            return membership_b
        elif status_a == self.PAST:
            return self._select_past(membership_a, membership_b)
        elif status_a == self.PRESENT:
            return self._select_present(membership_a, membership_b)
        else:
            return self._select_future(membership_a, membership_b)

    @classmethod
    def select_groups(cls, memberships):
        """
        Return a single memberships for each group.

        The precedence is CURRENT, FUTURE, and PAST.
        """

        selector = cls()
        results = {}

        for membership in memberships:
            group = membership.group
            other_membership = results.get(group)

            if other_membership is not None:
                membership = selector.select_group(membership, other_membership)

            results[group] = membership

        results = results.values()

        return results
