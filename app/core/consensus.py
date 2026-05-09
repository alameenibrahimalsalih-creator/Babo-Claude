class ConsensusEngine:
    def evaluate(self, votes, threshold=0.85):
        weighted_score = 0
        total_weight = 0

        for vote in votes:
            weighted_score += vote["confidence"] * vote["weight"]
            total_weight += vote["weight"]

        if total_weight == 0:
            return {"approved": False, "score": 0}

        consensus = weighted_score / total_weight
        return {
            "approved": consensus >= threshold,
            "score": consensus
        }
