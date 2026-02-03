class AIGovernance:

    def validate(self, session, message_text):
        if len(message_text) > 1000:
            return False, "Message too long"

        if session.status in ["completed", "cancelled"]:
            return False, "Session closed"

        banned = ["abuse", "hack", "illegal"]
        for word in banned:
            if word in message_text.lower():
                return False, "Unsafe content"

        return True, None
